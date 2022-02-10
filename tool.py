import numpy as np


# [x,y,z] ===> [[x],[y],[z],[w]]
def v3_to_mr4c1(v3, w=1):
    return np.array([np.append(v3, w)]).T


# [[x],[y],[z],[w]] ===> [x,y,z]
def mr4c1_to_v3(mr4c1, normal=True):
    if normal:
        return mr4c1.T[0][:3] / mr4c1[3][0]
    else:
        return mr4c1.T[0][:3].copy()
