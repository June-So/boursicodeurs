from SECRET import *
import app.utils.ScriptModel as script_model
import fxcmpy
from app.forms import TrainForm
from app.models import TrainHistory, Asset
from app.utils.fxcmManager import connect_fxcm

def take_position():
    con_fxcmpy = connect_fxcm()

    data = con_fxcmpy.get_candles('GER30', period='H1', number=1000)

    #con_fxcmpy.get_open_positions().T

    model_id = 13
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
        #order = con_fxcmpy.create_market_buy_order('GER30', 5)

        order = con_fxcmpy.open_trade(symbol='GER30', is_buy=True,
                       is_in_pips=False,
                       amount='5', time_in_force='GTC',
                       order_type='AtMarket', limit=1.001*askhigh)

    if bidclose < bidopen:
        #order = con_fxcmpy.create_market_sell_order('GER30', 5)

        order = con_fxcmpy.open_trade(symbol='GER30', is_buy=False,
                       is_in_pips=False,
                       amount='5', time_in_force='GTC',
                       order_type='AtMarket', limit=bidlow)

    open_position = con_fxcmpy.get_open_positions()

    return open_position
