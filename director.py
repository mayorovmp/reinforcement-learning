# -*- coding: utf-8 -*-
# Посредник между средой и агентом.
from environment import Environment
from agent import Agent
from MotionMap import MotionMap
import random


def run():

    agent = Agent(number_of_actions=3, Q={})
    map = MotionMap()
    # Запустим N действий
    N = 1001
    for epoch in range(N):
        start_point = map._start_positions[random.randint(0, len(map._start_positions)-1)]
        start_point[0] += random.randint(-4, 4)
        start_point[1] += random.randint(-4, 4)
        env = Environment(start_position=start_point,
                          number_of_last_states=1,
                          theta=15,
                          start_theta=90,
                          map=map)
        for i in range(100):
            agent.process(env.get_states(), env.get_reward(), )

            env.log()
            action_id = agent.get_chosen_action_number()
            env.process_action(action_id)
            if env.get_reward() < -16:
                break
        agent.reset_reward()
        if epoch % 50 == 0:
            env.show()
    print(agent.get_params())


