from app import app
from flask import render_template
from app.forms import TrainForm, BotForm, BotDqlForm
from app.models import TrainHistory, StockHistory, StockPrediction, Asset, BotAction
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
    limit = -20
    plt.figure()

    # plot history
    stock_history = StockHistory.query.order_by(StockHistory.date.asc()).all()
    dates_real = [stock.date for stock in stock_history]
    y_real = [stock.askclose for stock in stock_history]
    plt.plot(dates_real,  y_real, label='real')

    # plot predictions par model
    stock_predictions = StockPrediction.query.order_by(StockPrediction.date.asc()).all()
    models = [ predict.train_history.id for predict in stock_predictions ]
    models_ids = list(dict.fromkeys(models))
    for model_id in models_ids:
        dates_predict = [stock.date for stock in stock_predictions if stock.train_history.id == model_id]
        y_predict = [stock.bidclose for stock in stock_predictions if stock.train_history.id == model_id]
        plt.plot(dates_predict, y_predict,  label='prediction_' + str(model_id))

    # plot des actions
    bot_actions = BotAction.query.order_by(BotAction.date.asc()).all()
    x = [action.date for action in bot_actions]
    x_format = [action.date.strftime('%d/%m/%Y %H') for action in bot_actions]
    y = [history.askclose for history in stock_history if history.date.strftime('%d/%m/%Y %H') in x_format] #[ action.predictions[0].bidclose for action in bot_actions ]
    print(x_format)
    print([history for history in stock_history if history.date.strftime('%d/%m/%Y %H') in x_format])
    print(len(x), len(y))
    #plt.scatter(x, y)

    #plt.legend()
    #plt.savefig('app/static/img/stock-history.png')

    return render_template('stock-history.html', predictions=stock_predictions)


@app.route('/bot')
def bot():
    form = BotForm()
    formdql = BotDqlForm()
    models = TrainHistory.query.all()
    bot_actions = BotAction.query.all()
    return render_template('bot.html', botform=form, BotDqlForm=formdql, models=models, bot_actions=bot_actions)


@app.route('/liste-indices')
def list_instrument():
    # connection API fxcmpy
    assets = Asset.query.all()
    # list of instruments, generate choice for get data in view
    return render_template('list-instrument.html', assets=assets)

