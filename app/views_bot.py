from app import app
from flask import render_template
from flask import request, flash, redirect, url_for
import app.utils.ScriptModel as script_model
from app.models import TrainHistory, Asset
from app.utils.fxcmManager import connect_fxcm
from app.bot.botTrader import take_position, take_position_free
from app.forms import TrainForm, BotForm
import time
import datetime as dt


@app.route('/buy-sell')
def buy_sell():

    position = take_position()
    flash(f"recap des positions ouvertes {position}")
    return redirect(url_for('bot'))

@app.route('/free-trader',methods=['GET', 'POST'])
def free_trader():
    con_fxcmpy = connect_fxcm()
    if request.method == 'POST':
        temps = request.form['time_trade']
        temps = int(temps)
        while temps > 0:
            minute_actual = dt.datetime.now().time().minute
            minut_restant = minute_actual%5
            if minut_restant == 0:
                position = take_position()
                time.sleep(300)
                tradeId = position['tradeId'][0]
                con_fxcmpy.close_all()
            else:
                sec_restant = (minut_restant)*60
                min_restant=300-sec_restant
                position = take_position()
                time.sleep(min_restant)
                tradeId = position['tradeId'][0]
                con_fxcmpy.close_all()
            temps = temps-1
    return redirect(url_for('bot'))
