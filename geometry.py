import os
import numpy as np

from camera import *


class Geometry(object):

    def __init__(self, file_path):
        self.screen_point_list = []
        self.world_point_list = []
        self.polygon_list = []
        with open(os.path.split(os.path.realpath(__file__))[0] + os.sep + file_path) as file:
            line_list = file.readlines()
        line = line_list[0].split()
        point_number = int(line[1])
        polygon_number = int(line[2])
        for i in range(1, 1 + point_number):
            line = line_list[i].split()
            self.world_point_list.append(np.array([float(line[0]), float(line[1]), float(line[2])]))
        for i in range(1 + point_number, 1 + point_number + polygon_number):
            line = line_list[i].split()
            point_index_list = []
            for j in range(1, len(line)):
                point_index_list.append(int(line[j]) - 1)
            p0p1 = self.world_point_list[point_index_list[1]] - self.world_point_list[point_index_list[0]]
            p1p2 = self.world_point_list[point_index_list[2]] - self.world_point_list[point_index_list[1]]
            normal_vector = np.cross(p1p2, p0p1)
            render = True
            polygon = [point_index_list, normal_vector, render]
            self.polygon_list.append(polygon)

    def world_to_screen(self, camera):
        for point in self.world_point_list:
            self.screen_point_list.append(camera.world_to_screen(point))
        if camera.remove_back_face:
            for polygon in self.polygon_list:
                if np.dot(camera.n, polygon[1]) >= 0:
                    polygon[2] = False
