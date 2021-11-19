from ray.rllib.env.multi_agent_env import MultiAgentEnv
import random
import gym
import numpy as np


class TestGrid(MultiAgentEnv):
    def __init__(self):
        self.num_agents = 20
        self.observation_space = gym.spaces.MultiDiscrete([20, 20])
        self.action_space = gym.spaces.Discrete(4)
        self.iterations = 50
        self.fruit_ripening_time = 150
        self.fruit_grid = [[random.randint(0, self.fruit_ripening_time) for c in range(20)] for r in range(20)]


    def reset(self):
        obs = {}
        self.dones = set()
        for i in range(self.num_agents):
            x = random.randint(0, 19)
            y = random.randint(0, 19)
            obs[i] = np.array([x, y])
        self.locations = obs
        self.iterations = 50
        self.fruit_ripening_time = 15
        self.fruit_grid = [[random.randint(0, self.fruit_ripening_time) for c in range(20)] for r in range(20)]
        return obs

    def cal_rewards(self, obs_dict, action_dict):

        obs = {}
        reward = {}
        dones = {}
        info = {}

        for i in range(self.num_agents):

            reward_value = 0
            action = action_dict.get(i)

            current_location = obs_dict.get(i)
            # print(current_location)
            new_location = np.array([0, 0])
            x_val = current_location[0]
            # print(x_val)
            y_val = current_location[1]
            # print(y_val)

            if action == 0 and y_val < 19:
                new_location[0] = x_val
                new_location[1] = y_val + 1
            elif action == 1 and x_val < 19:
                new_location[0] = x_val + 1
                new_location[1] = y_val
            elif action == 2 and y_val > 0:
                new_location[0] = x_val
                new_location[1] = y_val - 1
            elif action == 3 and x_val > 0:
                new_location[0] = x_val - 1
                new_location[1] = y_val
            else:
                new_location = current_location

            if self.fruit_grid[new_location[0]][new_location[1]] <= 0:
                reward_value = 1
                self.fruit_grid[new_location[0]][new_location[1]] = self.fruit_ripening_time
            elif np.array_equal(new_location, current_location):
                reward_value = -1
            else:
                reward_value = 0
            if self.iterations == 0 :
                dones[i] = True
            else:
                dones[i] = False
            obs[i] = new_location
            reward[i] = reward_value
            info[i] = {}

        for i in range(len(self.fruit_grid)):
            for j in range(len(self.fruit_grid[i])):
                self.fruit_grid[i][j] = self.fruit_grid[i][j]-1
        self.locations = obs
        return obs, reward, dones, info

    def step(self, action_dict):
        self.iterations -= 1
        obs, rew, done, info = {}, {}, {}, {}
        obs, rew, done, info = self.cal_rewards(self.locations, action_dict)
        if self.iterations == 0:
            done["__all__"] = True
        else:
            done["__all__"] = False
        # print(obs)
        # print(self.observation_space)
        return obs, rew, done, info


"""
This code is for the environment, if it generates rewards and cycles thorough episodes before training

def env_creator(_):
    return TestGrid()
single_env = TestGrid()
env_name = "MultiAgentGrid"
register_env(env_name, env_creator)

# Get environment obs, action spaces and number of agents
obs_space = single_env.observation_space
act_space = single_env.action_space
num_agents = single_env.num_agents
print(obs_space)
print(act_space)
print(num_agents)

env = TestGrid()
print(env.action_space.sample())
print(env.observation_space.sample())
episodes = 100
agents = 20
for episode in range(1, episodes+1):
    observation = env.reset()
    print(observation)

    done = False
    score = 0

    while not done:
        act = {}
        obs = {}
        for k in range(agents):
            new_act = env.action_space.sample()
            act[k] = new_act

        observation, reward, done, info = env.step(act)
        print(reward)
        for key, value in reward.items():
            score += value



    print('Episode:{} Score:{}'.format(episode, score))"""
