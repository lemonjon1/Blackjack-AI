import gymnasium as gym
import numpy as np
import game
from environment import Environment
from stable_baselines3 import PPO, A2C
import matplotlib.pyplot as plt

def create_blackjack():
    suits = ["Spades", "Clubs", "Diamonds", "Hearts"]
    values = ["Ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King"]
    deck = [(value, suit) for suit in suits for value in values]
    agent = game.Player()
    newGame = game.Game(agent)
    return Environment(deck, newGame)

gym.register(
    id="gymnasium_env/CSE368-BlackJack-v0",
    entry_point = create_blackjack,
)

env = gym.make("gymnasium_env/CSE368-BlackJack-v0")

agent = "A2C"
policy = "MultiInputPolicy"

model = A2C(policy, env, verbose=1)
model.learn(total_timesteps=50_000)
# model.save(f"{agent}_{policy}")
del model

# for i in range(100_000):
#     observation, info = env.reset()
#     done = False
#     while not done:
#         action = env.action_space.sample()
#         observation, reward, done, truncated, info = env.step(action)
#     # print (f"Action: {action}, Reward: {reward}, Done: {done}")

average = []
sum = 0
num = len(game.money) / 100
for i in range(len(game.money)):
    sum += game.money[i]
    if i%100 == 0:
        average.append(sum/100)
        sum = 0

plt.plot(list(range(len(average))), average)
plt.show()

env.close()
