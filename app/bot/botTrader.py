import app.utils.ScriptModel as script_model
from app.models import TrainHistory, Asset, BotAction
from app.utils.fxcmManager import connect_fxcm
from app.utils.utilsDatabase import  save_action

STATE_BUY = 1
STATE_SELL = 2
STATE_NONE = 3


def take_position(model_id=17, asset_id=1, period='H1'):
    """
    :param model_id:  id du model à utiliser
    :param asset_id:  id de l'indice sur lequel se placer
    :param period:
    :return:
    """
    # -- GET DATA ---- Récupérer les dernières données
    con_fxcmpy = connect_fxcm()
    train_history = TrainHistory.query.get(model_id)
    asset = Asset.query.get(asset_id)
    data = con_fxcmpy.get_candles(asset.name, period=period, number=1000)

    # -- MAKE PREDICTION -----
    #con_fxcmpy.get_open_positions().
    cot = script_model.make_prediction(data, train_history, asset)

    # -- MAKE DECISION (from prediction) ---------
    # Condition d'ordre d'achat, revente automatique selon limite
    if cot.bidclose > cot.bidopen:
        #order = con_fxcmpy.create_market_buy_order('GER30', 5)

        order = con_fxcmpy.open_trade(symbol=asset.name, is_buy=True,
                       is_in_pips=False,
                       amount='5', time_in_force='GTC',
                       order_type='AtMarket', limit=cot.askhigh, stop=cot.asklow)
        save_action(STATE_BUY, cot)

    # Condition de ???
    if cot.bidclose < cot.bidopen:
        #order = con_fxcmpy.create_market_sell_order('GER30', 5)

        order = con_fxcmpy.open_trade(symbol=asset.name, is_buy=False,
                       is_in_pips=False,
                       amount='5', time_in_force='GTC',
                       order_type='AtMarket', limit=cot.bidlow, stop=cot.bidhigh)
        save_action(STATE_NONE, cot)

    # -- SAVE DECISION


    open_position = con_fxcmpy.get_open_positions()
    print(order)
    print(open_position)

    return open_position


def take_position_free(time):
    time = int(time)
    while time > 0:
        rep = print("j'ai passé ",time,"position")
        time = time - 1
    return rep
