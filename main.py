import gymnasium as gym
import numpy as np
import game
from environment import Environment

def create_blackjack():
    suits = ["Spades", "Clubs", "Diamonds", "Hearts"]
    values = ["Ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King"]
    deck = [(value, suit) for suit in suits for value in values]
    agent = game.Player()
    return Environment(deck, agent)

gym.register(
    id="gymnasium_env/CSE368-BlackJack-v0",
    entry_point = create_blackjack,
)

env = gym.make("gymnasium_env/CSE368-BlackJack-v0")

observation, info = env.reset()

done = False
while not done:
    action = env.action_space.sample()
    observation, reward, done, truncated, info = env.step(action)
    print (f"Action: {action}, Reward: {reward}, Done: {done}")

print(f"Reset return length: {len(env.reset())}")  # Should be 2
print(f"Step return length: {len(env.step(action))}")  # Should be 5
env.close()
