from ..http_interactor import HttpInteractor
from ..persons.schemas import Person, PersonList, PersonOrderBy, Action, UpdatePersonsRequest, UpdatePersonsResponse
from .. import util as util
from ..schemas import SortOrder
from typing import Optional

class PersonsManager:
    '''Class to manage persons
    
    :param http_interactor: the http interactor instance
    :type http_interactor:HttpInteractor
    '''
    
    def __init__(self, http_interactor:HttpInteractor) -> None:
        self.__http_interactor = http_interactor

    def list(self, skip:Optional[int]=0, 
             take:Optional[int]=20, 
             order_by:Optional[PersonOrderBy]=PersonOrderBy.NAME, 
             order:Optional[SortOrder]=SortOrder.ASC, 
             search:Optional[str]=None) -> PersonList:
        """Get a persons list 

        :param skip: skip the specified number of initial rows, defaults to 0
        :type skip:Optional[int]
        :param take: get the specified number of rows, defaults to 20
        :type take:Optional[int]
        :param order: order ascending(SortOrder.ASC) or descending(SortOrder.DESC)
        :type order:Optional[SortOrder]
        :param order_by: the column to choose for the ordering
        :type order_by:Optional[PersonOrderBy]
        :param search: a search string to filter collections by name/description
        :type search:Optional[str]

        :raises ApiError: an API error if unsuccessful

        :return: a CollectionList object
        :rtype: CollectionList
        """
        s_order_by = str(order_by).lower().replace("personorderby.", "")
        order = "ASC" if order == SortOrder.ASC else "DESC"
        params = {"skip": skip, "take": take, "order": order, "search": search, "order_by": s_order_by}
        result = self.__http_interactor.get("persons", params)
        return PersonList.from_dict(result)

    def create(self, person:Person) -> Person:
        """Create a person

        :param person: a person object minimally specifying a name and images
        :type person:Person

        :raises ApiError: an API error if unsuccessful

        :return: a Person object representing the person that was created
        :rtype: Person
        """
        post_body = person.to_dict()
        b64_images = []
        for image in post_body["images"]:
            i_bytes = util.get_jpeg_bytes_from_pillow_img(image)
            i_str = util.get_base64_from_bytes(i_bytes)
            b64_images.append(i_str)
        post_body["images"] = b64_images

        result = self.__http_interactor.post("person", post_body)
        return Person.from_dict(result)

    def update(self, person:Person) -> Person:
        """Updates a person

        :param person: a person object
        :type person:Person

        :raises ApiError: an API error if unsuccessful

        :return: a Person object representing the person that was updated
        :rtype: Person
        """
        obj = person.to_dict()
        if len(obj.keys()) == 1:
            raise ValueError("Object is not modified. Nothing to update")
        b64_images = []
        if "images" in obj:
            for image in obj["images"]:
                i_bytes = util.get_jpeg_bytes_from_pillow_img(image)
                i_str = util.get_base64_from_bytes(i_bytes)
                b64_images.append(i_str)
            obj["images"] = b64_images
        result = self.__http_interactor.patch("person", obj)
        result = Person.from_dict(result)
        return result

    def delete(self, id:str) -> None:
        """Deletes the specified person

        :param id: the id of the person to be deleted
        :type id:str

        :raises ApiError: an API error if unsuccessful
        """
        self.__http_interactor.delete("person", id)

    def get(self, id:str) -> Person:
        """Gets person specified by the id

        :param id: the id of the person to be retrieved
        :type id:str

        :raises ApiError: an API error if unsuccessful

        :return: a Person object
        :rtype: Person
        """
        result = self.__http_interactor.get(f"person/{id}")
        return Person.from_dict(result)
    
    def update_persons(self, request:UpdatePersonsRequest) -> dict:
        """Patchs persons specified in person_ids of PatchPersonsRequest

        :param request: a UpdatePersonsRequest object
        :type request: UpdatePersonsRequest

        :return: List of person ids
        :rtype: List(str)
        
        """
        obj = request.to_dict()
        result = self.__http_interactor.patch("persons",obj)
        result = UpdatePersonsResponse.from_dict(result)
        return result

    
