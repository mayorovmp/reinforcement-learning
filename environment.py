# -*- coding: utf-8 -*-
import numpy as np
from queue import Queue
from PIL import Image


class Environment:
    _RED = (255, 0, 0)
    _GREEN = (0, 255, 0)
    _BLUE = (0, 0, 255)

    _img_map = None     # Картинка, для отображения
    _states = None  # Карта с линией
    _sensors = None  # Состояние датчиков
    _actions = []  # Допустимые ходы
    _last_reward = None

    _step = None       # Длина вектора - шаг, так как картинка дискретна, то это часть пикселя
    _dist_btw_sensors = None    # Расстояние между сенсорами

    _start_point = None  # Позиция робота
    _end_point = None   # Куда сходит робот

    _theta = None

    def __init__(self,
                 start_position: 'Вектор столбец. Начальная позиция робота' = (0, 0),  #[[0.], [0.]],
                 step: 'Длина шага'=1.0,
                 theta: 'Угол поворота в градусах'=30,
                 dist_btw_sensors: 'Расстояние между сенсорами'=0.5,
                 path_to_map: 'Путь до картинки с картой'='maps\map1.jpg'):

        self._dist_btw_sensors = dist_btw_sensors

        self._theta = theta

        self._step = float(step)
        start_position = [
            [float(start_position[0])],
            [float(start_position[1])]
        ]

        self._start_point = np.array(start_position)
        end_position = start_position
        end_position[1][0] += step
        self._end_point = np.array(end_position)

        self._actions.append(self._action1)
        self._actions.append(self._action2)
        self._actions.append(self._action3)

        self._sensors = np.zeros(2)

        self._load_map(path_to_map)

        self._mark_position(color=Environment._RED)

    def get_sensors(self):
        self._eval_sensor_state()
        return self._sensors

    def get_actions_amount(self):
        return len(self._actions)

    def process_action(self, action_id):
        self._actions[action_id]()

    def log(self):
        print('position: [' + str(self._start_point[0][0]) + ', ' + str(self._start_point[1][0]) + ']')
        print('sensors: [' + str(self.get_sensors()) + ']')
        print('last reward: ' + str(self._last_reward))
        print()

    def get_reward(self):
        self._last_reward = self._evaluate_reward()
        return self._last_reward

    def _evaluate_reward(self):
        """ Оценка награды, расчитывается как расстояние до ближайшей линии, использую волновой алгоритм(BFS)"""
        queue = Queue()
        visited = set()
        start_point = [[int(self._start_point[0][0])], [int(self._start_point[1][0])]]  # [[12], [43]]
        queue.put(start_point)
        reward = float('-inf')
        while not queue.empty():
            cur_position = queue.get()
            queue.task_done()

            x_pos = cur_position[0][0]
            y_pos = cur_position[1][0]

            if not self._is_valid_point_position(cur_position):
                continue

            if (x_pos, y_pos) in visited:
                continue

            visited.add((x_pos, y_pos))

            if self._states[x_pos][y_pos] > 0.5:
                reward = -abs(x_pos - start_point[0][0]) - abs(y_pos - start_point[1][0])
                break

            next_pos = [[x_pos + 1], [y_pos]]
            queue.put(next_pos)

            next_pos = [[x_pos - 1], [y_pos]]
            queue.put(next_pos)

            next_pos = [[x_pos], [y_pos + 1]]
            queue.put(next_pos)

            next_pos = [[x_pos], [y_pos - 1]]
            queue.put(next_pos)
        return reward

    def show(self):
        self._img_map.show()
        # self._img_map.save('map6.png')

    def _action1(self):
        """ Движение вперед."""
        d = self._end_point - self._start_point
        self._start_point += d
        self._end_point += d
        self._mark_position()

    def _action2(self):
        """ Поворот по часовой на фиксированный угол и движение по направлению вектора."""
        self._end_point = Environment.rotate(self._start_point, self._end_point, -self._theta)
        self._action1()

    def _action3(self):
        """ Поворот против часовой на фиксированный угол и движение по направлению вектора."""
        self._end_point = Environment.rotate(self._start_point, self._end_point, self._theta)
        self._action1()

    @staticmethod
    def rotate(point_a, point_b, theta):
        """Поворот point_b относительно point_a на угол theta, возврат новые координаты. """
        d = point_b - point_a  # Перенесли центр координатных осей
        d = np.dot(Environment._get_rot_matrix(theta), d)  # Совершили поворот против часовой
        d += point_a  # Вернули центр оси
        return d

    def _eval_sensor_state(self):
        left_sensor_position = self._eval_left_sensor_position()
        right_sensor_position = self._eval_right_sensor_position()

        if self._is_valid_point_position(left_sensor_position):
            x_left = int(left_sensor_position[0][0])
            y_left = int(left_sensor_position[1][0])
            self._sensors[0] = self._states[x_left][y_left]
        else:
            self._sensors[0] = 0

        if self._is_valid_point_position(right_sensor_position):
            x_right = int(right_sensor_position[0][0])
            y_right = int(right_sensor_position[1][0])
            self._sensors[1] = self._states[x_right][y_right]
        else:
            self._sensors[1] = 0

    def _is_valid_point_position(self, point):
        """ point - вектор столбец [[2\n  1]]"""
        if point[0][0] < 0 or point[1][0] < 0:
            return False

        if point[0][0] >= self._states.shape[0] or point[1][0] >= self._states.shape[1]:
            return False
        return True

    def _eval_left_sensor_position(self):
        left_point = Environment.rotate(self._start_point, self._end_point, 90)
        k = self._dist_btw_sensors / self._step
        left_point -= self._start_point
        left_point *= k
        left_point += self._start_point
        return left_point

    def _eval_right_sensor_position(self):
        right_point = Environment.rotate(self._start_point, self._end_point, -90)
        k = self._dist_btw_sensors / self._step
        right_point -= self._start_point
        right_point *= k
        right_point += self._start_point
        return right_point

    def _load_map(self, path):
        self._img_map = Image.open(path)
        #  im.save('greyscale.png')
        states = np.array(self._img_map.convert('L'))
        mx = states.max()
        states = states / mx
        self._states = states

    def _mark_position(self, color=_GREEN):
        if not self._is_valid_point_position(self._start_point):
            return
        x = int(self._start_point[0][0])
        y = int(self._start_point[1][0])
        pixels = self._img_map.load()
        pixels[x, y] = color

    @staticmethod
    def _get_rot_matrix(theta_degree):
        """ Матрица поворота против часовой. """
        theta = np.radians(theta_degree)
        return np.array(((np.cos(theta), -np.sin(theta)),
                         (np.sin(theta), np.cos(theta))))

    def _get_states(self):
        return self._states

    def _set_states(self, states):
        self._states = states

