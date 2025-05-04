from ..http_interactor import HttpInteractor
from ..search.schemas import SearchRequest, DetectionRequest, DetectionResponseItem, VerificationRequest, VerificationResponse, PersonSearchResult, SearchLiveFaceRequest, SearchLiveFaceResponse
from .. import util as util
from ..persons.schemas import Person
from typing import List


class SearchManager:
    """A class to manage search

    :param http_interactor: the http interactor instance
    :type http_interactor:API7.HttpInteractor
    """
    
    def __init__(self, http_interactor:HttpInteractor) -> None:
        self.__http_interactor = http_interactor

    def search(self, search:SearchRequest) -> List[Person]:
        """Search for a person

        :param search: a SearchRequest object minimally specifying images
        :type search:SearchRequest

        :raises ApiError: an API error if unsuccessful

        :return: a list of persons matching the search criteria
        :rtype: List[Person]
        """
        post_body = search.to_dict()

        b64_images = []
        for image in post_body["images"]:
            i_bytes = util.get_jpeg_bytes_from_pillow_img(image)
            i_str = util.get_base64_from_bytes(i_bytes)
            b64_images.append(i_str)
        post_body["images"] = b64_images

        result = self.__http_interactor.post("search", post_body, expected_status=200)
        return [PersonSearchResult.from_dict(person) for person in result]

    def search_crops(self, search:SearchRequest) -> List[Person]:
        """Search for a person from crops of images obtained using face detection

        :param search: a SearchRequest object minimally specifying crop images
        :type search:SearchRequest

        :raises ApiError: an API error if unsuccessful

        :return: a list of persons matching the search criteria
        :rtype: List[Person]
        """
        post_body = search.to_dict()

        b64_images = []
        for image in post_body["images"]:
            i_bytes = util.get_jpeg_bytes_from_pillow_img(image)
            i_str = util.get_base64_from_bytes(i_bytes)
            b64_images.append(i_str)
        post_body["images"] = b64_images
        
        result = self.__http_interactor.post("search/crops", post_body, expected_status=200)
        return [PersonSearchResult.from_dict(person) for person in result]

    def detect(self, detection_request:DetectionRequest) -> List[DetectionResponseItem]:
        """Detect, and optionally search for all detected persons

        :param detection_request: a DetectionRequest object minimally specifying images, and optionally search options
        :type detection_request:DetectionRequest

        :raises ApiError: an API error if unsuccessful

        :return: a list of DetectionResponseItem objects representing the detected faces (and optionally matched persons)
        :rtype: List[DetectionResponseItem]
        """
        post_body = detection_request.to_dict()

        image = post_body["image"]
        i_bytes = util.get_jpeg_bytes_from_pillow_img(image)
        i_str = util.get_base64_from_bytes(i_bytes)
        post_body["image"] = i_str

        result = self.__http_interactor.post("detect", post_body, expected_status=200)
        return [DetectionResponseItem.from_dict(item) for item in result]

    def verify(self, verification_request:VerificationRequest) -> VerificationResponse:
        """Verify a person

        :param verification_request: a VerificationRequest object specifying the person id to be verified, and the images to be used for verification
        :type verification_request:VerificationRequest

        :raises ApiError: an API error if unsuccessful

        :return: a VerificationResponse object with a matched person and score. If no match was found, the matched person is None.
        :rtype: VerificationResponse
        """
        post_body = verification_request.to_dict()

        b64_images = []
        for image in post_body["images"]:
            i_bytes = util.get_jpeg_bytes_from_pillow_img(image)
            i_str = util.get_base64_from_bytes(i_bytes)
            b64_images.append(i_str)
        post_body["images"] = b64_images
        
        result = self.__http_interactor.post("verify", post_body, expected_status=200)
        return VerificationResponse.from_dict(result)
    
    def search_live_face(self, search_live_face_request:SearchLiveFaceRequest):
        """Search for a matching face and check liveness

        :param search_live_face_request: a SearchLiveFaceRequest object specifying the image of the person and other optional attributes such as collection_id
        :type search_live_face_request: SearchLiveFaceRequest

        :raises ApiError: an API error if unsuccessful

        :return: a SearchLiveFaceResponse object with matched person(s) and liveness_score. If no match was found, entity not found exception is raised.
        :rtype: SearchLiveFaceResponse
        """
        post_body = search_live_face_request.to_dict()
        i_bytes = util.get_jpeg_bytes_from_pillow_img(search_live_face_request.image)
        i_str = util.get_base64_from_bytes(i_bytes)
        post_body["image"] = i_str

        result = self.__http_interactor.post("search-live-face", post_body, expected_status=200)
        return SearchLiveFaceResponse.from_dict(result)