from app import app
from flask import render_template
import app.utils.ScriptModel as script_model
from app.models import TrainHistory, Asset
from app.utils.fxcmManager import connect_fxcm

@app.route('/bot')
def bot():
    con_fxcmpy = connect_fxcm()

    data = con_fxcmpy.get_candles('GER30', period='H1', number=500)

    #con.get_open_positions().T

    model_id = 10
    asset_id = 1

    train_history = TrainHistory.query.get(model_id)
    asset = Asset.query.get(asset_id)

    cot = script_model.make_prediction(data, train_history, asset)

    askopen = cot.askopen
    askclose = cot.askclose
    bidopen = cot.bidopen
    bidclose = cot.bidclose

    askhigh = cot.askhigh
    asklow = cot.asklow
    bidhigh = cot.bidhigh
    bidlow = cot.bidlow


    # Pour passer un ordre d'achat ou vente
    if askclose > askopen:
        #con_fxcmpy.create_market_buy_order('GER30', 5)

        order = con_fxcmpy.create_entry_order(symbol='GER30', is_buy=True,
                               amount=5000, limit=112,
                               is_in_pips = False,
                               time_in_force='GTC', rate=110,
                               stop=None, trailing_step=None)


    if askclose < askopen:
        #con_fxcmpy.create_market_sell_order('GER30', 5)
        order = con_fxcmpy.create_entry_order(symbol='GER30', is_buy=False,
                               amount=5000, limit=112,
                               is_in_pips = False,
                               time_in_force='GTC', rate=110,
                               stop=None, trailing_step=None)

    return render_template('bot.html', cot=cot)
