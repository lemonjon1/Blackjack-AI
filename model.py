import gymnasium as gym
import numpy as np

class Agent:
	def __init__(self, env: gym.Env, ):
		self.env = env

	def get_action(self) -> int:
		return np.random.choice(3)
	
	def update(self) -> None:
		raise NotImplementedError


env = gym.make("Blackjack-v1")
agent = Agent(env)
print(agent.get_action())
