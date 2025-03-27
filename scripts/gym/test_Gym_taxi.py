import gymnasium as gym
import numpy as np
import random
import time 

# create Taxi environment
env = gym.make('Taxi-v3', render_mode="human")

# create a new instance of taxi, and get the initial state
state = env.reset()

num_steps = 99
for s in range(num_steps+1):
    print(f"step: {s} out of {num_steps}")

    # sample a random action from the list of available actions
    action = env.action_space.sample()

    # perform this action on the environment
    observation, reward, terminated, truncated, info = env.step(action)
    print(observation)
    print(reward)

    # print the new state
    env.render()

    time.sleep(0.5)

# end this instance of the taxi environment
env.close()