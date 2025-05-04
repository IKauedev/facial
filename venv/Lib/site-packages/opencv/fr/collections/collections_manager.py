from ..http_interactor import HttpInteractor
from ..schemas import SortOrder
from ..collections.schemas import CollectionBase, CollectionList, Collection, UpdateCollectionRequest, UpdateCollectionResponse
from typing import Optional


class CollectionsManager:
    """Class to help manage collections
    
    :param http_interactor: the http interactor instance
    :type http_interactor:HttpInteractor
    """
    def __init__(self, http_interactor:HttpInteractor) -> None:
        self.__http_interactor = http_interactor

    def list(self, skip:Optional[int]=0, 
             take:Optional[int]=20, 
             order:Optional[SortOrder]=SortOrder.ASC, 
             search:Optional[str]=None) -> CollectionList:
        """Get a collections list 

        :param skip: skip the specified number of initial rows, defaults to 0
        :type skip:Optional[int]
        :param take: get the specified number of rows, defaults to 20
        :type take:Optional[int]
        :param order: order ascending(SortOrder.ASC) or descending(SortOrder.DESC)
        :type order:Optional[SortOrder]
        :param search: a search string to filter collections by name/description
        :type search:Optional[str]

        :raises API7.ApiError: an API error if unsuccessful

        :return: a CollectionList object
        :rtype: CollectionList
        """
        if not isinstance(order, SortOrder):
            raise TypeError("order should be of type SortOrder Enum")

        order = "ASC" if order == SortOrder.ASC else "DESC"
        params = {"skip": skip, "take": take, "order": order, "search": search}
        result = self.__http_interactor.get("collections", params)
        return CollectionList.from_dict(result)

    def create(self, collection:CollectionBase) -> Collection:
        """Create a collection

        :param collection: a collection base object specifying the name and description of the collection to be created
        :type collection:CollectionBase

        :raises API7.ApiError: an API error if unsuccessful

        :return: a Collection object representing the collection that was created
        :rtype: Collection
        """
        obj = collection.to_dict()
        if "count" in obj:
            del obj["count"]
        result = self.__http_interactor.post("collection", obj)
        result = Collection.from_dict(result)
        return result

    def update(self, collection:Collection) -> Collection:
        """Updates a collection

        :param collection: a collection object specifying the id, name and description of the collection to be updated
        :type collection:Collection

        :raises ApiError: an API error if unsuccessful

        :return: a Collection object representing the collection that was updated
        :rtype: Collection
        """
        obj = collection.to_dict()
        if "count" in obj:
            del obj["count"]
        result = self.__http_interactor.patch("collection", obj)
        result = Collection.from_dict(result)
        return result

    def delete(self, id:str) -> None:
        """Deletes the specified collection

        :param id: the id of the collection to be deleted
        :type id:str

        :raises ApiError: an API error if unsuccessful
        """
        self.__http_interactor.delete("collection", id)

    def get(self, id:str) -> Collection:
        """Gets collection specified by the id

        :param id: the id of the collection to be retrieved
        :type id:str

        :raises ApiError: an API error if unsuccessful

        :return: a Collection object
        :rtype: Collection
        """
        result = self.__http_interactor.get(f"collection/{id}")
        return Collection.from_dict(result)
    
    def update_collection_persons(self,request: UpdateCollectionRequest):
        """Patches collection with new persons and remove the existing person

        :param request: a UpdateCollectionRequest
        :type request: UpdateCollectionRequest

        :return: a UpdateCollectionResponse
        :rtype: UpdateCollectionResponse        
        """
        obj = request.to_dict()
        result = self.__http_interactor.patch(f"collection/persons",obj)
        return(UpdateCollectionResponse(result))
