''' Register new environments
'''
from rlcard.envs.env import Env
from rlcard.envs.vec_env import VecEnv
from rlcard.envs.registration import register, make


register(
    env_id='limit-holdem',
    entry_point='rlcard.envs.limitholdem:LimitholdemEnv',
)

register(
    env_id='no-limit-holdem',
    entry_point='rlcard.envs.nolimitholdem:NolimitholdemEnv',
)

register(
    env_id='leduc-holdem',
    entry_point='rlcard.envs.leducholdem:LeducholdemEnv'
)
