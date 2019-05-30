from SECRET import *
import app.utils.ScriptModel as script_model
import fxcmpy
from app.forms import TrainForm
from app.models import TrainHistory, Asset

def take_position():
    con_fxcmpy = fxcmpy.fxcmpy(FXCMY_ACCESS_TOKEN, server='demo')

    data = con_fxcmpy.get_candles('GER30', period='H1', number=1000)

    #con.get_open_positions().T

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
        order = con_fxcmpy.create_market_buy_order('GER30', 5)
        #order = con_fxcmpy.get_order(order_id)
        #order.set_stop_rate(111, is_in_pips=False)

        #con_fxcmpy.create_entry_order(symbol='GER30', is_buy=True,
        #                       amount=5000, limit=112,
        #                       is_in_pips = False,
        #                       time_in_force='GTC', rate=110,
        #                       stop=None, trailing_step=None)

        #con_fxcmpy.open_trade(symbol='GER30', is_buy=True,
        #               rate=105, is_in_pips=False,
        #               amount='1000', time_in_force='GTC',
        #               order_type='AtMarket', limit=120)


    if askclose < askopen:
        order = con_fxcmpy.create_market_sell_order('GER30', 5)
        #order = con_fxcmpy.get_order(order_id)
        #order.set_stop_rate(111, is_in_pips=False)
        #con_fxcmpy.create_entry_order(symbol='GER30', is_buy=False,
        #                       amount=5000, limit=112,
        #                       is_in_pips = False,
        #                       time_in_force='GTC', rate=110,
        #                       stop=None, trailing_step=None)

        #con_fxcmpy.open_trade(symbol='GER30', is_buy=False,
        #               rate=105, is_in_pips=False,
        #               amount='1000', time_in_force='GTC',
        #               order_type='AtMarket', limit=120)
    order_ids = con_fxcmpy.get_order_ids()
    #order_id = order_ids[-1]
    return order_ids

def set_limit_stop():
    con_fxcmpy = fxcmpy.fxcmpy(FXCMY_ACCESS_TOKEN, server='demo')
    #order_ids = con_fxcmpy.get_order_ids()
    order_ids = con_fxcmpy.orders
    return order_ids
