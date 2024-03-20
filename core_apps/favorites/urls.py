from django.urls import path

from . import views

urlpatterns = [
    path(
        "blogs/me/",
        views.ListUserFavoriteBlogsAPIView.as_view(),
        name="my-favorites",
    ),
    path("<slug:slug>/", views.FavoriteAPIView.as_view(), name="favorite-blogs"),
]
