from spinup.utils.test_policy import load_policy, run_policy

_, get_action = load_policy("output_dir2")

import train

double = train.Doubling()
run_policy(double, get_action)
