from app import app, db
from flask import render_template, request, flash, redirect, url_for
import fxcmpy
import pandas as pd
from SECRET import *
from sqlalchemy import create_engine
from .utils import utilsDatabase
import app.utils.ScriptModel as script_model
from app.forms import TrainForm
from app.models import TrainHistory, Asset
import os

@app.route('/')
def index():
    # formulaire d'entrainement
    form = TrainForm()

    # connection API fxcmpy
    con_fxcmpy = fxcmpy.fxcmpy(FXCMY_ACCESS_TOKEN_REAL, server='real')

    # list of instruments, generate choice for get data in view
    instruments = con_fxcmpy.get_instruments()
    list_models = TrainHistory.query.all()
    return render_template('index.html', instruments=instruments, trainform=form, list_models=list_models)


@app.route('/get-data-<instrument>', methods=['GET'])
def get_data(instrument):
    """
    Stock data for one instrument in csv
    :param instrument: name of instrument for research
    :return: json of data for instrument
    """
    # get asset or create
    asset = utilsDatabase.get_asset(instrument)

    # connection API fxcmpy
    con_fxcmpy = fxcmpy.fxcmpy(FXCMY_ACCESS_TOKEN, server='demo')

    # search params GET for get candle
    params_candle = request.args.to_dict()
    if request.args.get('number'):
        params_candle['number'] = int(params_candle['number'])

    # get data from api, use GET params
    data = con_fxcmpy.get_candles(instrument, **params_candle)
    data['asset_id'] = asset.id
    con_fxcmpy.close()

    data = utilsDatabase.actualize_data(data)

    # stock data in csv
    filename = 'bourse_' + instrument + '.csv'
    data.to_csv('app/data/' + filename)

    return data.to_json()


@app.route('/train-model', methods=['GET', 'POST'])
def train_model():
    """ entraîne le modèle sur les donnèes existantes
        effectue une sauvegarde du model
    """
    if request.method == 'POST':
        epochs = request.form['epochs']
        time_step = request.form['time_steps']
        batch_size = request.form['batch_size']

        # Entrainement du model
        script_model.train_model(epochs=int(epochs), batch_size=int(batch_size), time_steps=int(time_step))

        # Sauvegarde du model


        flash('Le modèle à bien été entraîné')
        return redirect(url_for('index'))
    return 'Vous ne devriez pas être là.. Passez par le formulaire !'


@app.route('/get-predict-<int:asset_id>-<int:model_id>')
def get_predict(asset_id, model_id):
    """ Prédiction du modèle """
    train_history = TrainHistory.query.get(model_id)
    asset = Asset.query.get(asset_id)
    # récupère toutes les données
    data = script_model.get_data_on_db()

    stock = script_model.make_prediction(data, train_history, asset)
    flash(f'Prédiction effectuées pour {stock.asset.name} le {stock.date} :\n ASK :\n\topen :{stock.askopen} close{stock.askclose} low:{stock.asklow} high:{stock.askhigh} \n BID :\n\topen :{stock.bidopen} close{stock.bidclose} low:{stock.bidlow} high:{stock.bidhigh}')
    return redirect(url_for('index'))


@app.route('/delete-model-<int:model_id>')
def delete(model_id):
    train_history = TrainHistory.query.get(model_id)
    db.session.delete(train_history)
    db.session.commit()
    os.remove('app/models/' + train_history.filename)
    flash(f"Nous avons exterminé le modèle n°{train_history.id} !")
    return redirect(url_for('index'))




@app.route('/bot')
def bot():
    con_fxcmpy = fxcmpy.fxcmpy(FXCMY_ACCESS_TOKEN, server='demo')

    data = con_fxcmpy.get_candles('GER30', period='H1', number=500)

    #con.get_open_positions().T

    model_id = 10
    asset_id = 1

    train_history = TrainHistory.query.get(model_id)
    asset = Asset.query.get(asset_id)

    cot = script_model.make_prediction(data, train_history, asset)

    askopen = cot.askopen
    askclose = cot.askclose
    bidopen = cot.bidopen
    bidclose = cot.bidclose

    askhigh = cot.askhigh
    asklow = cot.asklow
    bidhigh = cot.bidhigh
    bidlow = cot.bidlow


    # Pour passer un ordre d'achat ou vente
    if askclose > askopen:
        #con_fxcmpy.create_market_buy_order('GER30', 5)

        order = con.create_entry_order(symbol='GER30', is_buy=True,
                               amount=5000, limit=112,
                               is_in_pips = False,
                               time_in_force='GTC', rate=110,
                               stop=None, trailing_step=None)


    if askclose < askopen:
        #con_fxcmpy.create_market_sell_order('GER30', 5)
        order = con.create_entry_order(symbol='GER30', is_buy=False,
                               amount=5000, limit=112,
                               is_in_pips = False,
                               time_in_force='GTC', rate=110,
                               stop=None, trailing_step=None)

    return render_template('bot.html', cot=cot)
