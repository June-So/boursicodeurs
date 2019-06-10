import app.utils.ScriptModel as script_model
from app.models import TrainHistory, Asset, BotAction
from app.utils.fxcmManager import connect_fxcm
from app.utils.utilsDatabase import save_action

from keras.models import Sequential
from keras.models import load_model
from keras.layers import Dense
from keras.optimizers import Adam

import numpy as np
import random
from collections import deque

class Agent:
    def __init__(self, state_size, is_eval=False, model_name=""):
        self.state_size = state_size # normalized previous days
        self.action_size = 3 # sit, buy, sell
        self.memory = deque(maxlen=2500)
        self.inventory = []
        self.model_name = model_name
        self.is_eval = is_eval
        self.portfolio = []

        self.gamma = 0.95
        self.epsilon = 1.0
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995

        self.model = load_model("app/bot/qTrader/models/weights/" + model_name) if is_eval else self._model()

    def _model(self):
        model = Sequential()
        model.add(Dense(units=64, input_dim=self.state_size, activation="relu"))
        model.add(Dense(units=32, activation="relu"))
        model.add(Dense(units=8, activation="relu"))
        model.add(Dense(self.action_size, activation="linear"))
        model.compile(loss="mse", optimizer=Adam(lr=0.001))

        return model

    def act(self, state):
        if not self.is_eval and np.random.rand() <= self.epsilon:
            return random.randrange(self.action_size)

        options = self.model.predict(state)
        return np.argmax(options[0])

    def expReplay(self, batch_size):
        mini_batch = []
        l = len(self.memory)
        for i in range(l - batch_size + 1, l):
            mini_batch.append(self.memory[i])

        for state, action, reward, next_state, done in mini_batch:
            target = reward
            if not done:
                target = reward + self.gamma * np.amax(self.model.predict(next_state)[0])

            target_f = self.model.predict(state)
            target_f[0][action] = target
            self.model.fit(state, target_f, epochs=1, verbose=0)

        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    def load(self, name):
        self.model.load_weights(name)

    def save(self, name):
        self.model.save_weights(name)

    def take_position(self, action, model_id=13, asset_id=1, period='H1'):
        STATE_BUY = 1
        STATE_SELL = 2
        STATE_NONE = 0
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
        if action == STATE_BUY:
            #order = con_fxcmpy.create_market_buy_order('GER30', 5)

            order = con_fxcmpy.open_trade(symbol=asset.name, is_buy=True,
                           is_in_pips=False,
                           amount='5', time_in_force='GTC',
                           order_type='AtMarket', stop=cot.asklow)
            save_action(STATE_BUY, cot)

        # Condition de ???
        if action == STATE_SELL:
            con_fxcmpy.open_trade(symbol=asset.name, is_buy=False,
                           is_in_pips=False,
                           amount='5', time_in_force='GTC',
                           order_type='AtMarket', stop=cot.bidhigh)
            save_action(STATE_SELL, cot)

        if action == STATE_NONE:
            save_action(STATE_NONE, cot)
        # -- SAVE DECISION


        open_position = con_fxcmpy.get_open_positions()

        return (open_position, cot)