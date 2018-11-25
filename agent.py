# -*- coding: utf-8 -*-
import random

from abc import ABC, ABCMeta, abstractmethod
import numpy as np


class AgentA(ABC):
    __metaclass__ = ABCMeta

    @abstractmethod
    def process(self, states, reward):
        """ Установка нового состояния
        и награды за предыдущее действие"""

    @abstractmethod
    def get_chosen_action_number(self):
        """ Получение выбранного действия"""

    @abstractmethod
    def get_params(self):
        """ Получение найденных коэффициентов"""


class Agent(AgentA):
    _last_reward = None
    _last_state = None
    _last_action_number = None
    _total_reward = None
    _number_of_actions = None
    _Q = None

    _entry = None

    def __init__(self, number_of_actions, Q):
        self._last_reward = 0
        self._total_reward = 0
        self._number_of_actions = number_of_actions
        self._last_state = -1
        self._last_action_number = 0
        self._Q = Q

    def process(self, state, reward):

        if self._Q.get(self._last_state) is None and self._last_state != -1:
            self._Q[self._last_state] =np.zeros(self._number_of_actions)

        if self._Q.get(state) is None:
            self._Q[state] = np.zeros(self._number_of_actions)

        if self._last_state != -1:
            self._Q[self._last_state][self._last_action_number] += reward

        self._last_state = state

        self._last_reward = reward
        self._total_reward += int(reward)
        localMax = -9999999
        idx = 0
        for i in range(len(self._Q[state])):
            if localMax < self._Q[state][i]:
                localMax = self._Q[state][i]
                idx = i
        # idx = self._Q[state].index(max(self._Q[state]))
        self._last_action_number = idx

    def set_Q(self, Q):
        self._Q = Q

    def get_chosen_action_number(self):
        """ """
        return self._last_action_number

    def get_params(self):
        """ """
        return self._Q

    def get_total_reward(self):
        return self._total_reward

    def reset_reward(self):
        self._total_reward = 0
