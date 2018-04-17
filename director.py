# -*- coding: utf-8 -*-
# Посредник между средой и агентом.
from environment import Environment
from agent import Agent


def run():
    env = Environment(start_position=(13, 4),
                      start_theta=-60)
    agent = Agent(number_of_states=env.get_number_of_last_states(),
                  number_of_actions=env.get_number_of_actions())
    # Запустим 100 действий
    for i in range(10):
        agent.set_feedback(env.get_states(), env.get_reward(), )
        env.log()
        action_id = agent.get_chosen_action_number()
        env.process_action(action_id)

    env.show()

