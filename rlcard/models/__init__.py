''' Register rule-based models or pre-trianed models
'''

from rlcard.models.registration import register, load
import subprocess
import sys
from distutils.version import LooseVersion

reqs = subprocess.check_output([sys.executable, '-m', 'pip', 'freeze'])
installed_packages = [r.decode().split('==')[0] for r in reqs.split()]

if 'tensorflow' in installed_packages:
    import tensorflow as tf
    if LooseVersion(tf.__version__) < LooseVersion('1.14.0') \
            or LooseVersion(tf.__version__) >= LooseVersion('2.0.0'):
        print('WAINING - RLCard supports Tensorflow >=1.14 and <2.0\nThe detected version is {} \nIf the models can not be loaded, please install Tensorflow via\n$ pip install rlcard[tensorflow]\n'.format(tf.__version__))
    register(
        model_id = 'leduc-holdem-nfsp',
        entry_point='rlcard.models.pretrained_models:LeducHoldemNFSPModel')

if 'torch' in installed_packages:
    register(
        model_id = 'leduc-holdem-nfsp-pytorch',
        entry_point='rlcard.models.pretrained_models:LeducHoldemNFSPPytorchModel')

register(
    model_id = 'leduc-holdem-cfr',
    entry_point='rlcard.models.pretrained_models:LeducHoldemCFRModel')

register(
    model_id = 'leduc-holdem-rule-v1',
    entry_point='rlcard.models.leducholdem_rule_models:LeducHoldemRuleModelV1')

register(
    model_id = 'leduc-holdem-rule-v2',
    entry_point='rlcard.models.leducholdem_rule_models:LeducHoldemRuleModelV2')


register(
    model_id = 'limit-holdem-rule-v1',
    entry_point='rlcard.models.limitholdem_rule_models:LimitholdemRuleModelV1')

register(
    model_id = 'nolimit-holdem-random',
    entry_point='rlcard.models.nolimitholdem_random_models:NoLimitholdemRandomModel')

register(
    model_id = 'nolimit-holdem-call',
    entry_point='rlcard.models.nolimitholdem_call_models:NoLimitholdemCallModel')

register(
    model_id = 'nolimit-holdem-hm',
    entry_point='rlcard.models.nolimitholdem_hm_models:NoLimitholdemHotheadManiacModel')

register(
    model_id = 'nolimit-holdem-la',
    entry_point='rlcard.models.nolimitholdem_la_models:NoLimitholdemLooseAggressiveModel')

register(
    model_id = 'nolimit-holdem-lp',
    entry_point='rlcard.models.nolimitholdem_lp_models:NoLimitholdemLoosePassiveModel')

register(
    model_id = 'nolimit-holdem-sl',
    entry_point='rlcard.models.nolimitholdem_sl_models:NoLimitholdemScaredLimperModel')

register(
    model_id = 'nolimit-holdem-ta',
    entry_point='rlcard.models.nolimitholdem_ta_models:NoLimitholdemTightAggressiveModel')

register(
    model_id = 'nolimit-holdem-tp',
    entry_point='rlcard.models.nolimitholdem_tp_models:NoLimitholdemTightPassiveModel')
