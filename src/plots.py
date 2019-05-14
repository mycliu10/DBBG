import matplotlib.pyplot as plt
import numpy as np

data = np.loadtxt("output_dir2/progress.txt", skiprows=1)

plt.plot(data[::15,0], data[::15,1], linewidth=5)
plt.gca().set_xlabel("Epoch", fontsize=18)
plt.gca().set_ylabel("Reward", fontsize=18)
plt.show()
