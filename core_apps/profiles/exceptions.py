"""this module implements a custom exception class"""

from rest_framework.exceptions import APIException


class NotYourProfile(APIException):
    status_code: int = 403
    default_detail: str = "You can't edit a profile that doesn't belong to you!"


class CantFollowYourself(APIException):
    status_code: int = 403
    default_detail: str = "You can't follow yourself"
