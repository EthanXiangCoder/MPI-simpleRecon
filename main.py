import matplotlib.pyplot as plt
from P_Phantom import *
from SM_simulation import *
from MDF_to_information import *
from examine import *
from system_matrix_recon import *

import os

def Simulation_1(PhantomType, 
                 T, D, Satur_M, C,
                 S_X, S_Y,
                 DF_X,DF_Y,DA_X,DA_Y,DP_X,DP_Y,
                 Time,Sample_F,
                 Iter,Theta,Delta):
    
    try:
        '''other phantom is not available'''
        if PhantomType == 0:  
            phantom = Phantom_Shape_P(temperature=T, diameter=D, saturation_mag_core=Satur_M, concentration=C)
    except:
        Exception("Phantom Module is broken !!!")
    
    try:
        simulation = SM_simulation(Phantom=phantom, 
                                   SelectionField_X=S_X, SelectionField_Y=S_Y,
                                   DriveField_XA=DA_X, DriveField_YA=DA_Y, DriveField_XF=DF_X, DriveField_YF=DF_Y, DriveField_XP=DP_X, DriveField_YP=DP_Y,
                                   Repeat_Time=Time, Sample_Frequency=Sample_F,
                                   concentration_delta_volume=Delta)
    except:
        Exception("Simulation Module is broken !!!")
    
    try:
        Information_examine(simulation.message)
    except:
        Exception("Examine Module is broken !!!")
    
    try:
        ImgData = SM_recon(simulation.message,Iter,Theta)
        result = ImgData.get_Image()[1][0]
    except:
        Exception("Reconstruction Module is broken !!!")

    return phantom.get_Shape(simulation._Y_num,simulation._X_num,phantom._concentration),result


if __name__ == "__main__":
    print("*" * 32)
    print("1: MPI Simulation based on System Matrix and Kaczmarz method (default 'P' shape)")
    print("2: MPI Simulation based on System Matrix and Moore-Penrose pseudoinverse (default 'P' shape)")
    print("3: MPI Simulation based on System Matrix and conjugate gradient normal residual method (default 'P' shape)")
    print("4: xxxxxxx")
    print("5: xxxxxxx")
    print("6: xxxxxxx")
    print("7: MPI Simulation based on System Matrix and All methods display (default 'P' shape)")
    print("Q: Quit")
    print("*" * 32)

    symbol  = input("select your own methods: ")
    default = ["1", "2", "3", "7", "Q"]

    while True:
        try:
            judge = symbol in default
            m = 1 / int(judge)
        except ZeroDivisionError:
            break
        if symbol == "Q":
            break
        if symbol == "1":
            phantom, image_result = Simulation_1(0,
                                                 20, 30e-9, 8e5, 5e7,
                                                 2.0, 2.0,
                                                 2500000.0/102.0, 2500000.0/96.0, 12e-3, 12e-3,
                                                 PI / 2.0,PI / 2.0,
                                                 6.528e-4,2.5e6,
                                                 20, 1e-6, 50e-3)
            
            plt.rcParams['font.sans-serif'] = ['FangSong']
            plt.rcParams['axes.unicode_minus'] = False

            plt.subplot(1, 2, 1)
            plt.title("Phantom")
            plt.imshow(phantom)

            plt.subplot(1, 2, 2)
            plt.title("Kaczmarz Method")
            plt.imshow(image_result)
            plt.show()

            print(phantom.shape, image_result.shape)

            break
            
