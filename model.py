import gymnasium as gym
import numpy as np
import game
from environment import Environment

def create_blacckjack():
    deck= []
    agent=game.Player()
    return Environment(deck, agent)

gym.register(
    id="gymnasium_env/CSE368-BlackJack-v0",
    entry_point=create_blacckjack,
)
