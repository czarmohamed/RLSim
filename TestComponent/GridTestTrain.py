import ray
from ray import tune
from ray.rllib.models import MODEL_DEFAULTS
from ray.tune.registry import register_env
from GridTest import TestGrid

algo = input("Please enter [1] for Policy Gradient or [2] for Proximal Policy Optimization:\n")
def setup_and_train():
    # Create environment
    def env_creator(_):
        return TestGrid()
    single_env = TestGrid()
    env_name = "TestGrid"
    register_env(env_name, env_creator)

    # Return environment properties for policy mapping
    obs_space = single_env.observation_space
    act_space = single_env.action_space
    num_agents = single_env.num_agents

    # Map policy
    def generate_policy():
        return None, obs_space, act_space, {}

    # Generate Policy graphs
    policy_graph = {}
    for i in range(num_agents):
        policy_graph['agent-' + str(i)] = generate_policy()

    def policy_mapping_fn(agent_id):
        return 'agent-' + str(agent_id)

    if algo == "1":
        # Hyperparameter configuration 1
        config={
                    "log_level": "WARN",
                    "num_workers": 3,
                    "num_cpus_for_driver": 1,
                    "num_cpus_per_worker": 1,
                    "train_batch_size": 128,
                    "lr": 5e-3,
                    "model":{"fcnet_hiddens": [8, 8]},
                    "multiagent": {
                        "policies": policy_graph,
                        "policy_mapping_fn": policy_mapping_fn,
                    },
                    "env": "TestGrid"}

        # Training Details
        exp_name = 'my_exp'
        exp_dict = {
                'name': exp_name,
                'run_or_experiment': 'PG',
                "stop": {
                    "training_iteration": 100
                },
                'checkpoint_freq': 10,
                "config": config,
            }
    elif algo == "2":
        # Hyperparameter configuration 2
        config = {
            "log_level": "WARN",
            "num_workers": 3,
            "num_cpus_for_driver": 1,
            "num_cpus_per_worker": 1,
            "num_sgd_iter": 10,
            "train_batch_size": 128,
            "lr": 5e-3,
            "model":{"fcnet_hiddens": [8, 8]},
            "multiagent": {
                "policies": policy_graph,
                "policy_mapping_fn": policy_mapping_fn,
            },
            "env": "TestGrid"}

        # Training Details
        exp_name = 'my_exp'
        exp_dict = {
            'name': exp_name,
            'run_or_experiment': 'PPO',
            "stop": {
                "training_iteration": 100
            },
            'checkpoint_freq': 10,
            "config": config,
        }
    else:
        print("Please Enter an Algorithm")
        exit()
    ray.init()
    tune.run(**exp_dict)

if __name__=='__main__':
    setup_and_train()