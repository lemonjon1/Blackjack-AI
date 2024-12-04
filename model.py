import gymnasium as gym
import numpy as np

from environment import Environment


gym.register(
    id="gymnasium_env/BlackJack-v0",
    entry_point=Environment,
)
