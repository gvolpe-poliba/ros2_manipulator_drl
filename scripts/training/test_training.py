import sys
import gymnasium as gym
import numpy as np
import logging
from gymnasium.envs.registration import register
from stable_baselines3.sac.policies import MlpPolicy
from stable_baselines3 import SAC

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

register(
    id='URenv-v0',
    entry_point='URenv:URenv',
)

env = gym.make('URenv-v0')

model = SAC(MlpPolicy, env, verbose=1,  tensorboard_log="./ur3_tensorboard/")

model.learn(total_timesteps=1000*1000, log_interval=1)

model.save("sac_manipulator_pose")

env.close()

