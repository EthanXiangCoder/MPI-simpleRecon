import numpy as np
import math
from abc import ABC,abstractmethod

from Information_Base import *

'''开始是不打算设置一个抽象类完成仿真重建的重写操作的 但一些Information的部分可以重复使用 并且单独写一个会不容易出错'''

PI = 3.1416
KB = 1.3806488e-23
T_BASE = 273.15
U0 = 4.0 * PI *1e-7


class SimulationBase(Information_Class,ABC):
    def __init__(self,
                Phantom,
                SelectionField_X,
                SelectionField_Y,
                DriveField_XA,
                DriveField_YA,
                DriveField_XF,
                DriveField_YF,
                DriveField_XP, #Phase PI/2.0之类的格式
                DriveField_YP, 
                Repeat_Time,
                Sample_Frequency):
        super().__init__()

        self._phantom = Phantom #phantom class instance

        self._Sensiticity = 1.0 #coil sensitivity

        #selection field property
        self._selection_x = SelectionField_X/U0 #MPI中都会使用除以U0的通用单位
        self._selection_y = SelectionField_Y/U0
        self._selection_gradient = np.array([[self._selection_x],[self._selection_y]]) 

        #drive field property
        self._drive_x_a = DriveField_XA/U0
        self._drive_y_a = DriveField_YA/U0
        self._drive_x_f = DriveField_XF
        self._drive_y_f = DriveField_YF
        self._drive_x_p = DriveField_XP
        self._drive_y_p = DriveField_YP
        self._drive_repeat_time = Repeat_Time 

        #message['Sample']
        self._sample_frequency = Sample_Frequency
        self._sample_num = round(self._drive_repeat_time*self._sample_frequency)

        #采样区间边界
        self._max_X = self._drive_x_a/self._selection_x
        self._max_Y = self._drive_y_a/self._selection_y

        #采样列表
        self.move_step_size = 1e-4
        self._Xsequence = np.arange(-self._max_X,self._max_X+self.move_step_size,self.move_step_size)
        self._Ysequence = np.arange(-self._max_Y,self._max_Y+self.move_step_size,self.move_step_size)
        self._X_num = len(self._Xsequence)
        self._Y_num = len(self._Ysequence)

        #采样时间列表
        self._Tsequence = np.arange(0,self._drive_repeat_time+self._drive_repeat_time/self._sample_num,self._drive_repeat_time/self._sample_num)

        #计算所有时刻的驱动场场强
        self._X_Drive_sequence,self._X_Drive_Derivative_sequence = self.__Calculate_DriveField_Value(self._drive_x_a,self._drive_x_f,self._drive_x_p,self._Tsequence)
        self._Y_Drive_sequence,self._Y_Drive_Derivative_sequence = self.__Calculate_DriveField_Value(self._drive_y_a,self._drive_y_f,self._drive_y_p,self._Tsequence)
        self._Drive_sequence = np.array([self._X_Drive_sequence,self._Y_Drive_sequence])
        self._Drive_Derivative_sequence = np.array([self._X_Drive_Derivative_sequence,self._Y_Drive_Derivative_sequence])

        #计算所有时刻的FFP位置
        self._Ordinate = np.divide(self._Drive_sequence,np.tile(self._selection_gradient,(1,np.shape(self._Drive_sequence)[1]))) #没乘上-1 不是直接算的磁场强度
        self._Ordinate = (-1) * self._Ordinate
        self._X_Ordinate = self._Ordinate[0]
        self._Y_Ordinate = self._Ordinate[1]

        self._Ordinate = self.__Mapping()

    #计算驱动场在指定时间的场强 
    def __Calculate_DriveField_Value(self,Amplitude,Frequency,phase,Tsequence):
        Drive_sequence = Amplitude * np.cos(2.0 * PI * Frequency * Tsequence + phase) * (-1.0) #即正弦波
        Drive_Derivative_sequence = Amplitude * 2.0 * PI * Frequency * np.sin(2.0 * PI * Frequency * Tsequence + phase) #为什么这里没有设置自由的相位 因为想最开始的位置处于0的地方
        return Drive_sequence,Drive_Derivative_sequence

    #坐标转换 其实也就是两步 电脑坐标系映射(随便搜就能看到) 将原来的坐标进行缩放 因为设置了比较小的步长
    def __Mapping(self):
        self._Ordinate[0] += self._max_X
        self._Ordinate[1] -= self._max_Y
        self._Ordinate[1] *= -1

        self._Ordinate *= (1/self.move_step_size)

        return np.around(self._Ordinate)+1
    
    # 根据画出的图形进行坐标系转换计算每个位置的梯度场强度 计算机坐标系和array维度顺序不相同 后续改进时请注意
    def __init_Gradient_mag(self):
        self._phantom._Picture = self._phantom.get_Shape(self._Y_num,self._X_num,self._phantom._concentration)
        Seletion_Mag = np.zeros((self._Y_num,self._X_num,2))
        for i in range(self._Y_num):
            y = (-1) * (i * self.move_step_size) + self._max_Y
            for j in range(self._X_num):
                x = j * self.move_step_size - self._max_X
                magnetic = self._selection_gradient * [[x],[y]]
                Seletion_Mag[i,j,0] = magnetic[0]
                Seletion_Mag[i,j,1] = magnetic[1]
        #self._sample_num += 1
        return Seletion_Mag  
    
    '''calculate the voltage of magnetic particle using CPU 
       (Knopp T, Gdaniec N, Moddel M. Magnetic particle imaging:from proof of principle to preclinical applications. Phys MedBiol. 2017;62(14):R124-R178.)
    '''
    def _get_Voltage(self):
        seletion_mag = self.__init_Gradient_mag()

        voltage = np.zeros((2, self._sample_num))

        self._Total_Field_Strength_length = np.zeros((self._Y_num, self._X_num, self._sample_num))

        for i in range(self._sample_num):
            coeff = (-1.0) * U0 * self._Sensiticity * self._phantom._particle_magnetic_moment * self._phantom._beta_coeff * self._Drive_Derivative_sequence[:,i]
            drive_field_strength = np.tile(self._Drive_sequence[:,i],(self._Y_num,self._X_num,1))
            total_field_strength = np.add(drive_field_strength, seletion_mag)
            self._Total_Field_Strength_length[:,:,i] = np.sqrt(total_field_strength[:,:,0] ** 2 + total_field_strength[:,:,1] ** 2)
            Langevin_function_derivative = (1.0 / ((self._Total_Field_Strength_length[:,:,i] * self._phantom._beta_coeff) ** 2)) - (1.0 / ((np.sinh(self._Total_Field_Strength_length[:,:,i] * self._phantom._beta_coeff)) ** 2))
            Langevin_sequence = np.zeros((self._Y_num,self._X_num,2))
            Langevin_sequence[:,:,0] = Langevin_function_derivative
            Langevin_sequence[:,:,1] = Langevin_function_derivative
            '''这里用矩阵计算积分 希望读者在这里能自己画图理解一下'''
            #截至目前为止，Langevin_sequence的维度为y，x，2  phantom的shape的形状为y,x
            Phantom_shape = np.tile(np.transpose(self._phantom._Picture),(2,1,1))
            Phantom_shape = np.transpose(Phantom_shape)
            coeff_large = np.tile(coeff,(self._Y_num,self._X_num,1))
            Phantom_integral = Phantom_shape * Langevin_sequence
            Signal = Phantom_integral * coeff_large

            voltage[0,i] = np.sum(Signal[:,:,0]) #这里根据驱动场的x和y来判断
            voltage[1,i] = np.sum(Signal[:,:,1])
        
        return voltage

    @abstractmethod
    def _get_AuxSignal(self):
        pass

    def _get_Signal(self):

        voltage = self._get_Voltage()
        aux_signal = self._get_AuxSignal()

        return voltage, aux_signal
    
    #初始化仿真相关数据
    def _send_2_information(self,aux_type):
        voltage,aux_signal = self._get_Signal()

        self._get_item('Particle_Porperty','Diameter',self._phantom._diameter)
        self._get_item('Particle_Porperty','Temperature',self._phantom._temperature)
        self._get_item('Particle_Porperty','Saturation_Mag',self._phantom._saturation_mag_core)

        self._get_item('Selection_Field','X_Gradient',self._selection_x)
        self._get_item('Selection_Field','Y_Gradient',self._selection_y)
        
        self._get_item('Drive_Field','X_Waveform',np.array([self._drive_x_a,self._drive_x_f,self._drive_x_p]))
        self._get_item('Drive_Field','Y_Waveform',np.array([self._drive_y_a,self._drive_y_f,self._drive_y_p]))
        self._get_item('Drive_Field','RepeatTime',self._drive_repeat_time)
        self._get_item('Drive_Field','WaveType','cos')

        self._get_item('Sample','Topology','FFP')
        self._get_item('Sample','Frequency',self._sample_frequency)
        self._get_item('Sample','Number',self._sample_num)
        self._get_item('Sample','BeginTime',None)
        self._get_item('Sample','Sensetivity',self._Sensiticity)

        self._get_item('Measurement','Type',aux_type)
        self._get_item('Measurement','Background_Flag',np.ones(np.shape(voltage),dtype = 'bool'))
        self._get_item('Measurement','Measure_Signal',voltage)
        self._get_item('Measurement','Auxiliary_Signal',aux_signal)
        self._get_item('Measurement','Voxel_Number',np.array([self._X_num,self._Y_num],dtype = 'int64'))
        































