import numpy as np
import h5py
from Information_Base import *

'''MDF File Reader Derived from ReaderBase.py'''

class MDFReader(Information_Class):
    '''MDF File Reader'''
    def __init__(self,smfilepath,meafilepath):
        super(MDFReader,self).__init__()
        self.__SMFilePath = smfilepath
        self.__MeasurementFilePath = meafilepath
        self._create_FILE()
        self._load_content()
    
    def _create_FILE(self):
        "create a h5 file"
        try:
            self.SMFile = h5py.file(self.__SMFilePath,'r')
            self.MEAFile = h5py.file(self.__MeasurementFilePath,"r")
        except Exception:
            print("can not open the filepath!!!")
            raise Exception
        
    '''这里因为各项数据的数据类型不一致 不写在一个函数中 而是单独分开进行提取'''

    def __get_samplepointnumber(self):
        content = self.SMFile['/acquisition/receiver/numSamplingPoints']
        return int(np.array(content,dtype=np.int32)) #就是一个数
    
    def __get_measure_type(self):
        pass #这部分不用写 直接赋值即可 MDF决定了重建方法是系统矩阵
        return 1

    def __get_background_flag(self):
        content = self.SMFile['/measurement/isBackgroundFrame']
        return content[:].view(bool) #N一维数组

    def __get_measurement_signal(self):
        content = self.SMFile['/measurement/data']
        return content[:,:,:,:] #四维数据
    
    def __get_auxsignal(self):
        content = self.SMFile['/measurement/data']
        return content[:,:,:,:].squeeze()
    
    def __get_voxel_number(self):
        content = self.SMFile['/calibration/size']
        return content[:,:] #目前是只有二维 后续可以调整

    def _load_content(self):
        '''load the necessary content about the reconstruction'''

        self.__get_item('Sample','Number',self.__get_samplepointnumber)
        self.__get_item('Measurement','Type',self.__get_measure_type)
        self.__get_item('Measurement','Background_Flag',self.__get_background_flag)
        self.__get_item('Measurement','Measure_Signal',self.__get_measurement_signal)
        self.__get_item('Measurement','Auxiliary_Signal',self.__get_auxsignal)
        self.__get_item('Measurement','Voxel_Number',self.__get_voxel_number)


