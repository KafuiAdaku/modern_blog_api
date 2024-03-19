from django.urls import path
from .views import (
    BlogCreateAPIView,
    BlogDeleteAPIView,
    BlogDetailView,
    BlogListAPIView,
    update_blog_api_view,
)

urlpatterns = [
    path("all/", BlogListAPIView.as_view(), name="all-blogs"),
    path("create/", BlogCreateAPIView.as_view(), name="create-blogs"),
    path("details/<slug:slug>/", BlogDetailView.as_view(), name="blog-detail"),
    path("delete/<slug:slug>/",
         BlogDeleteAPIView.as_view(), name="delete-blog"),
    path("update/<slug:slug>/", update_blog_api_view, name="update-blog"),
]
