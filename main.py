import gymnasium as gym

env=gym.make("gymnasium_env/CSE368-BlackJack-v0")

observation, info= env.reset()

done=False
while not done:
    action=env.action_space.sample()
    observation, reward, done, _, info = env.step(action)
    print (f"Action: {action}, Reward: {reward}, Done: {done}")

env.close()
