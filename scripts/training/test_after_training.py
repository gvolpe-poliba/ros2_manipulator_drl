import time
import sys
import gymnasium as gym
import numpy as np
import logging
from gymnasium.envs.registration import register
from stable_baselines3 import SAC

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

register(
    id='URenv-v0',
    entry_point='URenv:URenv',
)

env = gym.make('URenv-v0')

model = SAC.load("sac_manipulator_pose")

obs, info = env.reset()
for i in range(1000):
    action, _states = model.predict(obs)
    logging.getLogger(__name__).info('Step: "%s"' % i)
    obs, reward, terminated, truncated, info = env.step(action)
    time.sleep(0.5)

env.close()

