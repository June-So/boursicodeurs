from app import app
from flask import request, flash, redirect, url_for
from app.bot.botTrader import take_position
from app.bot.qTrader.realtime import agent_playing
from app.utils.fxcmManager import connect_fxcm
from app.models import BotAction
import time
import datetime as dt


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
        time_trade = int(time_trade)
        while time_trade > 0 :
            agent_playing(model_name=model_name)
            time_trade -= 1

    return redirect(url_for('bot'))
