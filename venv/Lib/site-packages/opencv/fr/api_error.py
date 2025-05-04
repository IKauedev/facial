from typing import Union
class APIError(Exception):
    """Class that defines an API Error
    :param http_status_code: the HTTP status code of the error
    :type int
    :param err_code: the API error code
    :type str
    :param messsage: the API error message
    :type str
    :param retry_after: if present, specifies the time in seconds when the request can be retried to meet rate limit checks
    :type Union[int, None]
    """
    def __init__(self, http_status_code:int, err_code:str, messsage: str, retry_after:Union[int, None]=None) -> None:
        self.http_status_code = http_status_code
        self.err_code = err_code
        self.messsage = messsage
        self.retry_after = retry_after

class APIDataValidationError(Exception):
    """Class that defines an API Data Validation Error
    :param details: Error details from API Server
    :type dict
    """
    def __init__(self, details) -> None:
        self.details = details