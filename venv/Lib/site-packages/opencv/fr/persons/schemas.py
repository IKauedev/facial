import copy
from typing import List, Union, Optional
import numpy as np
import cv2
from PIL.Image import Image
from pathlib import Path
import enum
from datetime import datetime
from ..collections.schemas import Collection, CollectionBase
from .. import util as util 
from dateutil.parser import parse

'''
Gender of the person
'''
class PersonGender(enum.Enum):
    M = "M"
    F = "F"

'''
Gender of the person
'''
class PersonOrderBy(enum.Enum):
    NAME = "name"
    DATE_OF_BIRTH = "date_of_birth"
    GENDER = "gender"
    NATIONALITY = "nationality"
    MODIFIED_DATE = "modified_date"
    CREATE_DATE = "create_date"

'''
Action for a bulk operation
'''
class Action(enum.Enum):
    DELETE = "DELETE"

class UpdatePersonsRequest:
    '''A update person request object

    :param action: type of bulk operation
    :type action: Action
    :param person_ids: list of ID for persons 
    :type person_ids: List of person IDs    
    '''
    def __init__(self,
            action: Action = Action.DELETE,
            person_ids: list = []
                ) -> None:
        if not isinstance (action, Action):
            raise TypeError("Action must be defined")
        if not isinstance (person_ids, list):
            raise TypeError("person ids must be list")
        if len(person_ids)<1:
            raise ValueError("list of person ids cannot be empty")
        for id in person_ids:
            if not isinstance(id,str):
                raise TypeError("person ids must be string")

        self._action = action
        self._person_ids = person_ids
    
    def to_dict(self) -> dict:
        repr = {
           "action": str(self.action.name),
           "person_ids":self.person_ids
        }
        return repr

    def __repr__(self) -> str:
        return str({
            "action":self.action.name,
            "person_ids":self.person_ids
        })

    @property
    def action(self):
        return self._action

    @property
    def person_ids(self):
        return self._person_ids

    @action.setter
    def action(self, value):
        if not isinstance(value,Action):
            raise TypeError("action must be type Action")
        self._action = value
        
    @person_ids.setter
    def person_ids(self, value):
        if not isinstance(value,list ):
            raise TypeError("person ids must be list")
        if len(value)<1:
            raise ValueError("list of person ids cannot be empty")
        for id in value:
            if not isinstance(id,str):
                raise TypeError("person ids must be string")
        self._person_ids=value

class UpdatePersonsResponse:
    '''A update person response object

    :param person_ids: List of person IDs with successful operation
    :type person_ids: List(str)    
    '''
    def __init__(self, person_ids: dict()) -> None:
        self.person_ids = person_ids

    @classmethod
    def from_dict(cls, obj:dict):
        """Create a UpdatePersonsResponse from a dictionary

        :param obj: the list
        :type obj: List

        :return: a UpdatePersonsResponse object
        :rtype: UpdatePersonResponse
        """
        items = [item["id"] for item in obj]
        return UpdatePersonsResponse(items)
    
    def __repr__(self) -> str:
        return str({
            "person_ids":[item for item in self.person_ids]
        })

class PersonBase:
    '''A person object

    :param images: a list of images (max 3), with each image being either a numpy array (obtained with cv2.imread), a string (path to a file), a Pillow image (obtained with PIL.Image.open()), or a pathlib path
    :type images:List[Union[np.ndarray, str, Image, Path]]
    :param id: a unique identifier for the person. If unspecified a new id will be generated, defaults to None
    :type id: Optional[str]
    :param name: the name of the person
    :type name:Optional[str]
    :param gender: the gender of the person, defaults to None
    :type gender: Optional[PersonGender]
    :param date_of_birth: the date of birth of the person, defaults to None
    :type date_of_birth: Optional[datetime]
    :param nationality: the nationality of the person, defaults to None
    :type nationality: Optional[str]
    :param collections: a list containing either Collection, CollectionBase objects, or strings representing the id of the collections that this person belongs to, defaults to empty list []
    :type collections: Optional[List[Union[Collection, CollectionBase, str]]]
    :param notes: any additional notes about the person, defaults to None
    :type notes: Optional[str]
    :param is_bulk_insert: whether this person is part of a bulk insert batch, defaults to False
    :type is_bulk_insert: Optional[bool]
    '''
    def __init__(self, 
                 images: List[Union[np.ndarray, str, Image, Path]],
                 id:Optional[str] = None,
                 name: Optional[str] = None, 
                 gender:Optional[PersonGender] = None,
                 date_of_birth:Optional[datetime] = None,
                 nationality:Optional[str] = None,
                 collections:Optional[List[Union[Collection, CollectionBase, str]]]=[],
                 notes:Optional[str]=None,
                 is_bulk_insert:Optional[bool] = False) -> None:
        if not isinstance(images, list):
            raise TypeError("images must be a list")
        if len(images) > 3:
            raise ValueError("images list cannot contain more than 3 images")
        if len(images) < 1:
            raise ValueError("images list cannot be empty")
        self.name = name
        self._images = util.normalize_images(images)
        self.id = id
        self.gender = gender
        self.date_of_birth = date_of_birth
        self.nationality = nationality
        self.collections = collections
        self.notes = notes
        self.is_bulk_insert = is_bulk_insert
        self.__server_object:Person = None

    @property
    def images(self):
        raise RuntimeError('This property has no getter. Please use get_image(index:int) -> Image')

    @images.setter
    def images(self, images:List[Union[np.ndarray, str, Image, Path]]):
        """Replaces the current set of images with the ones specified

        :param images: the list of images to be set for this person, each image must be at least 224x224 pixels
        :type images:List[Union[np.ndarray, str, Image, Path]]
        """
        if not isinstance(images, list):
            raise TypeError("images must be a list")
        if len(images) > 3:
            raise ValueError("images list cannot contain more than 3 images")
        if len(images) < 1:
            raise ValueError("images list cannot be empty")
        images:List[Image] = util.normalize_images(images)
        for image in images:
            if image.height < 224 or image.width < 224:
                raise ValueError("At least one image is smaller than 224x224")
        self._images = images

    def get_image(self, image_index: int) -> Image:
        """Get's the image at the specified index

        :param image_index: the index of the image to get
        :type image_index:int
        """
        return self._images[image_index]

    @property
    def name(self):
        '''Name of the person'''
        return self._name

    @name.setter
    def name(self, value):
        if isinstance(value, str) and len(value) == 0:
            raise ValueError("If specified, name must be a non-empty string")
        elif value is not None and not isinstance(value, str):
            raise TypeError("If specified, name must be a string")
        self._name = value

    @property
    def id(self):
        '''Id of the person'''
        return self._id

    @id.setter
    def id(self, value):
        if isinstance(value, str) and len(value) == 0:
            raise ValueError("id must be a non-empty string or None")
        if not isinstance(value, str) and not value is None:
            raise TypeError("id must be a string or None")
        self._id = value

    @property
    def gender(self):
        '''Gender of the person'''
        return self._gender

    @gender.setter
    def gender(self, value):
        if value is not None and not isinstance(value, PersonGender):
            raise TypeError("gender must be of type PersonGender or None")
        self._gender = value

    @property
    def date_of_birth(self):
        '''Date of birth of the person'''
        return self._date_of_birth

    @date_of_birth.setter
    def date_of_birth(self, value):
        if value is not None and not isinstance(value, datetime):
            raise TypeError("date_of_birth must be of type datetime or None")
        self._date_of_birth = value

    @property
    def nationality(self):
        '''Nationality of the person'''
        return self._nationality

    @nationality.setter
    def nationality(self, value):
        if not isinstance(value, str) and not value is None:
            raise TypeError("nationality must be of type str or None")
        self._nationality = value

    @property
    def collections(self):
        '''Collections that the person belongs to'''
        return self._collections

    @collections.setter
    def collections(self, value):
        if not isinstance(value, list):
            raise TypeError("collections must be of type list")
        for collection in value:
            if not isinstance(collection, Collection) and not isinstance(collection, CollectionBase):
                raise TypeError("At least one item in collections is neither of type Collection nor CollectionBase")
        self._collections = value

    @property
    def notes(self):
        '''Any notes related to the person'''
        return self._notes

    @notes.setter
    def notes(self, value):
        if not isinstance(value, str) and not value is None:
            raise TypeError("notes must be of type str or None")
        self._notes = value

    @property
    def is_bulk_insert(self):
        '''Whether this person is part of a bulk insert operation'''
        return self._is_bulk_insert

    @is_bulk_insert.setter
    def is_bulk_insert(self, value):
        if not isinstance(value, bool):
            raise TypeError("is_bulk_insert must be of type bool")
        self._is_bulk_insert = value

    def set_server_obj(self, obj):
        self.__server_object = obj

    def to_dict(self) -> dict:
        '''
        Return a dictionary representation of this object

        :return: a dictionary representing this object
        :rtype: dict
        '''
        repr = {}

        if not self.__server_object:
            # If there is no server object, images are always included
            images = util.normalize_images(self._images)
            repr["images"] = images
        else:
            # Otherwise, include only if they are changed
            if self.name != self.__server_object.name:
                repr["name"] = self.name

            if self._images != self.__server_object._images:
                images = util.normalize_images(self._images)
                repr["images"] = images

        # Id should always be included
        repr["id"] = self.id

        if not self.__server_object:
            if self.gender == PersonGender.M:
                repr["gender"] = "M"
            elif self.gender == PersonGender.F:
                repr["gender"] = "F"
            else:
                repr["gender"] = None
        else:
            if self.__server_object.gender != self.gender:
                if self.gender == PersonGender.M:
                    repr["gender"] = "M"
                elif self.gender == PersonGender.F:
                    repr["gender"] = "F"
                else:
                    repr["gender"] = None
        

        if not self.__server_object:
            if self.date_of_birth is not None:
                repr["date_of_birth"] = str(self.date_of_birth).split(' ')[0]
            else:
                repr["date_of_birth"] = None
        else:
            if self.__server_object.date_of_birth != self.date_of_birth:
                if self.date_of_birth is not None:
                    repr["date_of_birth"] = str(self.date_of_birth).split(' ')[0]
                else:
                    repr["date_of_birth"] = None

        if not self.__server_object:
            repr["nationality"] = self.nationality
        else:
            if self.__server_object.nationality != self.nationality:
                repr["nationality"] = self.nationality

        if not self.__server_object:
            repr["name"] = self.name
        else:
            if self.__server_object.name != self.name:
                repr["name"] = self.name

        if not self.__server_object:
            collections = []
            for collection in self.collections:
                if isinstance(collection, CollectionBase):
                    collections.append(collection.id)
                elif isinstance(collection, Collection):
                    collections.append(collection.id)
                elif isinstance(collection, str):
                    collections.append(collection)
                else:
                    raise TypeError("At least one collection is of inappropriate type")
            
            repr["collections"] = collections
        else:
            if self.__server_object.collections != self.collections:
                collections = []
                for collection in self.collections:
                    if isinstance(collection, CollectionBase):
                        collections.append(collection.id)
                    elif isinstance(collection, Collection):
                        collections.append(collection.id)
                    elif isinstance(collection, str):
                        collections.append(collection)
                    else:
                        raise TypeError("At least one collection is of inappropriate type")
                repr["collections"] = collections


        if not self.__server_object:
            repr["notes"] = self.notes
        else:
            if self.__server_object.notes != self.notes:
                repr["notes"] = self.notes

        if not self.__server_object:
            repr["is_bulk_insert"] = self.is_bulk_insert
        else:
            if self.is_bulk_insert != self.is_bulk_insert:
                repr["is_bulk_insert"] = self.is_bulk_insert

        return repr

    # def __getattribute__(self, name):
    #     val = object.__getattribute__(self, name)
    #     return val

    def __repr__(self) -> str:
        return str({
            "id": self.id,
            "name": self.name,
            "images": self._images,
            "gender": self.gender,
            "collections": self.collections,
            "date_of_birth": self.date_of_birth,
            "nationality": self.nationality,
            "notes": self.notes
        })

class Person(PersonBase):
    '''A previously created person object

    :param images: a list of images (max 3), with each image being either a numpy array (obtained with cv2.imread), a string (path to a file), a Pillow image (obtained with PIL.Image.open()), or a pathlib path
    :type images:List[Union[numpy.ndarray, str, PIL.Image.Image, pathlib.Path]]
    :param id: a unique identifier for the person. If unspecified a new id will be generated, defaults to None
    :type id: Optional[str]
    :param name: the name of the person
    :type name:Optional[str]
    :param gender: the gender of the person, defaults to None
    :type gender: Optional[PersonGender]
    :param date_of_birth: the date of birth of the person, defaults to None
    :type date_of_birth: Optional[datetime]
    :param nationality: the nationality of the person, defaults to None
    :type nationality: Optional[str]
    :param collections: a list containing either Collection, CollectionBase objects, or strings representing the id of the collections that this person belongs to, defaults to empty list []
    :type collections: Optional[List[Union[Collection, CollectionBase, str]]]
    :param notes: any additional notes about the person, defaults to None
    :type notes: Optional[str]
    :param is_bulk_insert: whether this person is part of a bulk insert batch, defaults to False
    :type is_bulk_insert: Optional[bool]
    :param create_date: date that this person was created
    :type create_date: datetime
    :param modified_date: date that this person was modified
    :type modified_date: datetime
    '''
    def __init__(self, 
                 images: List[Union[np.ndarray, str, Image, Path]],
                 id:Optional[str] = None,
                 name: Optional[str] = None, 
                 gender:Optional[PersonGender] = None,
                 date_of_birth:Optional[datetime] = None,
                 nationality:Optional[str] = None,
                 collections:Optional[List[Union[Collection, CollectionBase, str]]]=[],
                 notes:Optional[str]=None,
                 is_bulk_insert:Optional[bool] = False,
                 create_date:datetime = None,
                 modified_date:datetime = None) -> None:
        super().__init__(images, id=id, name=name, gender=gender,
                        date_of_birth=date_of_birth, nationality=nationality,
                        collections=collections, notes=notes,
                        is_bulk_insert=is_bulk_insert)

        if not isinstance(create_date, datetime):
            raise TypeError("create_date must be of type datetime")

        if not isinstance(modified_date, datetime):
            raise TypeError("modified_date must be of type datetime")

        self._create_date = create_date
        self._modified_date = modified_date

    @property
    def create_date(self):
        '''Date that the person was created'''
        return self._create_date

    @property
    def modified_date(self):
        '''Date that the person was modified'''
        return self._modified_date

    @classmethod
    def from_dict(cls, obj:dict):
        """Get a person initialized from a dict

        :param obj: the dictionary representing this object
        :type obj:dict

        :return: a Person object
        :rtype: Person
        """
        collections = [Collection.from_dict(item) for item in obj["collections"]]
        thumbnails = [util.get_pillow_image_from_base64(item["thumbnail"]) for item in obj["thumbnails"]]
        gender = obj["gender"]
        if gender == "M":
            gender = PersonGender.M
        elif gender == "F":
            gender = PersonGender.F
        else:
            gender = None
        server_obj = Person( 
            thumbnails,
            id=obj["id"],
            name=obj["name"],
            gender=gender,
            date_of_birth= parse(obj["date_of_birth"]) if obj["date_of_birth"] else None,
            nationality=obj["nationality"],
            collections=collections,
            notes=obj["notes"],
            is_bulk_insert=False,
            create_date=parse(obj["create_date"]),
            modified_date=parse(obj["modified_date"]))

        client_obj = copy.copy(server_obj)
        client_obj._images = thumbnails
        client_obj.set_server_obj(server_obj)
        return client_obj

    def __repr__(self) -> str:
        return str({
            "id": self.id,
            "name": self.name,
            "images": self._images,
            "gender": self.gender,
            "collections": self.collections,
            "date_of_birth": self.date_of_birth,
            "nationality": self.nationality,
            "notes": self.notes,
            "create_date": str(self.create_date),
            "modified_date": str(self.modified_date)
        })

class PersonList:
    '''A list of persons
    
    :param count: the total count of all persons in the database
    :type count:int
    :param persons: the persons matching the criteria
    :type persons:List[Person]
    '''
    
    def __init__(self, count: int, persons: List[Person]) -> None:
        if not isinstance(count, int):
            raise TypeError("count must be of type int")
        if not isinstance(persons, list):
            raise TypeError("persons must be of type list")
        for person in persons:
            if not isinstance(person, Person):
                raise TypeError("At least one item in persons is not an object of type Person")
        self._count: int = count
        self._persons: List[Person] = persons

    @property
    def count(self):
        '''Total number of persons in the database that match the criteria'''
        return self._count

    @property
    def persons(self):
        '''The (paged) list of persons that match the criteria'''
        return self._persons

    @classmethod
    def from_dict(cls, obj:dict):
        """Get a person list initialized from a dict

        :param obj: the dictionary representing this object
        :type obj:dict

        :return: a PersonList object
        :rtype: PersonList
        """
        persons = [Person.from_dict(item) for item in obj["persons"]]
        return PersonList(obj["count"], persons)

    def to_dict(self) -> dict:
        '''
        Return a dictionary representation of this object

        :return: a dictionary representing this object
        :rtype: dict
        '''
        return {
            "count": self.count,
            "persons": [item.to_dict() for item in self.persons],
        }

    def __repr__(self) -> str:
        return str({"count": self.count, "persons": [str(item) for item in self.persons]})

        

    

    
