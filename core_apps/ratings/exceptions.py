from rest_framework.exceptions import APIException


class CantRateYourBlog(APIException):
    """
    Custom exception for trying to rate own blog.

    This exception is raised when a user tries to
        rate their own blog post.

    Attributes:
    - status_code (int): The HTTP status code for the
        exception (403 Forbidden).
    - default_detail (str): The default error message.
    """

    status_code: int = 403
    default_detail: str = "You can't rate/review your own blog post"


class AlreadyRated(APIException):
    status_code: int = 400
    default_detail: str = "You have already rated this blog post"
