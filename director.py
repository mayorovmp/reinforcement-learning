# -*- coding: utf-8 -*-
# Посредник между средой и агентом.
from environment import Environment
from agent import Agent


def run():

    agent = Agent(number_of_actions=3, Q={})
    # Запустим N действий
    N = 1000
    for epoch in range(N):
        env = Environment(start_position=(31, 57),
                          number_of_last_states=4,
                          start_theta=-90)
        for i in range(100):
            agent.process(env.get_states(), env.get_reward(), )

            env.log()
            action_id = agent.get_chosen_action_number()
            env.process_action(action_id)
            if env.get_reward() < -10:
                break
        agent.reset_reward()
        # env = Environment(start_position=(31, 57),
        #                   number_of_last_states=1,
        #                   start_theta=-90)
        if epoch % 100 == 0:
            env.show()


