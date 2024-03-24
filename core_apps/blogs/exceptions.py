from rest_framework.exceptions import APIException


class UpdateBlog(APIException):
    """
    Exception for updating a blog.

    This exception is raised when a user tries to update
        a blog that does not belong to them.

    Attributes:
    - status_code (int): HTTP status code for the exception.
    - default_detail (str): Default detail message for
        the exception.
    """

    status_code = 403
    default_detail = "You can't update a blog that does not belong to you'"
