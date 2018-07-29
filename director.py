# -*- coding: utf-8 -*-
# Посредник между средой и агентом.
from environment import Environment
from agent import Agent


def run():

    agent = Agent(number_of_actions=3, Q={})
    # Запустим N действий
    for epoch in range(3):
        env = Environment(start_position=(31, 57),
                          number_of_last_states=1,
                          start_theta=-90)
        for i in range(20):
            agent.process(env.get_states(), env.get_reward(), )
            env.log()
            action_id = agent.get_chosen_action_number()
            env.process_action(action_id)
        # env = Environment(start_position=(31, 57),
        #                   number_of_last_states=1,
        #                   start_theta=-90)

        env.show()


