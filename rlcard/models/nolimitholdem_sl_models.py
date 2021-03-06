'''
NoLimit Hold 'em rule model
ScaredLimper 只有拿到最顶级的牌才call，否则对于任何bet都fold 在小盲位时先跟注
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

hand_strength_band = 200

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
    #小盲注时直接call 检测场内chips即可 如果是[1,2]或者[2,1]一定是该种情况
    my_chips = state['raw_obs']['my_chips']
    if my_chips == 1:
        return Action.CALL
    #根据手中牌力进行动作
    #若牌力很高或者自己先动作(即此时双方筹码相同)才会call
    #其余情况 自己牌力不高且不是自己先动作 直接fold()
    legal_actions = state['raw_legal_actions']
    all_chips = state['raw_obs']['all_chips']
    if hand_strength >= hand_strength_band or (all_chips[0] == all_chips[1]):
        if Action.CALL in legal_actions:
            return Action.CALL
        else:
            return Action.CHECK
    else:
        return Action.FOLD

class NoLimitholdemScaredLimperAgent(object):
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

class NoLimitholdemScaredLimperModel(Model):
    ''' NoLimitholdem Random Model
    '''

    def __init__(self):
        ''' Load model
        '''
        env = rlcard.make('no-limit-holdem')

        rule_agent = NoLimitholdemScaredLimperAgent()
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
