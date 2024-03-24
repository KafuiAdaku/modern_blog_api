from rest_framework.pagination import PageNumberPagination


class ProfilePagination(PageNumberPagination):
    """
    Pagination class for profile lists.

    This class defines the pagination behavior for profile lists.

    Attributes:
    - page_size (int): Number of profiles to include in each page.
    """

    page_size: int = 3
