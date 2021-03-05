'''
NoLimit Hold 'em rule model
HotheadManiac:总是随机raise 0.5/1 pot
'''
import rlcard
from rlcard.models.model import Model
import numpy as np
from rlcard.games.nolimitholdem import Action

'''
FOLD = 0
CHECK = 1
CALL = 2
RAISE_HALF_POT = 3
RAISE_POT = 4
ALL_IN = 5
'''

class NoLimitholdemHotheadManiacAgent(object):
    ''' NoLimit Hold 'em Random agent
    '''

    def __init__(self):
        self.use_raw = True

    @staticmethod
    def step(state):
        ''' Predict the action when given raw state. A simple rule-based AI.
        Args:
            state (dict): Raw state from the game

        Returns:
            action (str): Predicted action
        '''
        legal_actions = state['raw_legal_actions']
        action = np.random.choice([Action.RAISE_HALF_POT,Action.RAISE_POT])
        if action in legal_actions:
            return action
        elif Action.CALL in legal_actions:
            return Action.CALL
        else:
            return Action.CHECK


    def eval_step(self, state):
        ''' Step for evaluation. The same to step
        '''
        return self.step(state), []

class NoLimitholdemHotheadManiacModel(Model):
    ''' NoLimitholdem Random Model
    '''

    def __init__(self):
        ''' Load model
        '''
        env = rlcard.make('no-limit-holdem')

        rule_agent = NoLimitholdemHotheadManiacAgent()
        self.rule_agents = [rule_agent for _ in range(env.player_num)]
        #两个位置都设置为了rule

    @property
    def agents(self):
        ''' Get a list of agents for each position in a the game

        Returns:
            agents (list): A list of agents

        Note: Each agent should be just like RL agent with step and eval_step
              functioning well.
        '''
        return self.rule_agents

    @property
    def use_raw(self):
        ''' Indicate whether use raw state and action

        Returns:
            use_raw (boolean): True if using raw state and action
        '''
        return True
