from app import app
import app.utils.ScriptModel as script_model
from keras.models import load_model
from app.bot.qTrader.agent.agent import Agent
import pickle
#from app.bot.qTrader.agent import Agent

from keras import backend as K
from app.bot.qTrader.functions import *
import time
import datetime as dt
from app.utils.fxcmManager import connect_fxcm


STATE_BUY = 1
STATE_SELL = 2
STATE_NONE = 3


def agent_playing(model_name,time_horizon, col="askclose"):

    model = load_model("app/bot/qTrader/models/weights/" + model_name)

    window_size = model.layers[0].input.shape.as_list()[1]

    period = time_horizon

    agent = Agent(window_size, True, model_name)

    data = getLastCotationVect("ger30", period, window_size, col)
    #batch_size = 32


    state = getState(data, window_size - 1, window_size + 1)
    total_profit = 0
    agent.inventory = []

    action = agent.act(state)

    reward = 0

    minute_actual = dt.datetime.now().time().minute
    minute_remain = minute_actual % 5
    con_fxcmpy = connect_fxcm()

    if minute_remain == 0:
        open_pos, cot_lstm = agent.take_position(action)
        time.sleep(300)
        con_fxcmpy.close_all()

    else:
        sec_remain = (minute_remain) * 60
        minute_remain = 300 - sec_remain

        open_pos, cot_lstm = agent.take_position(action)
        time.sleep(minute_remain)
        con_fxcmpy.close_all()

    data = getLastCotationVect("ger30", period, window_size, col)

    if action == 1:  # buy
        reward = max(data[-1] - data[-2], 0)
        agent.portfolio.append(data[-1] - data[-2])

    if action == 2:  # sell
        reward = max(-(data[-1] - data[-2]), 0)
        agent.portfolio.append(data[-1] - data[-2])

    next_state = getState(data, window_size - 1, window_size + 1)

    agent.memory.append((state, action, reward, next_state))

    return (agent.portfolio, agent.memory, open_pos, cot_lstm)

