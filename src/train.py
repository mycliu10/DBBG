import numpy as np
from spinup import ppo

class Doubling:
    def __init__(self, dir_in='finale/'):
        self._dir_in = dir_in
        import os
        self._num_episodes = len(os.listdir(dir_in))
        self._count_episode = 0

        from gym.spaces.discrete import Discrete
        from gym.spaces.box import Box
        self.action_space = Discrete(2)
        self.observation_space = Box(-8, 8, shape=(50,), dtype=np.int)


    def reset(self):
        with open("counter.dat", "w") as fh:
            fh.write(self._count_episode.__str__())
        import subprocess
        subprocess.call(["gnubg -t -p play.py"], stdout=subprocess.DEVNULL, shell=True)

        filename = "".join((self._dir_in,'eps',self._count_episode.__str__().zfill(8),'.dat'))
        self._data = np.loadtxt(filename)
        self._num_moves = self._data.shape[0]
        self._count_move = 0
        observation = self._data[0,:50]

        self._count_episode += 1
        return observation

    def step(self, action):
        if action==1:
            reward = self._data[self._count_move,-1]
        else:
            reward = self._data[self._count_move,-2]

        self._count_move += 1
        if self._count_move < self._num_moves:
            observation = self._data[self._count_move,:50]
            done = False
        else:
            observation = self._data[-1,:50]
            done = True
        info = {}

        return observation, reward, done, info
            


import tensorflow as tf
env_fn = lambda : Doubling()
ac_kwargs = dict(hidden_sizes=[64,64], activation=tf.nn.relu)
logger_kwargs = dict(output_dir='output_dir', exp_name='training_64x64relu')
ppo(env_fn=env_fn, ac_kwargs=ac_kwargs, steps_per_epoch=5000, epochs=250, logger_kwargs=logger_kwargs, save_freq=1)

