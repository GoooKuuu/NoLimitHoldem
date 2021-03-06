'''
NoLimit Hold 'em rule model
TightAggressive 会有一定概率的bluff

'''
import rlcard
from rlcard.models.model import Model
import numpy as np
from rlcard.games.nolimitholdem import Action

from rlcard.models.CardEvaluator.lookup import Lookup

'''
FOLD = 0
CHECK = 1
CALL = 2
RAISE_HALF_POT = 3
RAISE_POT = 4
ALL_IN = 5
'''

hand_strength_band_high = 100     # 用于调整手牌阈值
hand_strength_band_low = -100

bluffing_rate = 0.2  #弱牌bluffing的概率

def card_transform(cards):
    '''
    对牌型做一个格式转换 使其符合lookup的查找标准
    ['CA', 'S2'] -> ['Ac', '2s']
    '''
    if len(cards) == 0:
        return cards
    cards_T = []
    for card in cards:
        card = card[1] + card[0].lower()
        cards_T.append(card)
    return cards_T

def get_action(state, hand_strength):
    #action = get_action(state, hand_strength)
    legal_actions = state['raw_legal_actions']
    if hand_strength < hand_strength_band_low:
        #弃牌或者诈唬
        rand_num = random.uniform(0, 1)
        if (rand_num < bluffing_rate) and (Action.RAISE_HALF_POT in legal_actions):
            action = np.random.choice([Action.RAISE_HALF_POT,Action.RAISE_POT])
            return action
        return Action.FOLD
    elif hand_strength < hand_strength_band_high:
        if Action.CALL in legal_actions:
            return Action.CALL
        else:
            return Action.CHECK
    elif hand_strength >= hand_strength_band_high:
        if Action.RAISE_HALF_POT in legal_actions:
            action = np.random.choice([Action.RAISE_HALF_POT,Action.RAISE_POT])
            return action
        elif Action.CALL in legal_actions:
            return Action.CALL
        else:
            return Action.CHECK

class NoLimitholdemTightAggressiveAgent(object):
    ''' NoLimit Hold 'em Random agent
    '''

    def __init__(self):
        self.use_raw = True
        #初始化查表工具
        self.lookup = Lookup()

    @staticmethod
    def step(self,state):
        ''' Predict the action when given raw state. A simple rule-based AI.
        Args:
            state (dict): Raw state from the game

        Returns:
            action (str): Predicted action
        '''
        legal_actions = state['raw_legal_actions']
        #首先计算手牌强度
        private_card = card_transform(state['raw_obs']['hand'])
        public_card = card_transform(state['raw_obs']['public_cards'])
        hand_strength = self.lookup.calc(private_card, public_card)
        action = get_action(state, hand_strength)
        return action



    def eval_step(self, state):
        ''' Step for evaluation. The same to step
        '''
        return self.step(self,state), []

class NoLimitholdemTightAggressiveModel(Model):
    ''' NoLimitholdem Random Model
    '''

    def __init__(self):
        ''' Load model
        '''
        env = rlcard.make('no-limit-holdem')

        rule_agent = NoLimitholdemTightAggressiveAgent()
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
