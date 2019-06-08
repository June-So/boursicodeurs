import keras
from keras.models import load_model

from agent.agent import Agent
from functions import *
import sys

if len(sys.argv) != 3:
    print("Usage: python evaluate.py [stock] [model]")
    exit()

stock_name, model_name = sys.argv[1], sys.argv[2]
model = load_model("models/" + model_name)
window_size = model.layers[0].input.shape.as_list()[1]

agent = Agent(window_size, True, model_name)
data = getStockDataVec(stock_name)
l = len(data) - 1
batch_size = 32

state = getState(data, 0, window_size + 1)
total_profit = 0
agent.inventory = []

for t in range(l):
        action = agent.act(state)

        # sit
        next_state = getState(data, t + 1, window_size + 1)
        reward = 0
        
        if action == 1: # buy
            agent.inventory.append(data[t])
            
            #--------
            bought_price = agent.inventory.pop(0)
            reward = max(data[t+1] - data[t],0)
            #--------
            total_profit += (data[t+1] - data[t])
            #print("Buy: " + formatPrice(data[t]) + " | Profit: " + formatPrice(data[t+1] - bought_price))

        if action == 2: # sell
            #--------
            agent.inventory.append(data[t])
            sold_price = agent.inventory.pop(0)
            reward = max(-(data[t+1] - sold_price),0)
            #--------
#             bought_price = agent.inventory.pop(0)
#             reward = max(data[t] - bought_price, 0)
            total_profit += -(data[t+1] - sold_price)
            #print("Sell: " + formatPrice(data[t]) + " | Profit: " + formatPrice(data[t+1] - sold_price))
        print("--------------------------------")
        print("Gain/perte temp: " + formatPrice(total_profit))
        print("--------------------------------")
        done = True if t == l - 1 else False
        agent.memory.append((state, action, reward, next_state, done))
        state = next_state

        if done:
            print("--------------------------------")
            print("Total Profit Final: " + formatPrice(total_profit))
            print("--------------------------------")
