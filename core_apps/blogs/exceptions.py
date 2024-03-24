from rest_framework.exceptions import APIException


class UpdateBlog(APIException):
    """Update Blog Exception"""
    status_code = 403
    default_detail = "You can't update a blog that does not belong to you'"
