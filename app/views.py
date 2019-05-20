from app import app
from flask import render_template, request, flash, redirect, url_for
import fxcmpy
import pandas as pd
from SECRET import *
from sqlalchemy import create_engine

import app.ScriptModel as script_model


@app.route('/')
def index():
    # connection API fxcmpy
    con_fxcmpy = fxcmpy.fxcmpy(FXCMY_ACCESS_TOKEN, server='demo')

    # list of instruments, generate choice for get data in view
    instruments = con_fxcmpy.get_instruments()
    return render_template('index.html', instruments=instruments)


@app.route('/get-data-<instrument>', methods=['GET'])
def get_data(instrument):
    """
    Stock data for one instrument in csv
    :param instrument: name of instrument for research
    :return: json of data for instrument
    """
    # connection API fxcmpy
    con_fxcmpy = fxcmpy.fxcmpy(FXCMY_ACCESS_TOKEN, server='demo')

    # search params GET for get candle
    params_candle = request.args.to_dict()
    if request.args.get('number'):
        params_candle['number'] = int(params_candle['number'])

    # get data from api, use GET params
    data = con_fxcmpy.get_candles(instrument, **params_candle)
    con_fxcmpy.close()

    data = actualize_data(data)

    # stock data in csv
    filename = 'bourse_' + instrument + '.csv'
    data.to_csv('app/data/' + filename)

    return data.to_json()


@app.route('/train-model')
def train_model():
    """ entraîne le modèle sur les donnèes existantes
        effectue une sauvegarde du model
    """
    model = script_model.train_model()
    flash('Le modèle à bien été entraîné')
    return redirect(url_for('index'))


@app.route('/get-predict')
def get_predict():
    """ Prédiction du modèle """
    model_name = 'modelDAX_Hour0.hdf5'
    # récupère toutes les données
    data = script_model.get_data_on_db()

    inputs_pred_ds, real_input_ds = script_model.make_prediction(data, model_name)

    print(zip(inputs_pred_ds, real_input_ds))
    flash('Prédiction effectuées')
    return redirect(url_for('index'))


def actualize_data(data):
    """
    la fonction va récuper les dernieres données de l'API,
    et ensuite les append dans la table assets_tables
    de la base de données.
    """
    last_value_df = data.tail(1)

    engine = create_engine('mysql+mysqldb://{user}:{password}@{server}:{port}/{database}?charset=utf8mb4'.format(**DATABASE))

    # on récupère la derniere row inséré dans la base de donnée
    last_value_db = pd.read_sql_query("""SELECT * from assets_tables
                                        ORDER BY date
                                        DESC LIMIT 1;""", engine, index_col='date')

    if last_value_df.index.values == last_value_db.index.values:
        print("La base de donnée est deja a jour...")

    else :
        # On recupère les lignes qui sont supérieurs à la dernière date enrégistré dans la base de données
        ecart_df = data[data.index.values > last_value_db.index.values]

        ecart_df.to_sql(name='assets_tables', con=engine, if_exists='append')
        print("{} row(s) ont été rajoutée(s) à la table assets_tables".format(len(ecart_df)))

    return data
