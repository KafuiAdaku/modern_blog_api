from rest_framework.exceptions import APIException


class NotYourProfile(APIException):
    """
    Exception raised when a user tries to edit a profile
        that doesn't belong to them.

    Attributes:
    - status_code (int): HTTP status code for the
        exception (403 Forbidden).
    - default_detail (str): Default error message for the exception.
    """

    status_code: int = 403
    default_detail: str = "You can't edit a profile that doesn't belong to you!"


class CantFollowYourself(APIException):
    """
    Exception raised when a user tries to follow themselves.

    Attributes:
    - status_code (int): HTTP status code for the exception (403 Forbidden).
    - default_detail (str): Default error message for the exception.
    """

    status_code: int = 403
    default_detail: str = "You can't follow yourself"
