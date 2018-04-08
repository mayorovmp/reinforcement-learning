# -*- coding: utf-8 -*-
# Посредник между средой и агентом.
from environment import Environment
from agent import Agent


def main():
    # env = Environment(start_position=[[14.], [4.]])
    env = Environment(start_position=[[133.], [46.]])
    agent = Agent()
    for i in range(100):
        agent.set_feedback(env.get_sensors(), env.get_reward(), env.get_actions_amount())
        action_id = agent.get_chosen_action_number()
        env.process_action(action_id)
        env.log()
    env.show()


main()
