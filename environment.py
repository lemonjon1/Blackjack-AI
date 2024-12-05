from typing import Optional
import gymnasium as gym
import numpy as np
from gymnasium.wrappers import FlattenObservation
import random

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
                "score": gym.spaces.Discrete(35), #Set to 32 incase someone decides to hit on 21
                "dealer score": gym.spaces.Discrete(35),
                "soft ace": gym.spaces.Discrete(2), #Soft ace can be a 0 or a 1
                "count": gym.spaces.Discrete(201), #Count can be anywhere between -100 through +100
                "money": gym.spaces.Box(low=0, high=np.inf, shape=(1,), dtype=np.float32),  # Player's remaining money
            }
        )

        # The action space is the set of actions that
        self.action_space = gym.spaces.Discrete(3)
        self._action_to_decision: dict[int, str] = {0: "S", 1: "H", 2: "D"}

    def _get_obs(self) -> dict:
        return {
            "score": int(self.game.player.currentScore),  # Convert to int otherwise it yells at you
            "dealer score": int(self.game.dealer.currentScore),
            "soft ace": 1 if self.game.player.soft_ace else 0,
            "count": int(self.game.count) + 100, #Observation space is 0-200, but we want to simulate -100 to 100
            "money": np.array([self.game.player.money], dtype=np.float32)  # Player's remaining money
        }

    def reset(self, seed: Optional[int] = None, options: Optional[dict] = None) -> tuple:
        super().reset(seed=seed)
        # self.game = game.Game(game.Player)
        # self.game.player.bet = 0.0
        # self.game.player.money = 1000.0
        # self.game.player.soft_ace = False
        self.game.is_over = False
        self.game.player.hand = []
        self.game.player.currentScore = 0
        self.game.player.soft_ace = False

        self.game.dealer.hand = []
        self.game.dealer.currentScore = 0

        self.game.dealHand(self.game.player)
        self.game.dealHand(self.game.dealer)

        # Return both observation and an empty info dictionary
        return self._get_obs(), {}


    def step(self, action: int, bet: int = 50):

        if len(self.game.gameDeck) <= 10:
            self.game.gameDeck = [(value, suit) for suit in game.suits for value in game.values for deck in range(game.numDecks)]
            random.shuffle(self.game.gameDeck)
            self.game.count = 0

        actionStr = self._action_to_decision[action]
        self.game.player.bet = bet
        if actionStr == "H":
            self.game.hit(self.game.player)
        elif actionStr == "D":
            self.game.doubleDown(self.game.player)
        elif actionStr == "S":
            self.game.is_over = True

        reward = 0
        if self.game.is_over:
            self.game.dealerAction()
            reward = self.game.player.bet if self.game.player.currentScore > self.game.dealer.currentScore and self.game.player.currentScore <= 21 else -1 * self.game.player.bet
            self.game.player.money += reward

        game.money.append(self.game.player.money)
        # game.money.append(reward)
        observation = self._get_obs()

        return observation, reward, self.game.is_over, False, {}
