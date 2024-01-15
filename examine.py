import numpy as np
import time

PI = 3.1416
KB = 1.3806488e-23
T_BASE = 273.15
U0 = 4.0 * PI *1e-7

class Information_examine():
    def __init__(self,message):
        self.Data_Cut(message)
        yes, str1, str2, = self.Data_Check(message)
        if yes is False:
            print("message_{first}_{second} have some problems".format(str1,str2))

    def data_check(self,varible,type):
        if isinstance(varible,type):
            return True
        elif type==float and isinstance(varible, int):
            return True
        else:
            return False
    
    def data_check_2(self,varible,type_list):
        if str(varible.dtype) in type_list:
            return True
        else:
            return False
        
    def data_check_3(self,varible,type_list,type_list_2):
        if str(varible.dtype) in type_list or str(varible.dtype) in type_list_2:
            return True
        else:
            return False
    
    def Data_Check(self,message):
        '''
            check the type 

        ''' 
        # Part1: Particle Porperty
        if not message['Particle_Porperty']['Diameter'] is None:
            flag = self.data_check(message['Particle_Porperty']['Diameter'], float)
            if flag == False:
                return False,'Particle_Porperty','Diameter'

        if not message['Particle_Porperty']['Temperature'] is None:
            flag = self.data_check(message['Particle_Porperty']['Temperature'], float)
            if flag == False:
                return False,'Particle_Porperty','Temperature'     

        if not message['Particle_Porperty']['Saturation_Mag'] is None:
            flag = self.data_check(message['Particle_Porperty']['Saturation_Mag'], float)
            if flag == False:
                return False,'Particle_Porperty','Saturation_Mag'    

        # Part2: Selection Field
        if not message['Selection_Field']['X_Gradient'] is None:
            flag = self.data_check(message['Selection_Field']['X_Gradient'],float)
            if flag == False:
                return False,'Selection_Field','X_Gradient' 

        if not message['Selection_Field']['Y_Gradient'] is None:
            flag = self.data_check(message['Selection_Field']['Y_Gradient'],float)
            if flag == False:
                return False,'Selection_Field','Y_Gradient'

        if not message['Selection_Field']['Z_Gradient'] is None:
            flag = self.data_check(message['Selection_Field']['Z_Gradient'],float)
            if flag == False:
                return False,'Selection_Field','Z_Gradient'

        # Part3: Drive Field
        if not message['Drive_Field']['X_Waveform'] is None:
            flag = self.data_check_2(message['Drive_Field']['X_Waveform'],["float","float32","float64","float128"])
            if flag == False:
                return False,'Drive_Field','X_Waveform'
            
        if not message['Drive_Field']['Y_Waveform'] is None:
            flag = self.data_check_2(message['Drive_Field']['Y_Waveform'],["float","float32","float64","float128"])
            if flag == False:
                return False,'Drive_Field','Y_Waveform'
        
        if not message['Drive_Field']['Z_Waveform'] is None:
            flag = self.data_check_2(message['Drive_Field']['Z_Waveform'],["float","float32","float64","float128"])
            if flag == False:
                return False,'Drive_Field','Z_Waveform'
        
        if not message['Drive_Field']['RepeatTime'] is None:
            flag = self.data_check(message['Drive_Field']['RepeatTime'],float)
            if flag == False:
                return False,'Drive_Field','RepeatTime'
        
        if not message['Drive_Field']['WaveType'] is None:
            flag = self.data_check(message['Drive_Field']['WaveType'],str)
            if flag == False:
                return False,'Drive_Field','WaveType'
        
        # Part4: Focus Field
        if not message['Focus_Field']['X_Direction'] is None:
            flag = self.data_check_2(message['Focus_Field']['X_Direction'],["float","float32","float64","float128"])
            if flag == False:
                return False,'Focus_Field','X_Direction'
        
        if not message['Focus_Field']['Y_Direction'] is None:
            flag = self.data_check_2(message['Focus_Field']['Y_Direction'],["float","float32","float64","float128"])
            if flag == False:
                return False,'Focus_Field','Y_Direction'
        
        if not message['Focus_Field']['Z_Direction'] is None:
            flag = self.data_check_2(message['Focus_Field']['Z_Direction'],["float","float32","float64","float128"])
            if flag == False:
                return False,'Focus_Field','Z_Direction'
            
        if not message['Focus_Field']['WaveType'] is None:
            flag = self.data_check(message['Focus_Field']['WaveType'],str)
            if flag == False:
                return False,'Focus_Field','WaveType'
            
        # Part5: Information about Sample
        if not message['Sample']['Topology'] is None:
            flag = self.data_check(message['Sample']['Topology'],str)
            if flag == False:
                return False,'Sample','Topology'

        if not message['Sample']['Frequency'] is None:
            flag = self.data_check(message['Sample']['Frequency'],float)
            if flag == False:
                return False,'Sample','Frequency'

        if not message['Sample']['Number'] is None:
            flag = self.data_check(message['Sample']['Number'],int)
            if flag == False:
                return False,'Sample','Number'

        if not message['Sample']['BeginTime'] is None:
            flag = self.data_check(message['Sample']['BeginTime'],float)
            if flag == False:
                return False,'Sample','BeginTime'

        if not message['Sample']['Sensetivity'] is None:
            flag = self.data_check(message['Sample']['Sensetivity'],float)
            if flag == False:
                return False,'Sample','Sensetivity'
        
        # Part6: Information about Measurement
        if not message['Measurement']['Type'] is None:
            flag = self.data_check(message['Measurement']['Type'],str)
            if flag == False:
                return False,'Measurement','Type'
        
        if not message['Measurement']['Background_Flag'] is None:
            flag = self.data_check_3(message['Measurement']['Background_Flag'],['bool'],['int','int16','int32','int64'])
            if flag == False:
                return False,'Measurement','Background_Flag'
            
        if not message['Measurement']['Measure_Signal'] is None:
            flag = self.data_check_3(message['Measurement']['Measure_Signal'],['complex64','complex128'],['float','float32','float64','float128'])
            if flag == False:
                return False,'Measurement','Measure_Signal'
        
        if not message['Measurement']['Auxiliary_Signal'] is None:
            flag = self.data_check_3(message['Measurement']['Auxiliary_Signal'],['complex64','complex128'],['float','float32','float64','float128'])
            if flag == False:
                return False,'Measurement','Auxiliary_Signal'
        
        if not message['Measurement']['Voxel_Number'] is None:
            flag = self.data_check_2(message['Measurement']['Voxel_Number'],['int','int16','int32','int64'])
            if flag == False:
                return False,'Measurement','Voxel_Number'
        
        return True,'',''
    
    def Data_Normalization(self,message):
        '''
        this function is useless until we use it
        '''

        message['Measurement']['Measure_Signal'] /= KB

        if not message['Sample']['Sensetivity'] is None:
            message['Measurement']['Measure_Signal'] /= message['Sample']['Sensetivity']

        if (not message['Particle_Porperty']['Diameter'] is None) and (not message['Particle_Porperty']['Saturation_Mag'] is None):
            m = message['Particle_Porperty']['Saturation_Mag'] * (message['Particle_Porperty']['Diameter'] ** 3) * PI / 6.0
            message['Measurement']['Measure_Signal'] /= m

            if not message['Particle_Porperty']['Temperature'] is None:
                b = U0 * m / (message['Particle_Porperty']['Temperature'] * KB)
                message['Measurement']['Measure_Signal'] /= b

    def Data_Cut(self,message):
        '''
            this function is prepared for the data_cut of the MDF Format
        '''
        pass
