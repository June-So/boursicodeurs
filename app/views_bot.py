from app import app
from flask import render_template
from flask import request, flash, redirect, url_for
import app.utils.ScriptModel as script_model
from app.models import TrainHistory, Asset
from app.utils.fxcmManager import connect_fxcm
from app.bot.botTrader import take_position


@app.route('/buy-sell')
def buy_sell():

    position = take_position()
    flash(f"recap des positions ouvertes {position}")
    return redirect(url_for('bot'))
