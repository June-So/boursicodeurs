from SECRET import *

import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from app import db
from sklearn.preprocessing import MinMaxScaler
from app.models import TrainHistory, StockPrediction
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.callbacks import ModelCheckpoint
from keras.optimizers import Adam
from keras.layers import LSTM
from keras.layers import RepeatVector
from keras.layers import TimeDistributed
from sklearn.model_selection import train_test_split
from keras import backend as K
from sklearn.metrics import mean_squared_error
from app.models import TrainHistory, Asset

#time_steps = 100
#backsize = 32
#epochs = 2
N_FEATURE = 9

def get_data_on_db():
    """
        get data for database in format csv
    """
    engine = create_engine('mysql+mysqldb://{user}:{password}@{server}:{port}/{database}?charset=utf8mb4'.format(**DATABASE))

    # Récuperer les données de la base de donnée dans un dataframe
    data = pd.read_sql_query("""SELECT * FROM stock_history;""", engine, index_col='date')
    data = data.drop(['asset_id', 'id'], axis=1)
    return data



# splitage du dataset en trois parties
def split_data(data):
    """Split data in three dataframe
        train dataframe
        valid dataframe
        test dataframe
     """
    df_train, df_test = train_test_split(data, train_size=0.85, test_size=0.15, shuffle=False)
    df_valid, df_test = train_test_split(df_test, train_size=0.6, test_size=0.4, shuffle=False)
    return df_train, df_valid, df_test



def normalize_data(data):
    """
    take an input data and return data scaled
    in range 0,1
    """
    if data.shape[1] > 1:
        data = data.values
    else :
        data = data.values.reshape(-1,1)

    sc = MinMaxScaler(feature_range = (0, 1))
    data = sc.fit_transform(data)

    return data, sc



def make_timeseries(mat, time_steps):
    """this function transform array in timeseries array"""
    dim_0 = mat.shape[0]

    X = [] # va correspondre aux entrées : timesteps
    y = [] # va correspondre à la sortie : 1

    for i in range(time_steps, dim_0):
        X.append(mat[(i-time_steps):i])
        y.append(mat[i,])

    X, y = np.array(X), np.array(y)
    y = np.reshape(y, (y.shape[0], 1, y.shape[1]))

    return X, y



def build_model(time_steps):
    model = Sequential()
    model.add(LSTM(100, activation='relu', input_shape=(time_steps,N_FEATURE)))
    model.add(RepeatVector(1))
    model.add(LSTM(100, activation='relu', return_sequences=True))
    model.add(TimeDistributed(Dense(N_FEATURE)))
    optimizer = Adam(lr=0.001)
    model.compile(optimizer = optimizer, loss = 'mean_squared_error')
    return model



def fit_model(X_train, y_train, X_valid, y_valid, epochs=5, batch_size=10, time_steps=2, train_history=None):
    """la variable modif permet de pas écrasser après modification,
     le model entrainé précédement"""
    K.clear_session()
    filename = train_history.filename
    checkpoint = ModelCheckpoint('app/models/' + filename, monitor='val_loss',mode='min', verbose=1, save_best_only=True)
    regressor_trained = build_model(time_steps)
    regressor_trained.fit(X_train, y_train, epochs = epochs, batch_size = batch_size, validation_data = (X_valid, y_valid),
                callbacks=[checkpoint])

    return regressor_trained


def loaded_model(filename, time_steps):
    K.clear_session()
    model = build_model(time_steps)
    model.load_weights('app/models/' + filename)
    return model


def make_inputs(mat, time_steps):
    """format input before predict"""
    dim_0 = mat.shape[0]
    #time_steps = 400 # le nbre de time_steps

    X = [] # va correspondre aux entrées : 60 timesteps
    y = [] # va correspondre à la sortie : 1

    for i in range(time_steps, dim_0+1):
        X.append(mat[(i-time_steps):i+1])
        y.append(mat[i-1,])

    X, y = np.array(X), np.array(y)
    #X_train = np.reshape(X, (X.shape[0], X.shape[1], 1))

    return X, y


def make_prediction(data, train_history, asset):
    K.clear_session()

    previousDays = len(data) - train_history.time_steps


    # l'entrée est contitué des derniers jour récupérés
    inputs = data.iloc[previousDays:]

    # on reformate l'entré pour que l'entrée corresponde à l'entré du model
    #inputs_sc = sc.transform(inputs)
    inputs_sc, sc = normalize_data(inputs)

    #X_inputs, y_inputs = make_timeseries(inputs_sc)
    X_inputs, y_inputs = make_inputs(inputs_sc, train_history.time_steps)

    # chargement du model
    model = loaded_model(train_history.filename, train_history.time_steps)
    #X_inputs, y_inputs =

    # faire la prédiction
    inputs_pred = model.predict(X_inputs)
    # il faut déscaliser la prédiction et le target
    inputs_pred_ds = sc.inverse_transform(inputs_pred.reshape(-1,N_FEATURE))
    real_input_ds = sc.inverse_transform(y_inputs.reshape(-1,N_FEATURE))

    # sauvegarde dans la base de données
    prediction = pd.DataFrame(inputs_pred_ds)
    prediction.columns = inputs.columns

    stock = StockPrediction()
    stock.add_cotations(**prediction.to_dict())
    print(type(inputs.index.values.max()))
    new_date = inputs.index.values.max() + pd.to_timedelta(1,'hours')
    stock.date = new_date
    stock.train_history = train_history
    stock.asset = asset

    db.session.add(stock)
    db.session.commit()

    return stock


def train_model(epochs, batch_size, time_steps):
    """this function allowed to train model"""
    K.clear_session()
    data = get_data_on_db()

    dataset_train, dataset_valid, dataset_test = split_data(data)

    train_sc, sc = normalize_data(dataset_train)

    valid_sc = sc.transform(dataset_valid)

    test_sc = sc.transform(dataset_test)


    # faire des données X_train et y_train
    X_train, y_train = make_timeseries(train_sc, time_steps)

    X_valid, y_valid = make_timeseries(valid_sc, time_steps)

    X_test, y_test = make_timeseries(test_sc, time_steps)

    ## Save history
    train_history = TrainHistory(epochs=epochs, time_steps=time_steps, batch_size=batch_size)
    train_history.total_train = X_train.shape[0]
    train_history.total_validation = X_valid.shape[0]
    train_history.total_test = X_test.shape[0]
    db.session.add(train_history)
    db.session.commit()

    train_history.filename = 'modelDAX_Hour' + str(train_history.id) + '.hdf5'
    db.session.commit()


    model_trained = fit_model(X_train, y_train, X_valid, y_valid, epochs = epochs, batch_size= batch_size, time_steps= time_steps, train_history=train_history)

    # Prediction sur les données du train suivi de sa descalisation
    y_pred_train = model_trained.predict(X_train)
    y_pred_train = y_pred_train.reshape(-1,N_FEATURE)
    y_pred_train_ds = sc.inverse_transform(y_pred_train)

    # Prediction sur les données de la validation suivi de sa descalisation
    y_pred_valid = model_trained.predict(X_valid)
    y_pred_valid = y_pred_valid.reshape(-1,N_FEATURE)
    y_pred_valid_ds = sc.inverse_transform(y_pred_valid)

    # Prediction sur les données du test suivi de sa descalisation
    y_pred_test = model_trained.predict(X_test)
    y_pred_test = y_pred_test.reshape(-1,N_FEATURE)
    y_pred_test_ds = sc.inverse_transform(y_pred_test)

    # metrics du models
    rmse_train = round(np.sqrt(mean_squared_error(y_pred_train, y_train.reshape(-1,N_FEATURE))),3)
    rmse_valid = round(np.sqrt(mean_squared_error(y_pred_valid, y_valid.reshape(-1,N_FEATURE))),3)
    rmse_test = round(np.sqrt(mean_squared_error(y_pred_test, y_test.reshape(-1,N_FEATURE))),3)

    # insertion des metrics dans la base de donnée
    train_history.score_train = rmse_train
    train_history.score_validation = rmse_valid
    train_history.score_test = rmse_test
    db.session.commit()

    return model_trained
