from abc import ABC,abstractmethod

'''message抽象类'''

class Information_Class(ABC):
    def __init__(self):
        '''message初始化'''
        self.message = {
            'Particle_Porperty':{
                'Diameter':None,
                'Temperature':None,
                'Saturation_Mag':None
            },
            'Selection_Field':{
                'X_Gradient':None,
                'Y_Gradient':None,
                'Z_Gradient':None
            },
            'Drive_Field':{
                'X_Waveform':None,
                'Y_Waveform':None,
                'Z_Waveform':None,
                'RepeatTime':None,
                'WaveType':None
            },
            'Focus_Field':{
                'X_Direction':None,
                'Y_Direction':None,
                'Z_Direction':None,
                'WaveType':None,
            },
            'Sample':{
                'Topology':None,
                'Frequency':None,
                'Number':None,
                'BeginTime':None,
                'Sensetivity':None,
            },
            'Measurement':{
                'Type':None,
                'Background_Flag':None,
                'Measure_Signal':None,
                'Auxiliary_Signal':None,
                'Voxel_Number':None,
            }
        }

    def _get_item(self,messagefirst,messagesecond,content):
        self.message[messagefirst][messagesecond] = content
