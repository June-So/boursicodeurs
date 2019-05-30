from app import app
from flask import render_template, url_for
from app.forms import TrainForm
from app.models import TrainHistory, StockHistory, StockPrediction
from app.utils.fxcmManager import connect_fxcm

import  matplotlib.pyplot as plt

@app.route('/')
def index():
    # formulaire d'entrainement
    form = TrainForm()

    # connection API fxcmpy
    con_fxcmpy = connect_fxcm()

    # list of instruments, generate choice for get data in view
    instruments = con_fxcmpy.get_instruments()
    list_models = TrainHistory.query.all()
    return render_template('index.html', instruments=instruments, trainform=form, list_models=list_models)

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