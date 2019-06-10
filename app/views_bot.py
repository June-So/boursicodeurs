from app import app
from flask import request, flash, redirect, url_for
from app.bot.botTrader import take_position
from app.bot.qTrader.realtime import agent_playing
from app.utils.fxcmManager import connect_fxcm
from app.bot.qTrader.agent.agent import Agent
from keras.models import load_model
from app.models import BotAction
from keras import backend as K
import time
import datetime as dt
import pickle

timestamp = time.strftime('%Y%m%d%H%M')

@app.route('/buy-sell', methods=['GET', 'POST'])
def buy_sell():
    if request.method == 'POST':
        model_id = request.form['model']
        position = take_position(model_id=model_id)

    flash(f"recap des positions ouvertes {position}")
    return redirect(url_for('bot'))


@app.route('/free-trader', methods=['GET', 'POST'])
def free_trader():
    con_fxcmpy = connect_fxcm()

    if request.method == 'POST':
        time_trade = request.form['time_trade']
        model_id = request.form['model']
        time_trade = int(time_trade)

        while time_trade > 0:
            minute_actual = dt.datetime.now().time().minute
            minute_remain = minute_actual % 60

            if minute_remain == 0:
                position = take_position(model_id=model_id)
                time.sleep(3600)
                #tradeId = position['tradeId'][0]
                #con_fxcmpy.close_all()
            else:
                sec_remain = (minute_remain) * 60
                minute_remain = 3600-sec_remain
                position = take_position(model_id=model_id)
                time.sleep(minute_remain)
                #tradeId = position['tradeId'][0]
                #con_fxcmpy.close_all()
            time_trade = time_trade-1
    return redirect(url_for('bot'))


@app.route('/dql-trader', methods = ["POST", "GET"])
def dql_trader():
    if request.method == 'POST':
        time_trade = request.form['time_trade']
        model_name = request.form['model_name']
        time_horizon = request.form['time_horizon']
        time_trade = int(time_trade)

        #model = load_model("app/bot/qTrader/models/weights/" + model_name)
        #window_size = model.layers[0].input.shape.as_list()[1]
        #agent = Agent(window_size, True, model_name)

        portfolio = []
        memo_recap = []
        open_position_recap = []
        lstm_prediction = []

        while time_trade > 0 :

            portf, memo, open_pos, cot_lstm = agent_playing(model_name, time_horizon)
            portfolio.append(portf)
            memo_recap.append(memo)
            open_position_recap.append(open_pos)
            lstm_prediction.append(cot_lstm)

            time_trade -= 1


        with open('app/bot/qTrader/portfolio/wallet_at_{}.p'.format(timestamp), 'wb') as fp:
            pickle.dump(portfolio, fp)

        with open('app/bot/qTrader/portfolio/memory_at_{}.p'.format(timestamp), 'wb') as fm:
            pickle.dump(memo_recap, fm)

        with open('app/bot/qTrader/portfolio/open_position_at_{}.p'.format(timestamp), 'wb') as fo:
            pickle.dump(open_position_recap, fo)

        with open('app/bot/qTrader/portfolio/lstm_prediction_at_{}.p'.format(timestamp), 'wb') as fl:
            pickle.dump(lstm_prediction, fl)

    return redirect(url_for('bot'))
