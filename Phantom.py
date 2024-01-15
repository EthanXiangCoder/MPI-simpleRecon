import numpy as np 

from abc import ABC,abstractmethod

PI = 3.1415926
T_BASE = 273.15
U0 = 4.0 * PI *1e-7
KB = 1.3806488e-23

''' create a phantom
    这部分借鉴了MPIRF的想法 最开始只是想设置一个仿真形状 但为了后续好进行拓展 于是设置一个抽象类
'''

class Phantom_Base(ABC):
    def __init__(self,diameter,saturation_mag_core,temperature,concentration): #区别与Information 这里的Phantom一定要包含一个假定的浓度信息
        self._diameter = diameter
        self._temperature = temperature+T_BASE #Kelvin Temperature
        self._particle_volume = self.__get_volume()
        self._saturation_mag_core = saturation_mag_core
        self._particle_magnetic_moment = self.__get_particle_magnetic()
        self._concentration = concentration
        self._beta_coeff = self.__get_beta_coeff()

        self._Picture = None
        self._X = None
        self._Y = None
        
    #calculate the volume of particle
    def __get_volume(self):
        return PI*(self._diameter**3) / 6.0
    
    #calculate the magnetic moment of a single particle
    def __get_particle_magnetic(self):
        return self._particle_volume*self._saturation_mag_core

    #calculate the coeff of beta (Langevin Function)
    def __get_beta_coeff(self):
        return U0 * self._particle_magnetic_moment/(KB * self._temperature)
    
    #return the phantom matrix
    '''this function is open for the visitors'''
    def get_Phantom(self):
        return self._Picture
    
    @abstractmethod
    def get_Shape(self,x,y,concentration):
        pass
