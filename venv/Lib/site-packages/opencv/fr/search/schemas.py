import enum
from ..persons.schemas import Person
from typing import List, Union, Optional
import numpy as np
from PIL.Image import Image
from pathlib import Path
import datetime
from .. import util as util
from .. liveness.schemas import DeviceType

class SearchMode(enum.Enum):
    ACCURATE = 'ACCURATE'
    FAST = 'FAST'

class SearchRequest:
    """A search request object

    :param collection_id: the collection id to restrict the search
    :type collection_id:str
    :param images: a list of images (max 3), with each image being either a numpy array (obtained with cv2.imread), a string (path to a file), a Pillow image (obtained with PIL.Image.open()), or a pathlib path
    :type images:List[Union[numpy.ndarray, str, PIL.Image.Image, pathlib.Path]]
    :param min_score: a minimum score to match the person, defaults to 0.7
    :type min_score: Optional[float]
    :param search_mode: the model to search FAST or ACCURATE, defaults to FAST
    :type search_mode: Optional[SearchMode]
    """
    def __init__(self, 
                images: List[Union[np.ndarray, str, Image, Path]],
                collection_id: Optional[str] = None,
                min_score:Optional[float] = 0.7,
                search_mode:Optional[SearchMode] = SearchMode.FAST) -> None:
        
        self.collection_id = collection_id
        self.images = images
        self.images = util.normalize_images(images)
        self.min_score = min_score
        self.search_mode = search_mode

    def to_dict(self) -> dict:
        '''
        Return a dictionary representation of this object

        :return: a dictionary representing this object
        :rtype: dict
        '''
        repr = {
            "images": self.images,
            "min_score": self.min_score,
            "collection_id": self.collection_id
        }

        if isinstance(self.search_mode, SearchMode):
            if self.search_mode == SearchMode.FAST:
                repr["search_mode"] = "FAST"
            else:
                repr["search_mode"] = "ACCURATE"
        else:
            repr["search_mode"] = self.search_mode


        return repr

    def __repr__(self) -> str:
        return str({
            "collection_id": self.collection_id,
            "images": self.images,
            "min_score": self.min_score,
            "search_mode": self.search_mode
        })

    @property
    def collection_id(self):
        '''Collection id to search for a person'''
        return self._collection_id

    @collection_id.setter
    def collection_id(self, value):
        if isinstance(value, str) and len(value) == 0:
            raise ValueError("collection_id must be a non-empty string or None")
        elif value is not None and not isinstance(value, str):
            raise TypeError("collection_id must be a non-empty string or None")
        self._collection_id = value

    @property
    def min_score(self):
        '''Minimum score to match a person'''
        return self._min_score

    @min_score.setter
    def min_score(self, value):
        if isinstance(value, float) and (value <0 or value > 1.0):
            raise ValueError("min_score must be a float number between 0 and 1")
        elif not isinstance(value, float):
            raise TypeError("min_score must be a float number")
        self._min_score = value

    @property
    def search_mode(self):
        '''The model to use for a search'''
        return self._search_mode

    @search_mode.setter
    def search_mode(self, value):
        if not isinstance(value, SearchMode):
            raise TypeError("search_mode accepts only SearchMode.FAST or SearchMode.ACCURATE")
        self._search_mode = value

class PersonSearchResult:
    '''A Person and an associated similarity score
    
    :param person: the person
    :type person: Person
    :param score: the similarity score
    :type score: float
    '''
    def __init__(self, person:Person, score:float) -> None:
        self.person = person
        self.score = score

    @classmethod
    def from_dict(cls, obj:dict):
        """Get a person search result initialized from a dict

        :param obj: the dictionary representing this object
        :type obj:dict

        :return: a PersonSearchResult object
        :rtype: PersonSearchResult
        """
        return PersonSearchResult(Person.from_dict(obj), obj["score"])

    def __repr__(self) -> str:
        return "{" + '''"person": {}, "score": {}'''.format(self.person, self.score) + "}"

    def to_dict(self) -> dict:
        '''
        Return a dictionary representation of this object

        :return: a dictionary representing this object
        :rtype: dict
        '''
        return {
            "person": self.person,
            "score": self.score
        }

class SearchOptions:
    '''Class to specify search options
    
    :param collection_id: the collection id to restrict the search
    :type collection_id: str
    :param min_score: a minimum score to optionally search 
        for a person, defaults to 0.7
    :type min_score: Optional[float]
    :param search_mode: the mode to use for the SearchMode.FAST 
        or SearchMode.ACCURATE, defaults to FAST
    :type search_mode: Optional[SearchMode]
    '''
    def __init__(self, collection_id: Optional[str] = None, 
                 min_score:Optional[float] = 0.7, 
                 search_mode:Optional[SearchMode] = SearchMode.FAST) -> None:
        self.collection_id = collection_id
        self.min_score = min_score
        self.search_mode = search_mode

    @property
    def collection_id(self):
        '''Collection id to search for a person'''
        return self._collection_id

    @collection_id.setter
    def collection_id(self, value):
        if isinstance(value, str) and len(value) == 0:
            raise ValueError("collection_id must be a non-empty string or None")
        elif value is not None and not isinstance(value, str):
            raise TypeError("collection_id must be a non-empty string or None")
        self._collection_id = value

    @property
    def min_score(self):
        '''Minimum score to match a person'''
        return self._min_score

    @min_score.setter
    def min_score(self, value):
        if isinstance(value, float) and (value <0 or value > 1.0):
            raise ValueError("min_score must be a float number between 0 and 1")
        elif not isinstance(value, float):
            raise TypeError("min_score must be a float number")
        self._min_score = value

    @property
    def search_mode(self):
        '''The model to use for a search'''
        return self._search_mode

    @search_mode.setter
    def search_mode(self, value):
        if not isinstance(value, SearchMode):
            raise TypeError("search_mode accepts only SearchMode.FAST or SearchMode.ACCURATE")
        self._search_mode = value

    def to_dict(self) -> dict:
        '''
        Return a dictionary representation of this object

        :return: a dictionary representing this object
        :rtype: dict
        '''
        repr = {
            "collection_id": self.collection_id,
            "min_score": self.min_score
        }

        if isinstance(self.search_mode, SearchMode):
            if self.search_mode == SearchMode.FAST:
                repr["search_mode"] = "FAST"
            else:
                repr["search_mode"] = "ACCURATE"
        else:
            repr["search_mode"] = self.search_mode


        return repr

class DetectionRequest:
    '''A detect object
    
    :param image: image being either a numpy array (obtained with cv2.imread), a string (path to a file), a Pillow image (obtained with PIL.Image.open()), or a pathlib path
    :type image: Union[numpy.ndarray, str, PIL.Image.Image, pathlib.Path]
    :param search_options: optional search options, defaults to None. If not specified, the search will not be performed
    :type search_options: SearchOptions
    '''
    def __init__(self, 
                image: Union[np.ndarray, str, Image, Path],
                search_options: Optional[SearchOptions] = None) -> None:
        self.image = util.normalize_image(image)
        self.search_options = search_options

    def to_dict(self) -> dict:
        '''
        Return a dictionary representation of this object

        :return: a dictionary representing this object
        :rtype: dict
        '''
        repr = {
            "image": self.image
        }

        if isinstance(self.search_options, SearchOptions):
            repr["search"] = self.search_options.to_dict()

        return repr

    def __repr__(self) -> str:
        return str(self.to_dict())

    @property
    def image(self):
        '''Image to be detected'''
        return self._image

    @image.setter
    def image(self, value):
        self._image = util.normalize_image(value)

    @property
    def search_options(self):
        '''Search options'''
        return self._search_options

    @search_options.setter
    def search_options(self, value):
        if not isinstance(value, SearchOptions) and not value is None:
            raise TypeError("search_options must be of type SearchOptions or None")
        self._search_options = value

class Box:
    '''A bounding box

    :param left: left ordinate
    :type left: int
    :param top: top ordinate
    :type top: int
    :param right: right ordinate
    :type right: int
    :param bottom: bottom ordinate
    :type bottom: int
    '''
    def __init__(self, left: int, top: int, right: int, bottom: int) -> None:
        self.left = left
        self.top = top
        self.right = right
        self.bottom = bottom

    @classmethod
    def from_dict(cls, d: dict) -> 'Box':
        '''
        Create a Box from a dictionary

        :param d: a dictionary representing a Box
        :type d: dict
        :return: a Box object
        :rtype: Box
        '''
        return Box(d["left"], d["top"], d["right"], d["bottom"])

    def to_dict(self) -> dict:
        '''
        Return a dictionary representation of this object

        :return: a dictionary representing this object
        :rtype: dict
        '''
        return {
            "left": self.left,
            "top": self.top,
            "right": self.right,
            "bottom": self.bottom
        }

    def __repr__(self) -> str:
        return str(self.to_dict())

class Coordinate:
    '''A coordinate

    :param x: x ordinate
    :type x: int
    :param y: y ordinate
    :type y: int
    '''
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    @classmethod
    def from_list(cls, l: list) -> 'Coordinate':
        '''
        Create a Coordinate from a list

        :param l: a list representing a Coordinate
        :type l: list
        :return: a Coordinate object
        :rtype: Coordinate
        '''
        return Coordinate(l[0], l[1])

    def to_list(self) -> list:
        '''
        Return a list representation of this object

        :return: a list representing this object
        :rtype: list
        '''
        return [self.x, self.y]

    def __repr__(self) -> str:
        return str(self.to_list())

class Landmarks:
    '''Landmarks of a face

    :param left_eye: left eye
    :type left_eye: Coordinate
    :param right_eye: right eye
    :type right_eye: Coordinate
    :param nose: nose
    :type nose: Coordinate
    :param left_mouth: left mouth
    :type left_mouth: Coordinate
    :param right_mouth: right mouth
    :type right_mouth: Coordinate
    '''
    def __init__(self, left_eye:Coordinate, right_eye:Coordinate, nose: Coordinate, left_mouth: Coordinate, right_mouth: Coordinate) -> None:
        self.left_eye = left_eye
        self.right_eye = right_eye
        self.nose = nose
        self.left_mouth = left_mouth
        self.right_mouth = right_mouth

    @classmethod
    def from_dict(cls, d: dict) -> 'Landmarks':
        '''
        Create a Landmarks from a dictionary

        :param d: a dictionary representing a Landmarks
        :type d: dict
        :return: a Landmarks object
        :rtype: Landmarks
        '''
        return Landmarks(Coordinate.from_list(d["left_eye"]), 
                         Coordinate.from_list(d["right_eye"]), 
                         Coordinate.from_list(d["nose"]), 
                         Coordinate.from_list(d["left_mouth"]), 
                         Coordinate.from_list(d["right_mouth"]))

    def to_dict(self) -> dict:
        '''
        Return a dictionary representation of this object

        :return: a dictionary representing this object
        :rtype: dict
        '''
        return {
            "left_eye": self.left_eye.to_list(),
            "right_eye": self.right_eye.to_list(),
            "nose": self.nose.to_list(),
            "left_mouth": self.left_mouth.to_list(),
            "right_mouth": self.right_mouth.to_list()
        }

    def __repr__(self) -> str:
        return str(self.to_dict())

class DetectionResponseItem:
    '''A detection response item (one face) of a detection response
    which consists of a bounding box, landmarks, thumbnail, detection score, and list of matching persons

    :param box: bounding box
    :type box: Box
    :param landmarks: landmarks
    :type landmarks: Landmarks
    :param thumbnail: thumbnail
    :type thumbnail: Image
    :param score: detection score
    :type score: float
    :param persons: list of matching persons
    :type persons: List[PersonSearchResult]
    '''
    def __init__(self, 
                 box:Box,
                 landmarks: Landmarks,
                 thumbnail: Image,
                 detection_score: float,
                 persons: List[PersonSearchResult])->None:
        self.box = box
        self.landmarks = landmarks
        self.thumbnail = thumbnail
        self.detection_score = detection_score
        self.persons = persons

    @classmethod
    def from_dict(cls, d: dict) -> 'DetectionResponseItem':
        '''
        Create a DetectionResponseItem from a dictionary

        :param d: a dictionary representing a DetectionResponseItem
        :type d: dict
        :return: a DetectionResponseItem object
        :rtype: DetectionResponseItem
        '''
        return DetectionResponseItem(Box.from_dict(d["box"]),
                                     Landmarks.from_dict(d["landmarks"]),
                                     util.get_pillow_image_from_base64(d["thumbnail"]),
                                     d["detection_score"],
                                     [PersonSearchResult.from_dict(p) for p in d["persons"]])

    def to_dict(self) -> dict:
        '''
        Return a dictionary representation of this object

        :return: a dictionary representing this object
        :rtype: dict
        '''
        return {
            "box": self.box.to_dict(),
            "landmarks": self.landmarks.to_dict(),
            "thumbnail": self.thumbnail,
            "detection_score": self.detection_score,
            "persons": [p.to_dict() for p in self.persons]
        }

    def __repr__(self) -> str:
        return str(self.to_dict())

class VerificationRequest:
    '''A verification request object
    
    :param id: the id of a person being verified
    :type id:str
    :param images: a list of images (max 3), with each image being either a numpy array (obtained with cv2.imread), a string (path to a file), a Pillow image (obtained with PIL.Image.open()), or a pathlib path
    :type images:List[Union[numpy.ndarray, str, PIL.Image.Image, pathlib.Path]]
    :param min_score: a minimum score to match the person, defaults to 0.7
    :type min_score: Optional[float]
    :param search_mode: the model to search FAST or ACCURATE, defaults to ACCURATE
    :type search_mode: Optional[SearchMode]
    '''
    def __init__(self, 
                id: str,
                images: List[Union[np.ndarray, str, Image, Path]],
                min_score: Optional[float] = 0.7,
                search_mode: Optional[SearchMode] = SearchMode.ACCURATE) -> None:
        self.id = id
        self.images = util.normalize_images(images)
        self.min_score = min_score
        self.search_mode = search_mode

    def to_dict(self) -> dict:
        '''
        Return a dictionary representation of this object

        :return: a dictionary representing this object
        :rtype: dict
        '''
        repr = {
            "id": self.id,
            "images": self.images,
            "min_score": self.min_score,
        }

        if isinstance(self.search_mode, SearchMode):
            if self.search_mode == SearchMode.FAST:
                repr["verification_mode"] = "FAST"
            else:
                repr["verification_mode"] = "ACCURATE"
        else:
            repr["verification_mode"] = self.search_mode

        return repr

    def __repr__(self) -> str:
        return str(self.to_dict())

    @property
    def id(self):
        '''id of a person being verified'''
        return self._id

    @id.setter
    def id(self, value):
        if (isinstance(value, str) and len(value) == 0):
            raise ValueError("id must be a non-empty string")
        if not isinstance(value, str):
            raise TypeError("id must be a string")
        self._id = value

    @property
    def min_score(self):
        '''Minimum score to match a person'''
        return self._min_score

    @min_score.setter
    def min_score(self, value):
        if isinstance(value, float) and (value <0 or value > 1.0):
            raise ValueError("min_score must be a float number between 0 and 1")
        elif not isinstance(value, float):
            raise TypeError("min_score must be a float number")
        self._min_score = value

    @property
    def search_mode(self):
        '''The mode to use for a search'''
        return self._search_mode

    @search_mode.setter
    def search_mode(self, value):
        if not isinstance(value, SearchMode):
            raise TypeError("search_mode accepts only SearchMode.FAST or SearchMode.ACCURATE")
        self._search_mode = value

class SearchLiveFaceRequest:
    '''A search live face request object

    :param image: an image with the type being either a numpy array (obtained with cv2.imread), a string (path to a file), a Pillow image (obtained with PIL.Image.open()), or a pathlib path
    :type image:Union[numpy.ndarray, str, PIL.Image.Image, pathlib.Path]
    :param collection_id: the collection id to restrict the search
    :type collection_id: Optional[str]
    :param min_score: a minimum score to match the person, defaults to 0.7
    :type min_score: Optional[float]
    :param max_results: maximum number of search persons, defaults to 10
    :type max_results: Optional[int]
    :param os: OS setting to choose being either DeviceType.DESKTOP, DeviceType.ANDROID, or DeviceType.IOS, defaults to DeviceType.DESKTOP
    :type os: Optional[DeviceType]
    :param search_mode: the model to search FAST or ACCURATE, defaults to FAST
    :type search_mode: Optional[SearchMode]
    '''
    def __init__(self,
                image: Union[np.ndarray, str, Image, Path],
                collection_id: Optional[str] = None,
                min_score: Optional[float] = 0.7,
                max_results: Optional[int] = 10,
                os: Optional[DeviceType] = DeviceType.DESKTOP,
                search_mode: Optional[SearchMode] = SearchMode.ACCURATE) -> None:
        self.image = util.normalize_image(image)
        self.collection_id = collection_id
        self.min_score = min_score
        self.max_results = max_results
        self.os = os
        self.search_mode = search_mode

    def to_dict(self) -> dict:
        '''
        Return a dictionary representation of this object

        :return: a dictionary representing this object
        :rtype: dict
        '''
        repr = {
            "collection_id":self.collection_id,
            "image":self.image,
            "min_score":self.min_score,
            "max_results":self.max_results,
            "os":self.os,
            "search_mode":self.search_mode
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

        if isinstance(self.search_mode,SearchMode):
            if self.search_mode == SearchMode.FAST:
                repr["search_mode"] = "FAST"
            else:
                repr["search_mode"] = "ACCURATE"
        else:
            repr["search_mode"] = self.search_mode
        return repr

    def __repr__(self) -> str:
        return str({
            "collection_id":self.collection_id,
            "image":self.image,
            "max_results":self.max_results,
            "min_score":self.min_score,
            "os":self.os,
            "search_mode":self.search_mode
        })

    @property
    def collection_id(self):
        '''Collection id to search for a person'''
        return self._collection_id

    @collection_id.setter
    def collection_id(self, value):
        if isinstance(value, str) and len(value) == 0:
            raise ValueError("collection_id must be a non-empty string or None")
        elif value is not None and not isinstance(value, str):
            raise TypeError("collection_id must be a non-empty string or None")
        self._collection_id = value

    @property
    def min_score(self):
        return self._min_score

    @min_score.setter
    def min_score(self, value):
        print("value is:",value)
        if isinstance(value, float) and (value <0.7 or value > 1):
            raise ValueError("min_score must be a float number between 0.7 and 1")
        elif not isinstance(value, float):
            raise TypeError("min_score must be a float number")
        self._min_score = value

    @property
    def max_results(self):
        return self._max_results

    @max_results.setter
    def max_results(self,value):
        if isinstance(value,int) and (value < 0 or value > 100):
            raise ValueError("max_results must be a float number between 1 and 100")
        elif not isinstance(value, int):
            raise TypeError("max_results must be an integer number")
        self._max_results = value

    @property
    def search_mode(self):
        '''The model to use for a search'''
        return self._search_mode

    @search_mode.setter
    def search_mode(self, value):
        if not isinstance(value, SearchMode):
            raise TypeError("search_mode accepts only SearchMode.FAST or SearchMode.ACCURATE")
        self._search_mode = value

    @property
    def os(self):
        '''os type of the device'''
        return self._os

    @os.setter
    def os(self,value):
        if not isinstance(value,DeviceType):
            raise TypeError("device type accepts only DeviceType.ANDROID, DeviceType.IOS or DeviceType.DESKTOP")
        self._os = value
        
class SearchLiveFaceResponse:
    '''A search live face response object

    :param persons: a list of persons that closely match the images in the request object
    :type persons: a list of Person objects
    :params liveness_score: a liveness score of the top matched person
    :type liveness_score: float
    '''
    def __init__(self, persons: List[Person] , liveness_score: float) -> None:
        self.persons = persons
        self.liveness_score = liveness_score

    @classmethod
    def from_dict(cls, obj:dict()):
        """Create a SearchLiveFaceResponse from a dictionary

        :param obj: the dictionary representing this object
        :type obj:dict
        
        :return: a SearchLiveFaceResponse object
        :rtype: SearchLiveFaceResponse
        """
        persons = []
        for person in obj["persons"]:
            person_obj = Person.from_dict(person)
            persons.append(person_obj)
        return SearchLiveFaceResponse(persons,obj["liveness_score"])

    def __repr__(self) -> str:
        return str({
            "liveness_score": self.liveness_score,
            "persons":[person.__repr__() for person in self.persons]
        })

class VerificationResponse:
    '''A verification response object

    :param person: the person being verified
    :type person: Person
    :param score: the score of the verification
    :type score: float
    '''
    def __init__(self, person: Person, score: float)->None:
        self.person = person
        self.score = score

    @classmethod
    def from_dict(cls, obj:dict()):
        """Create a VerificationResponse from a dictionary

        :param obj: the dictionary representing this object
        :type obj:dict

        :return: a VerificationResponse object
        :rtype: VerificationResponse
        """
        if obj["match"]:
            return VerificationResponse(Person.from_dict(obj["match"]), obj["match"]["score"])
        else:
            return VerificationResponse(None, 0)


    def __repr__(self) -> str:
        return str({
            "person": self.person.__repr__(),
            "score": self.score
        })