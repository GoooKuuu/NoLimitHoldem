from rlcard.envs.registration import register, make
import numpy as np
import time

start = time.time()
battle_number = 100000
Reward = 0
for _ in range(battle_number):
    env = make('no-limit-holdem',config={'single_agent_mode':True})
    #print('---------------new game------------------------')
    state = env.reset()
    #dealer_id = env.game.dealer_id
    #print("dealer id即小盲注位置为:",env.game.dealer_id)
    #print('state:',state)
    while True:
        action = np.random.choice(state['legal_actions'])
        #print('选择的动作为:',action)
        state,reward,done = env.step(action)
        #print('state:',state)
        #print('reweard:',reward)
        #print('done:',done)
        if done:
            Reward += reward
            break
end = time.time()
print('the average payoff of {} battles TA Vs random opponent:{}'.format(battle_number,Reward/battle_number))
print('time is：',end-start)
