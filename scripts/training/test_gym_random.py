import time
import gymnasium as gym
from gymnasium.envs.registration import register

register(
    id='URenv-v0',
    entry_point='URenv:URenv',
)

env = gym.make('URenv-v0')

observation, info = env.reset()

episode_over = False
while not episode_over:
    action = env.action_space.sample()  # agent policy that uses the observation and info
    observation, reward, terminated, truncated, info = env.step(action)
    print(reward)
    time.sleep(0.5)

