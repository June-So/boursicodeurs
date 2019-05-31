from app import app
from flask import request, flash, redirect, url_for
from app.bot.botTrader import take_position
import time


@app.route('/buy-sell')
def buy_sell():
    position = take_position()
    flash(f"recap des positions ouvertes {position}")
    return redirect(url_for('bot'))

@app.route('/free-trader',methods=['GET', 'POST'])
def free_trader():
    if request.method == 'POST':
        temps = request.form['time_trade']
        temps = int(temps)
        while temps > 0:
            position = take_position()
            #print("j'ai passé ",temps,"position")
            time.sleep(300)
            temps = temps - 1
    return redirect(url_for('bot'))
