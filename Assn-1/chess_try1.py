import gym
import gym_chess
import random

env = gym.make('Chess-v0')
print(env.render())

env.reset()
done = False
num=  0
while not done:
    if len(env.legal_moves) == 0: break
    print('num: ', num, env.legal_moves)
    num += 1

    action = random.sample(env.legal_moves,1)
    env.step(action[0])
    print(env.render(mode='unicode'),'\n\n\n\n\n')
    if num == 5: break
    
env.close()