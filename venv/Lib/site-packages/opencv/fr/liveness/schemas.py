import enum
from typing import Optional, Union
import numpy as np
from PIL.Image import Image
from pathlib import Path
from .. import util as util 

class DeviceType(enum.Enum):
    DESKTOP = 'DESKTOP'
    ANDROID = 'ANDROID'
    IOS = 'IOS'

class LivenessRequest:
    '''A liveness request object
    
    :param os: OS setting to choose being either DeviceType.DESKTOP, DeviceType.ANDROID, or DeviceType.IOS
    :type os: Optional[DeviceType]
    :param image: image being either a numpy array (obtained with cv2.imread), a string (path to a file), a Pillow image (obtained with PIL.Image.open()), or a pathlib path
    :type image: Union[numpy.ndarray, str, PIL.Image.Image, pathlib.Path]
    '''
    def __init__(self, 
                image: Union[np.ndarray, str, Image, Path],
                os: Optional[DeviceType] = DeviceType.DESKTOP) -> None:
        self.os = os
        self.image = util.normalize_image(image)

    def to_dict(self) -> dict:
        '''
        Return a dictionary representation of this object

        :return: a dictionary representing this object
        :rtype: dict
        '''
        repr = {
            "os": self.os,
            "image": self.image
        }

        if isinstance(self.os, DeviceType):
            if self.os == DeviceType.DESKTOP:
                repr["os"] = "DESKTOP"
            elif self.os == DeviceType.ANDROID:
                repr["os"] = "ANDROID"
            elif self.os == DeviceType.IOS:
                repr["os"] = "IOS"
        else:
            repr["os"] = self.os

        return repr

    def __repr__(self) -> str:
        return str(self.to_dict())

    @property
    def os(self):
        '''OS setting to choose being either DESKTOP, ANDROID, or IOS'''
        return self._os

    @os.setter
    def os(self, value):
        if not isinstance(value, DeviceType):
            raise TypeError("os accepts only DeviceType.DESKTOP, DeviceType.ANDROID or DeviceType.IOS")
        self._os = value

class LivenessResponse:
    '''A liveness response object

    :param score: the score of the liveness
    :type score: float
    '''
    def __init__(self, score: float)->None:
        self.score = score

    @classmethod
    def from_dict(cls, obj:dict()):
        """Create a LivenessResponse from a dictionary

        :param obj: the dictionary representing this object
        :type obj:dict

        :return: a LivenessResponse object
        :rtype: LivenessResponse
        """
        if "liveness_score" in obj:
            return LivenessResponse(obj["liveness_score"])
        else:
            return None

    def __repr__(self) -> str:
        return str({
            "score": self.score
        })

