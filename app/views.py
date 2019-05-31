from app import app
from flask import render_template
from app.forms import TrainForm, BotForm
from app.models import TrainHistory, StockHistory, StockPrediction, Asset
from app.utils.fxcmManager import connect_fxcm

import  matplotlib.pyplot as plt

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
    print('hellllllo')
    limit = 100
    data = stock_history[-24:]
    dates_real = [stock.date for stock in data]
    dates_predict = [stock.date for stock in stock_predictions]
    askopen_real = [stock.askopen for stock in data]
    askopen_predict = [stock.askopen for stock in stock_predictions]
    plt.plot(dates_real, askopen_real)
    plt.plot(dates_predict, askopen_predict, c='red')
    plt.savefig('app/static/img/stock-history.png')

    return render_template('stock-history.html')


@app.route('/bot')
def bot():
    form = BotForm()
    return render_template('bot.html', botform=form)


@app.route('/liste-indices')
def list_instrument():
    # connection API fxcmpy
    con_fxcmpy = connect_fxcm()
    assets = Asset.query.all()
    # list of instruments, generate choice for get data in view
    instruments = con_fxcmpy.get_instruments()
    return render_template('list-instrument.html', instruments=instruments, assets=assets)

