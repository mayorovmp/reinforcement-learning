# -*- coding: utf-8 -*-
# Посредник между средой и агентом.
from environment import Environment
from agent import Agent
from MotionMap import MotionMap
import random


def run():

    agent = Agent(number_of_actions=3, Q={(1.0, 1.0): [1, 0, 0],
                                          (1.0, 2.0): [0, 1, 0],
                                          (0.0, 1.0): [0, 1, 0],
                                          (0.0, 2.0): [0, 1, 0],
                                          (1.0, 0.0): [0, 0, 1],
                                          (0.0, 0.0): [1, 0, 0],
                                          (2.0, 2.0): [1, 0, 0],
                                          (2.0, 0.0): [0, 0, 1],
                                          (2.0, 1.0): [0, 0, 1],

                                          (0.0, 3.0): [0, 1, 0],
                                          (1.0, 3.0): [0, 1, 0],
                                          (2.0, 3.0): [0, 1, 0],
                                          (3.0, 0.0): [0, 0, 1],
                                          (3.0, 1.0): [0, 0, 1],
                                          (3.0, 2.0): [0, 0, 1],
                                          (3.0, 3.0): [1, 0, 0],
                                          })
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

    map = MotionMap()
    # Запустим N действий
    N = 1
    show_every_n = 20
    for epoch in range(N):
        start_point = map._start_positions[random.randint(0, len(map._start_positions)-1)]
        if epoch % show_every_n == 0:
            start_point[0] = 58
            start_point[1] = 34

        #start_point[0] += random.randint(-2, 2)
        #start_point[1] += random.randint(-2, 2)

        env = Environment(start_position=start_point,
                          number_of_last_states=1,
                          theta=16,
                          step=2,
                          start_theta=90,
                          dist_btw_sensors=9,
                          map=map)
        for i in range(650):
            agent.process(env.get_states(), env.get_reward(), )

            # env.log()
            action_id = agent.get_chosen_action_number()

            env.process_action(action_id)
            x, y = int(env._start_point[0][0]), int(env._start_point[1][0])
            if env.get_reward() < -12 or x > 190 or y > 190 or x < 10 or y < 10:
                break
        agent.reset_reward()
        if epoch % show_every_n == 0:
            env.show()
    newQ=agent.get_params()
    for i in newQ:
        print(i, ':', newQ[i])