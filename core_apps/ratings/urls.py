from django.urls import path

from .views import create_blog_rating_view

urlpatterns = [path("<str:blog_id>/", create_blog_rating_view, name="rate-blog")]
