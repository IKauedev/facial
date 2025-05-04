from ..http_interactor import HttpInteractor
from ..liveness.schemas import LivenessRequest, LivenessResponse
from .. import util as util 

class LivenessManager:
    """Class to help manage liveness requests
    
    :param http_interactor: the http interactor instance
    :type http_interactor:HttpInteractor
    """
    def __init__(self, http_interactor:HttpInteractor) -> None:
        self.__http_interactor = http_interactor

    def check_liveness(self, liveness_request:LivenessRequest) -> LivenessResponse:
        """Check the liveness of the provided image

        :param liveness_request: a LivenessRequest object minimally specifying image, and optionally os type
        :type liveness_request:LivenessRequest

        :raises ApiError: an API error if unsuccessful

        :return: a LivenessResponse object containing the result of the liveness check
        :rtype: LivenessResponse
        """
        post_body = liveness_request.to_dict()

        image = post_body["image"]
        i_bytes = util.get_jpeg_bytes_from_pillow_img(image)
        i_str = util.get_base64_from_bytes(i_bytes)
        post_body["image"] = i_str

        result = self.__http_interactor.post("liveness", post_body, expected_status=200)
        return LivenessResponse.from_dict(result)
