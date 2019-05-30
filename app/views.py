from app import app
from flask import render_template
from app.forms import TrainForm
from app.models import TrainHistory
from app.utils.fxcmManager import connect_fxcm


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
    print('hellllllo')
    return render_template('stock-history.html')


@app.route('/bot')
def bot():

    return render_template('bot.html')
