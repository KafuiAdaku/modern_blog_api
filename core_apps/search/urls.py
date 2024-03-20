from django.urls import path
from rest_framework import routers

from .views import SearchBlogView

router = routers.DefaultRouter()
router.register("search", SearchBlogView, basename="search-article")

urlpatterns = [
    path("search/", SearchBlogView.as_view({"get": "list"}), name="search-article")
]
