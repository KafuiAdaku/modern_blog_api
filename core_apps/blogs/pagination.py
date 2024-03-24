from rest_framework.pagination import PageNumberPagination


class BlogPagination(PageNumberPagination):
    """
    Custom pagination for blog posts.

    This pagination class sets the default page size for blog posts.
    """

    # Set the default page size for blog posts
    page_size = 5
