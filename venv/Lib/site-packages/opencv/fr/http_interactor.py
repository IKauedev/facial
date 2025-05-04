import requests
from .api_error import APIError, APIDataValidationError
from typing import List, Union

class HttpInteractor:
    """Class to help with HTTP interactions
    :param backend_url: the URL where the REST API is deployed
    :type str
    :param developer_key: the developer key to use while interacting with the API
    :type str
    """
    def __init__(self, backend_url:str, developer_key:str) -> None:
        self.__backend_url = backend_url
        self.__developer_key = developer_key

    def get(self, url_fragment: str, params:dict=None) -> Union[dict, List[dict]]:
        """Performs an HTTP GET request

        :param url_fragment: the URL fragment from the base URL
        :type url_fragment: str
        :param params: if specified, the parameters to pass to the call, defaults to None
        :type params: Optional[dict]

        :raises APIError: an API7 error with http status code, error code, and error message

        :return: a dictionary or a list of dictionaries
        :rtype: Union[dict, List[dict]]
        """
        url = f"{self.__backend_url}/{url_fragment}"
        headers = {"x-api-key": self.__developer_key}
        response = None
        if params:
            response = requests.get(url, params=params, headers=headers)
        else:
            response = requests.get(url, headers=headers)

        if response.status_code == 422:
            body = response.json()
            error = APIDataValidationError(body)
            raise error
        elif response.status_code != 200:
            body = response.json()
            error = APIError(response.status_code, body["code"], body["message"])
            if "retry-after" in response.headers:
                error.retry_after = int(response.headers["retry-after"])
            raise error

        return response.json()

    def post(self, url_fragment: str, obj:dict, expected_status=201) -> dict:
        """Performs an HTTP POST request

        :param url_fragment: the URL fragment from the base URL
        :type url_fragment: str
        :param obj: the object to be posted represented as a dictionary
        :type obj: dict
        :param expected_status: the expected status code, defaults to 201
        :type expected_status: int

        :raises APIError: an API7 error with http status code, error code, and error message

        :return: a dictionary
        :rtype: dict
        """
        url = f"{self.__backend_url}/{url_fragment}"
        headers = {"x-api-key": self.__developer_key}
        response = requests.post(url, json=obj, headers=headers)

        if response.status_code == 422:
            body = response.json()
            error = APIDataValidationError(body)
            raise error
        elif response.status_code != expected_status:
            body = response.json()
            error = APIError(response.status_code, body["code"], body["message"])
            if "retry-after" in response.headers:
                error.retry_after = int(response.headers["retry-after"])
            raise error

        return response.json()

    def patch(self, url_fragment: str, obj:dict) -> dict:
        """Performs an HTTP PATCH request

        :param url_fragment: the URL fragment from the base URL
        :type url_fragment: str
        :param obj: the object to be posted represented as a dictionary
        :type obj: dict

        :raises APIError: an API7 error with http status code, error code, and error message

        :return: a dictionary
        :rtype: dict
        """
        url = f"{self.__backend_url}/{url_fragment}"
        headers = {"x-api-key": self.__developer_key}
        response = requests.patch(url, json=obj, headers=headers)

        if response.status_code == 422:
            body = response.json()
            error = APIDataValidationError(body)
            raise error
        elif response.status_code != 200:
            body = response.json()
            error = APIError(response.status_code, body["code"], body["message"])
            if "retry-after" in response.headers:
                error.retry_after = int(response.headers["retry-after"])
            raise error

        return response.json()

    def delete(self, url_fragment: str, id:str) -> None:
        """Performs an HTTP DELETE request

        :param url_fragment: the URL fragment from the base URL
        :type url_fragment: str
        :param id: the id of the object to be deleted
        :type id: str

        :raises APIError: an API7 error with http status code, error code, and error message
        """
        url = f"{self.__backend_url}/{url_fragment}/{id}"
        headers = {"x-api-key": self.__developer_key}
        response = requests.delete(url, headers=headers)

        if response.status_code == 422:
            body = response.json()
            error = APIDataValidationError(body)
            raise error
        elif response.status_code != 200:
            body = response.json()
            error = APIError(response.status_code, body["code"], body["message"])
            if "retry-after" in response.headers:
                error.retry_after = int(response.headers["retry-after"])
            raise error


