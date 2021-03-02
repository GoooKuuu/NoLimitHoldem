''' An example of solve Leduc Hold'em with CFR (chance sampling)
'''
import numpy as np

import rlcard
from rlcard.agents.best_response_agent import BRAgent
from rlcard.agents.random_agent import RandomAgent
from rlcard.agents.cfr_agent import CFRAgent
from rlcard.agents.cfr_agent import CFRAgent
from rlcard import models
from rlcard.utils.utils import set_global_seed, tournament
from rlcard.utils.exploitability import exploitability
from rlcard.utils.logger import Logger

# Make environment and enable human mode
env = rlcard.make('leduc-holdem', config={'allow_step_back': True, 'allow_raw_data': True})
eval_env = rlcard.make('leduc-holdem', config={'allow_step_back': True, 'allow_raw_data': True, 'seed':0})

# Set the iterations numbers and how frequently we evaluate/save plot
evaluate_every = 100
save_plot_every = 1000
evaluate_num = 100
episode_num = 10000000

# The paths for saving the logs and learning curves
log_dir = './experiments/leduc_holdem_br_result/'

# Set a global seed
set_global_seed(0)


# Initilize CFR Agent
opponent = CFRAgent(env) 
#opponent = RandomAgent(action_num=env.action_num)
#opponent.load()  # If we have saved model, we first load the model

#agent = RandomAgent(action_num=env.action_num)
agent = BRAgent(eval_env, opponent)
#agent = CFRAgent(env) 

# Evaluate CFR against pre-trained NFSP

# Init a Logger to plot the learning curve
logger = Logger(log_dir)

for episode in range(episode_num):
    opponent.train()
    #agent.train()
    print('\rIteration {}'.format(episode), end='\t')
    # Evaluate the performance. Play with NFSP agents.
    if episode % evaluate_every == 0:
        exp = exploitability(eval_env, opponent, evaluate_num)
        print("Eploitability:", exp)
        #logger.log_performance(env.timestep, tournament(eval_env, evaluate_num)[0])

# Close files in the logger
logger.close_files()
logger.plot('BR')
