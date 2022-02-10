import numpy as np
import os

import tool


class Camera(object):

    def __init__(self, file_path):
        # input
        with open(os.path.split(os.path.realpath(__file__))[0] + os.sep + file_path) as file:
            line_list = file.readlines()
        for line in line_list:
            line_split = line.split()
            if line_split[0] == "C":
                self.c = np.array([float(line_split[1]), float(line_split[2]), float(line_split[3])])
            elif line_split[0] == "P_{ref}":
                self.p_ref = np.array([float(line_split[1]), float(line_split[2]), float(line_split[3])])
            elif line_split[0] == "V\'":
                self.v_prime = np.array([float(line_split[1]), float(line_split[2]), float(line_split[3])])
            elif line_split[0] == "h":
                self.h = float(line_split[1])
            elif line_split[0] == "d":
                self.d = float(line_split[1])
            elif line_split[0] == "f":
                self.f = float(line_split[1])
            elif line_split[0] == "remove_back_face":
                if line_split[1] == "0":
                    self.remove_back_face = False
                else:
                    self.remove_back_face = True
        self.n = None
        self.u = None
        self.v = None
        self.r = None
        self.t = None
        self.m_view = None

        self.m_pers = None
        self.m_camera = None
        self.calculate_parameter()

    def set(self, c=None, p_ref=None, v_prime=None, h=None, d=None, f=None):
        if c is not None:
            self.c = np.array(c)
        if p_ref is not None:
            self.p_ref = np.array(p_ref)
        if v_prime is not None:
            self.v_prime = np.array(v_prime)
        if h is not None:
            self.h = h
        if d is not None:
            self.d = d
        if f is not None:
            self.f = f
        self.calculate_parameter()

    def calculate_parameter(self):
        temp = self.p_ref - self.c
        self.n = temp / np.linalg.norm(temp, 2)
        temp = np.cross(self.n, self.v_prime)
        self.u = temp / np.linalg.norm(temp, 2)
        self.v = np.cross(self.u, self.n)
        self.r = np.eye(4)
        self.r[0][:3] = self.u
        self.r[1][:3] = self.v
        self.r[2][:3] = self.n
        self.t = np.eye(4)
        self.t[0][3] = -self.c[0]
        self.t[1][3] = -self.c[1]
        self.t[2][3] = -self.c[2]
        self.m_view = np.dot(self.r, self.t)
        self.m_pers = np.zeros((4, 4))
        self.m_pers[0][0] = self.d / self.h
        self.m_pers[1][1] = self.d / self.h
        self.m_pers[2][2] = self.f / (self.f - self.d)
        self.m_pers[2][3] = -self.d * self.m_pers[2][2]
        self.m_pers[3][2] = 1
        self.m_camera = np.dot(self.m_pers, self.m_view)

    def world_to_screen(self, v3):
        return tool.mr4c1_to_v3(np.dot(self.m_camera, tool.v3_to_mr4c1(v3)))
