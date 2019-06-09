from app import app
import app.utils.ScriptModel as script_model
from keras.models import load_model
from app.bot.qTrader.agent.agent import Agent
from app.bot.qTrader.functions import *
import time
from app.utils.fxcmManager import connect_fxcm

STATE_BUY = 1
STATE_SELL = 2
STATE_NONE = 3


def agent_playing(model_name, col="askclose"):

    model = load_model("app/bot/qTrader/models/" + model_name +"")
    window_size = model.layers[0].input.shape.as_list()[1]

    agent = Agent(window_size, True, model_name)
    data = getLastCotationVect("ger30", "h1", col)
    #batch_size = 32


    state = getState(data, window_size - 1, window_size + 1)
    total_profit = 0
    agent.inventory = []

    action = agent.act(state)

    reward = 0

    minute_actual = dt.datetime.now().time().minute
    minute_remain = minute_actual % 60
    con_fxcmpy = connect_fxcm()

    if minute_remain == 0:
        agent.take_position(action)
        time.sleep(3600)
        con_fxcmpy.close_all()

    else:
        sec_remain = (minute_remain) * 60
        minute_remain = 3600 - sec_remain

        agent.take_position(action)
        time.sleep(minute_remain)
        con_fxcmpy.close_all()

    data = getLastCotationVect("ger30", "h1", col)

    if action == 1:  # buy
        reward = max(data[-1] - data[-2], 0)
        agent.portfolio += data[-1] - data[-2]

    if action == 2:  # sell
        reward = max(-(data[-1] - data[-2]), 0)
        agent.portfolio.append(data[-1] - data[-2])

    next_state = getState(data, window_size - 1, window_size + 1)

    agent.memory.append((state, action, reward, next_state))