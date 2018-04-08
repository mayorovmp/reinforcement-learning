# -*- coding: utf-8 -*-
import random


class Agent:
    _sensors = None
    _last_reward = None
    _total_reward = None
    _amount_available_actions = None

    def __init__(self, ):
        self._last_reward = 0
        self._total_reward = 0

    def set_feedback(self, sensors, reward, amount_available_actions):
        self._sensors = sensors
        self._last_reward = reward
        self._total_reward += reward
        self._amount_available_actions = amount_available_actions

    def get_chosen_action_number(self, ):
        """ Случайное блуждание"""
        return random.randint(0, self._amount_available_actions - 1)
