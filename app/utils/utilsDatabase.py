from SECRET import *
from sqlalchemy import create_engine
from flask import flash
import pandas as pd
from app.models import Asset, TrainHistory, StockPrediction
from app import db

def actualize_data(data):
    """
    la fonction va récuper les dernieres données de l'API,
    et ensuite les append dans la table assets_tables
    de la base de données.
    """
    last_value_df = data.tail(1)

    engine = create_engine('mysql+mysqldb://{user}:{password}@{server}:{port}/{database}?charset=utf8mb4'.format(**DATABASE))

    # on récupère la derniere row inséré dans la base de donnée
    last_value_db = pd.read_sql_query("""SELECT * from stock_history
                                        ORDER BY date
                                        DESC LIMIT 1;""", engine, index_col='date')

    if last_value_df.index.values == last_value_db.index.values:
        flash("La base de donnée est deja a jour...")

    elif last_value_db.empty == True:
        data.to_sql(name='stock_history', con=engine, if_exists='append')
        flash("La base de donnée à reçu ses première observation")

    else :
        # On recupère les lignes qui sont supérieurs à la dernière date enrégistré dans la base de données
        ecart_df = data[data.index.values > last_value_db.index.values]

        ecart_df.to_sql(name='stock_history', con=engine, if_exists='append')
        flash("{} row(s) ont été rajoutée(s) à la table stock_history".format(len(ecart_df)))

    return data


def get_asset(instrument):
    """ Get asset by name, if not exist: create"""
    asset = Asset.query.filter(Asset.name == instrument).first()
    if not asset:
        asset = Asset(instrument)
        db.session.add(asset)
        db.session.commit()

    return asset


def save_prediction(x_pred, x_previous, asset, model):
    """
    :param x_pred:
    :param x_previous:
    :param asset:
    :param model:
    :return:
    """
    # sauvegarde  de la prédiction dans la base de données
    prediction = pd.DataFrame(x_pred)
    prediction.columns = x_previous.columns
    new_date = x_previous.index.values.max() + pd.to_timedelta(1, 'hours')  # ajoute une heure

    stock = StockPrediction()
    stock.add_cotations(**prediction.to_dict())
    stock.train_history = model
    stock.asset = asset
    stock.date = new_date

    db.session.add(stock)
    db.session.commit()

    return stock
