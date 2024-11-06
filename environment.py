import gymnasium as gym
from gymnasium.wrappers import FlattenObservation

import game

"""
An environment for the blackjack game using OpenAI Gymnasium
"""


class Environment(gym.Env):

    def __init__(self, deck: list[tuple[str, str]], game: game.Game):
        self.deck = deck
        self.game = game

        # What the agent is aware of
        self.observation_space = gym.spaces.Dict(
            {
                "score": gym.spaces.Discrete(1),
                "dealer score": gym.spaces.Discrete(1),
                "soft ace": gym.spaces.Discrete(1),
                "count": gym.spaces.Discrete(1),
            }
        )

        # The action space is the set of actions that
        self.action_space = gym.spaces.Discrete(3)
        self._action_to_decision: dict[int, str] = {0: "S", 1: "H", 2: "D"}

    # I don't know if this is even necessary
    def _get_obs(self):
        raise NotImplementedError

    def reset(self, seed = None, options = None):
        super().reset(seed=seed)
        raise NotImplementedError

    def step(self, action: int, bet: int = 0):
        actionStr = self._action_to_decision[action]

        if actionStr == "H":
            pass
        # copied from game class

        # soft_ace = 1 if (*, "Ace") in self.game.player.hand else 0

        observation = {
            "score": self.game.player.currentScore,
            "dealer score": self.game.dealer.currentScore,
            "soft ace": 1 if self.game.player.soft_ace else 0,
            "count": self.game.count
		}
        
		#reward, terminated, truncated, info

        raise NotImplementedError
