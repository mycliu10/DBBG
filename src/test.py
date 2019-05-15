from spinup.utils.test_policy import load_policy, run_policy

_, get_action = load_policy("output_dir2")
import numpy as np
import train

double = train.Doubling()
o = np.array([0, 2, 0, 0, 0, 3, 0, 3, 0, 0, 1, 0, 3, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 5, 0, 3, 0, 0, 0, 1, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0])
a = get_action(o)
print(a)
#run_policy(double, get_action)
