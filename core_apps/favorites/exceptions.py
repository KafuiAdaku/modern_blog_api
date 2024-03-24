from rest_framework.exceptions import APIException


class AlreadyFavorited(APIException):
    """
    Custom exception for already favorited blogs.

    This exception is raised when a user attempts to favorite
    a blog that has already been favorited.

    Attributes:
    - status_code (int): The HTTP status code for the
        exception (400 Bad Request).
    - default_detail (str): The default error message.
    """

    status_code = 400
    default_detail = "You have already favorited this blog"
