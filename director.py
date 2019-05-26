# -*- coding: utf-8 -*-
# Посредник между средой и агентом.
from environment import Environment
from agent import Agent
from MotionMap import MotionMap
import random


def run():

    # agent = Agent(number_of_actions=3, Q={(1.0, 1.0): [1, 0, 0],
    #                                       (1.0, 2.0): [0, 1, 0],
    #                                       (0.0, 1.0): [0, 1, 0],
    #                                       (0.0, 2.0): [0, 1, 0],
    #                                       (1.0, 0.0): [0, 0, 1],
    #                                       (0.0, 0.0): [1, 0, 0],
    #                                       (2.0, 2.0): [1, 0, 0],
    #                                       (2.0, 0.0): [0, 0, 1],
    #                                       (2.0, 1.0): [0, 0, 1],
    #
    #                                       (0.0, 3.0): [0, 1, 0],
    #                                       (1.0, 3.0): [0, 1, 0],
    #                                       (2.0, 3.0): [0, 1, 0],
    #                                       (3.0, 0.0): [0, 0, 1],
    #                                       (3.0, 1.0): [0, 0, 1],
    #                                       (3.0, 2.0): [0, 0, 1],
    #                                       (3.0, 3.0): [1, 0, 0],
    #                                     })
    agent = Agent(number_of_actions=3, Q={})
    # стратегия смещаться только при сильном отклонении
    # agent = Agent(number_of_actions=3, Q={(1.0, 1.0): [1, 0, 0],
    #                                       (1.0, 2.0): [0, 1, 0],
    #                                       (0.0, 1.0): [1, 0, 0],
    #                                       (0.0, 2.0): [0, 1, 0],
    #                                       (1.0, 0.0): [1, 0, 0],
    #                                       (0.0, 0.0): [1, 0, 0],
    #                                       (2.0, 2.0): [1, 0, 0],
    #                                       (2.0, 0.0): [0, 0, 1],
    #                                       (2.0, 1.0): [0, 0, 1],
    #
    #                                       (0.0, 3.0): [0, 1, 0],
    #                                       (1.0, 3.0): [0, 1, 0],
    #                                       (2.0, 3.0): [0, 1, 0],
    #                                       (3.0, 0.0): [0, 0, 1],
    #                                       (3.0, 1.0): [0, 0, 1],
    #                                       (3.0, 2.0): [0, 0, 1],
    #                                       (3.0, 3.0): [1, 0, 0],
    #                                       })
    motion_map = MotionMap()
    # Запустим N действий
    N = 100
    show_every_n = 10
    for epoch in range(N):
        start_positions = motion_map.get_start_positions()
        start_point = start_positions[random.randint(0, len(start_positions)-1)]
        if epoch % show_every_n == 0:
            start_point[0] = 58
            start_point[1] = 34

        start_point[0] += random.randint(-2, 2)
        start_point[1] += random.randint(-2, 2)

        env = Environment(start_position=start_point,
                          number_of_last_states=1,
                          theta=16,
                          step=1,
                          start_theta=90,
                          dist_btw_sensors=8)
        for i in range(600):
            agent.process(env.get_states(), env.get_reward(), )

            # env.log()
            action_id = agent.get_chosen_action_number()

            env.process_action(action_id)
            if env.get_reward() < -12:
                break
        agent.reset_reward()
        if epoch % show_every_n == 0:
            env.show()
    new_q = agent.get_params()
    for i in new_q:
        print(i, ':', new_q[i])
