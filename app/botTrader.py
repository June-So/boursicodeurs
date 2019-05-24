from SECRET import *
import app.utils.ScriptModel as script_model
import fxcmpy

con_fxcmpy = fxcmpy.fxcmpy(FXCMY_ACCESS_TOKEN, server='demo')

data = con_fxcmpy.get_candles('GER30', period='H1', number=1000)

#con.get_open_positions().T

model_id = 1
asset_id = 1

train_history = TrainHistory.query.get(model_id)
asset = Asset.query.get(asset_id)

cot = make_prediction(data, train_history, asset)
open = cot.askopen
clse = cot.askclose

if close > open:
    con_fxcmpy.create_market_buy_order('GER30', 100)
elif close == open:
    pass
else con_fxcmpy.create_market_sell_order('GER30', 100)

print(cot)
