from rest_framework.exceptions import APIException


class AlreadyFavorited(APIException):
    """Custom exception for already favorited blog"""
    status_code = 400
    default_detail = "You have already favorited this blog"
