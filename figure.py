import numpy as np
from shapely.geometry import Polygon


class Figure:

    def __init__(self, name):
        self.points = np.array([[], [], []])
        self.name = name

    def add_point(self, x, y):
        new_column = np.array([[x], [y], [1]])
        self.points = np.append(self.points, new_column, axis=1)

    def do_translation(self, x, y):
        translation_matrix = np.array([[1, 0, x],
                                       [0, 1, y],
                                       [0, 0, 1]])
        self.points = np.dot(translation_matrix, self.points)

    def do_rotation(self, angles, x, y):
        self.do_translation(-x, -y)

        radians = np.pi * angles / 180
        rotation_matrix = np.array([[np.cos(radians), -np.sin(radians), 0],
                                    [np.sin(radians), np.cos(radians), 0],
                                    [0, 0, 1]])
        self.points = np.dot(rotation_matrix, self.points)

        self.do_translation(x, y)

    def get_points_list(self):
        return_list = []
        for index in range(self.points.shape[1]):
            return_list.append((self.points[0, index], self.points[1,index]))
        return return_list


def check_intersection(figure1, figure2):
    p1 = Polygon(figure1.get_points_list())
    p2 = Polygon(figure2.get_points_list())
    return p1.intersects(p2)
