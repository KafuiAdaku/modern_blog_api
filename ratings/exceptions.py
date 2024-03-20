from rest_framework.exceptions import APIException


class CantRateYourBlog(APIException):
    status_code: int = 403
    default_detail: str = "You can't rate/review your own blog post"


class AlreadyRated(APIException):
    status_code: int = 400
    default_detail: str = "You have already rated this blog post"
