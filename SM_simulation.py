import numpy as np
import math

from Simulation_Base import *

PI = 3.1415926

class SM_simulation(SimulationBase):
    def __init__(self,
                Phantom,
                SelectionField_X=2.0,
                SelectionField_Y=2.0,
                DriveField_XA=12e-3,
                DriveField_YA=12e-3,
                DriveField_XF=2500000.0/102.0,
                DriveField_YF=2500000.0/96.0,
                DriveField_XP=PI / 2.0, 
                DriveField_YP=PI / 2.0, 
                Repeat_Time=6.528e-4,
                Sample_Frequency=2.5e6,
                concentration_delta_volume=50e-3
                ):
        
        super(SM_simulation,self).__init__(
                Phantom,
                SelectionField_X,
                SelectionField_Y,
                DriveField_XA,
                DriveField_YA,
                DriveField_XF,
                DriveField_YF,
                DriveField_XP, 
                DriveField_YP, 
                Repeat_Time,
                Sample_Frequency)
        
        #measurement-based approach
        self._concentration_delta_volume = concentration_delta_volume

        self._send_2_information('System Matrix') 
        self._translate_voltage()

    #get the aux signal(System Matrix)
    def _get_AuxSignal(self):
        '''in this SM_simulation.py file the aux_signal is the system matrix'''
        AuxSignal = np.zeros((self._sample_num,self._Y_num,self._X_num,2))

        Cover = np.ones((self._Y_num,self._X_num,2))
        Cover *= self._concentration_delta_volume
        Langevin = np.zeros((self._Y_num,self._X_num,2))
        for i in range(self._sample_num):
            coeff = (-1.0) * U0 * self._Sensiticity * self._phantom._particle_magnetic_moment * self._phantom._beta_coeff * self._Drive_Derivative_sequence[:,i]
            Langevin_function_derivative = (1.0 / ((self._Total_Field_Strength_length[:,:,i] * self._phantom._beta_coeff) ** 2)) - (1.0 / ((np.sinh(self._Total_Field_Strength_length[:,:,i] * self._phantom._beta_coeff)) ** 2))
            Langevin[:,:,0] = Langevin_function_derivative
            Langevin[:,:,1] = Langevin_function_derivative
            coeff_cover = np.tile(coeff,(self._Y_num,self._X_num,1))
            temp = Cover * Langevin
            AuxSignal[i,:,:,:] = temp * coeff_cover
        
        AuxSignal = np.reshape(AuxSignal,(self._sample_num,self._X_num*self._Y_num,2))
        AuxSignal /= self._concentration_delta_volume
        tempx = AuxSignal[:,:,0]
        tempy = AuxSignal[:,:,1]

        tempx = np.fft.fft(np.transpose(tempx) * 1e6)
        tempy = np.fft.fft(np.transpose(tempy) * 1e6)

        AuxSignal = np.transpose(np.add(tempx,tempy))

        return AuxSignal

    #reset the voltage to the Fourier Transform Format
    def _translate_voltage(self):
        # the shape of voltage is [2,sample_num]
        temp = np.zeros((self._sample_num,2))
        temp = np.fft.fft(self.message['Measurement']['Measure_Signal'] * 1e6,axis = 1)
        temp = np.transpose(temp)

        self.message['Measurement']['Measure_Signal'] = np.add(temp[:,0],temp[:,1]) #still have some questions


