from app import app
from flask import request, flash, redirect, url_for
from app.bot.botTrader import take_position
from app.utils.fxcmManager import connect_fxcm
import time
import datetime as dt


@app.route('/buy-sell', methods=['GET', 'POST'])
def buy_sell():
    if request.method == 'POST':
        model_id = request.form['model']
        position = take_position(model_id=model_id)
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
            minut_restant = minute_actual%60
            if minut_restant == 0:
                position = take_position()
                time.sleep(3600)
                tradeId = position['tradeId'][0]
                con_fxcmpy.close_all()
            else:
                sec_restant = (minut_restant)*60
                min_restant=3600-sec_restant
                position = take_position()
                time.sleep(min_restant)
                tradeId = position['tradeId'][0]
                con_fxcmpy.close_all()
            temps = temps-1
    return redirect(url_for('bot'))
