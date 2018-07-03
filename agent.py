# -*- coding: utf-8 -*-
import random

from abc import ABC, ABCMeta, abstractmethod


class AgentA(ABC):
    __metaclass__ = ABCMeta

    @abstractmethod
    def set_feedback(self, states, reward):
        """ Установка нового состояния
        и награды за предыдущее действие"""

    @abstractmethod
    def get_chosen_action_number(self):
        """ Получение выбранного действия"""

    @abstractmethod
    def get_params(self):
        """ Получение найденных коэффициентов"""


class Agent(AgentA):
    _states = None
    _last_reward = None
    _total_reward = None
    _number_of_actions = None
    _number_of_states = None

    _entry = None

    def __init__(self, number_of_states, number_of_actions):
        self._last_reward = 0
        self._total_reward = 0
        self._number_of_actions = number_of_actions
        self._number_of_states = number_of_states

    def set_feedback(self, states, reward):
        self._states = states
        self._last_reward = reward
        self._total_reward += reward

    def get_chosen_action_number(self):
        """ Случайное блуждание"""
        return random.randint(0, self._number_of_actions - 1)

    def get_params(self):
        """ """
