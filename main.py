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
    newGame = game.Game()
    return Environment(deck, newGame)

gym.register(
    id="gymnasium_env/CSE368-BlackJack-v0",
    entry_point = create_blackjack,
)

env = gym.make("gymnasium_env/CSE368-BlackJack-v0")

agent = "A2C"
policy = "MultiInputPolicy"

model = A2C(policy, env, verbose=1)
model.learn(total_timesteps=10_000)
# model.save(f"{agent}_{policy}")
del model


average = []
sum = 0
for i in range(len(game.rewardList)):
    sum += game.rewardList[i]
    if i%100 == 0:
        average.append(sum/100)
        sum = 0

plt.plot(list(range(len(average))), average)
z = np.polyfit(list(range(len(average))), average, 1)
p = np.poly1d(z)
slope = z[0]
plt.plot(list(range(len(average))), p(list(range(len(average)))), label=f"Trendline (slope={slope:.2f})")
plt.legend()
plt.show()

env.close()
