from app import app
from flask import render_template
from app.forms import TrainForm, BotForm
from app.models import TrainHistory, StockHistory, StockPrediction, Asset
from app.utils.fxcmManager import connect_fxcm

import matplotlib.pyplot as plt


@app.route('/')
def index():
    # formulaire d'entrainement
    form = TrainForm()
    list_models = TrainHistory.query.all()
    return render_template('index.html',  trainform=form, list_models=list_models)


@app.route('/stock-history')
def stock_history():
    stock_history = StockHistory.query.all()
    stock_predictions = StockPrediction.query.all()
    limit = 100
    data = stock_history[-50:]
    plt.figure()

    dates_real = [stock.date for stock in data]
    y_real = [stock.askclose for stock in data]
    plt.plot(dates_real,  y_real, label='real')

    models = [ predict.train_history.id  for predict in stock_predictions]
    models_ids = list(dict.fromkeys(models))

    for model_id in models_ids:
        dates_predict = [stock.date for stock in stock_predictions if stock.train_history.id == model_id]
        y_predict = [stock.bidclose for stock in stock_predictions if stock.train_history.id == model_id]
        plt.plot(dates_predict, y_predict, label='prediction_'+str(model_id))

    plt.legend()
    plt.savefig('app/static/img/stock-history.png')

    return render_template('stock-history.html', predictions=stock_predictions)


@app.route('/bot')
def bot():
    form = BotForm()
    models = TrainHistory.query.all()
    return render_template('bot.html', botform=form, models=models)


@app.route('/liste-indices')
def list_instrument():
    # connection API fxcmpy
    con_fxcmpy = connect_fxcm()
    assets = Asset.query.all()
    # list of instruments, generate choice for get data in view
    instruments = con_fxcmpy.get_instruments()
    return render_template('list-instrument.html', instruments=instruments, assets=assets)

