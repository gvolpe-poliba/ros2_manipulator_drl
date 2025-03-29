# https://stable-baselines3.readthedocs.io/en/master/modules/dqn.html

import gymnasium as gym

from stable_baselines3 import DQN

env = gym.make("CartPole-v1", render_mode="human")

model = DQN("MlpPolicy", env, verbose=1, tensorboard_log="./dqn_tensorboard/")
model.learn(total_timesteps=10000, log_interval=2)
model.save("dqn_cartpole")

del model # remove to demonstrate saving and loading

print("End Training")

model = DQN.load("dqn_cartpole")

obs, info = env.reset()
while True:
    action, _states = model.predict(obs, deterministic=True)
    obs, reward, terminated, truncated, info = env.step(action)
    if terminated or truncated:
        obs, info = env.reset()