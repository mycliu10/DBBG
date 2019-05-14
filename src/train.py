import numpy as np
from spinup import ppo
import os

class Doubling:
    def __init__(self, dir_in='season', dynamic=False):
        self._dir_in = dir_in
        self._count_season = 0
        self._num_episodes = 0
        self._count_episode = 0

        from gym.spaces.discrete import Discrete
        from gym.spaces.box import Box
        self.action_space = Discrete(2)
        self.observation_space = Box(-8, 8, shape=(50,), dtype=np.int)

        self._dynamic = dynamic
        self._global_count = 0


    def reset(self):
        if self._dynamic:
            with open("counter.dat", "w") as fh:
                fh.write(self._count_episode.__str__())
            import subprocess
            subprocess.call(["gnubg -t -p play.py"], stdout=subprocess.DEVNULL, shell=True)
            filename = "".join((self._dir_in,'eps',self._count_episode.__str__().zfill(8),'.dat'))
        else:
            if self._count_episode == self._num_episodes:
                self._count_season += 1
                self._season_dir = "".join( ("season", self._count_season.__str__().zfill(2), '/') )
                print("ENTERED", self._season_dir)
                self._filenames = os.listdir(self._season_dir)
                self._num_episodes = len(self._filenames)
                self._count_episode = 0
                
            filename = "".join( (self._season_dir, self._filenames[self._count_episode]) )

        try:
            self._data = np.loadtxt(filename)
        except:
            self._data = np.zeros(50)
#            raise NotImplementedError("STOP! DATA ALL USED!")

        self._num_moves = self._data.shape[0]
        self._count_move = 0
        try:
            observation = self._data[0,:50]
        except:
            self._count_episode += 1
            observation = self.reset()

        self._count_episode += 1
        if self._count_season >= 9:
            raise ValueError("Season over...")
        self._global_count += 1
        if self._global_count%1000==1:
            print("COUNT ", self._global_count)
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
            


def main():

    import tensorflow as tf
    env_fn = lambda : Doubling()
    ac_kwargs = dict(hidden_sizes=[50,50], activation=tf.nn.relu)
    logger_kwargs = dict(output_dir='output_dir3', exp_name='training_64x64relu')
    ppo(env_fn=env_fn, ac_kwargs=ac_kwargs, steps_per_epoch=5000, epochs=25000000000, logger_kwargs=logger_kwargs, save_freq=1)


if __name__=='__main__':
    main()
