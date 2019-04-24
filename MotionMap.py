import numpy as np
from PIL import Image


class MotionMap:
    _predicts = None # Предпросчет
    _map = None  # Карта с линией
    _center_line = None # карта с центральной линией
    _start_positions = []
    _dist_btw_sensors = None

    def __init__(self, path_to_map: 'Путь до картинки с картой'='maps/12.jpg',
                 dist_btw_sensors=8):
        _img_map = None  # Картинка, для отображения
        self._dist_btw_sensors = dist_btw_sensors
        self._load_map(path_to_map)
        self._find_center_line()
        self._eval_predicts()
        self._eval_start_positions()

    def _eval_start_positions(self):
        for i in range(self._center_line.shape[0]):
            for j in range(self._center_line.shape[1]):
                if self._center_line[i][j] > 0.5 and self._is_valid_point_position([[i], [j + self._dist_btw_sensors]]):
                    isValid = True
                    for d in range(self._dist_btw_sensors):
                        if self._center_line[i][j + d] < 0.5:
                            isValid = False
                            break
                    if isValid:
                        self._start_positions.append([i, j])

    def _is_valid_point_position(self, point: 'Вектор столбец вида [[2\n  1]]'):
        """ Проверка не вышли за границу. """
        if point[0][0] < 0 or point[1][0] < 0:
            return False

        if point[0][0] >= self._map.shape[0] or point[1][0] >= self._map.shape[1]:
            return False
        return True

    def _load_map(self, path):
        self._img_map = Image.open(path)
        # self._pixels = self._img_map.load()
        # im.save('greyscale.png')
        states = np.array(self._img_map.convert('L'))
        mx = states.max()
        states = states / mx
        for x in range(states.shape[0]):
            for y in range(states.shape[1]):
                if states[x][y] > 0.5:
                    states[x][y] = 1
                else:
                    states[x][y] = 0

        self._map = states

    def _eval_predicts(self):
        self._predicts = np.zeros(self._map.shape)

        for x in range(self._map.shape[0]):
            for y in range(self._map.shape[1]):
                sum = 0
                count = 0
                for i in range(-int(self._dist_btw_sensors / 2) + 1, int(self._dist_btw_sensors / 2) - 1):
                    for j in range(-int(self._dist_btw_sensors / 2) + 1, int(self._dist_btw_sensors / 2) - 1):
                        if i ** 2 + j ** 2 <= self._dist_btw_sensors ** 2:
                            count += 1
                            if self._is_valid_point_position([[x+i], [y+j]]):
                                sum += self._map[x + i][y + j]
                self._predicts[x][y] = round(sum / count * 3)

    def _find_center_line(self):
        self._center_line = np.zeros(self._map.shape)
        for x in range(int(self._dist_btw_sensors / 2), self._map.shape[0] - int(self._dist_btw_sensors / 2)):
            for y in range(int(self._dist_btw_sensors / 2), self._map.shape[1] - int(self._dist_btw_sensors / 2)):
                is_valid = True
                for i in range(-int(self._dist_btw_sensors / 2) + 1, int(self._dist_btw_sensors / 2) - 1):
                    for j in range(-int(self._dist_btw_sensors / 2) + 1, int(self._dist_btw_sensors / 2) - 1):
                        if i ** 2 + j ** 2 <= self._dist_btw_sensors ** 2:
                            if self._map[x + i][y + j] < 0.5:
                                is_valid = False
                if is_valid:
                    self._center_line[x][y] = 1


