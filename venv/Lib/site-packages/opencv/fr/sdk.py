from .collections.collections_manager import CollectionsManager
from .persons.persons_manager import PersonsManager
from .search.search_manager import SearchManager
from .liveness.liveness_manager import LivenessManager
from .compare.compare_manager import CompareManager
from .http_interactor import HttpInteractor

class SDK:
    """Class to interact with the API7 REST API
    :param backend_url: the URL where the REST API is deployed
    :type str
    :param developer_key: the developer key to use while interacting with the API
    :type str
    """
    def __init__(self, backend_url:str, developer_key: str) -> None:
        interactor = HttpInteractor(backend_url, developer_key)
        self.collections = CollectionsManager(interactor)
        self.persons = PersonsManager(interactor)
        self.search = SearchManager(interactor)
        self.liveness = LivenessManager(interactor)
        self.compare = CompareManager(interactor)
    


    