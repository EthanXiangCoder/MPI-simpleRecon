import numpy as np 

from Phantom import *

'''create a 'P' shape matrix to simulate the MPI reconstruction'''

class Phantom_Shape_P(Phantom_Base):
    def __init__(self,temperature=20.0,diameter=30e-9,saturation_mag_core=8e5,concentration=5e7):
        super().__init__(diameter,saturation_mag_core,temperature,concentration)

    #code from https://github.com/XiaoYaoNet/MPIRF/tree/master/src/PhantomClass/PPhantom.py
    def get_Shape(self, x, y, concentration):  #注意次序 画出来的才是一个P 计算机坐标系和numpy数组维度是相反的

        self._X = x
        self._Y = y
        shape = np.zeros((self._X,self._Y))
        shape[int(x * (14 / 121)):int(x * (105 / 121)), int(y * (29 / 121)):int(y * (90 / 121))] =\
        np.ones((int(x * (105 / 121)) - int(x * (14 / 121)),int(y * (90 / 121)) - int(y * (29 / 121))))
        shape[int(x * (29 / 121)):int(x * (60 / 121)), int(y * (44 / 121)):int(y * (75 / 121))] =\
        np.zeros((int(x * (60 / 121)) - int(x * (29 / 121)),int(y * (75 / 121)) - int(y * (44 / 121))))
        shape[int(x * (74 / 121)):int(x * (105 / 121)), int(y * (44 / 121)):int(y * (90 / 121))] =\
        np.zeros((int(x * (105 / 121)) - int(x * (74 / 121)),int(y * (90 / 121)) - int(y * (44 / 121))))

        return shape * concentration
