from app import app
from flask import render_template
import app.utils.ScriptModel as script_model
from app.models import TrainHistory, Asset
from app.utils.fxcmManager import connect_fxcm


@app.route('/buy-sell')
def buy_sell():

    position = trader.take_position()

    return redirect(url_for('bot'))
