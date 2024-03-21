from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="Modern Blog API",
        default_version="v1",
        description="API endpoints for the Modern Blog API",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="modern_blog_api@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path(
        "swagger/<format>/", schema_view.without_ui(cache_timeout=0), name="schema-json"
    ),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    # setting admin to custom admin url path
    path(settings.ADMIN_URL, admin.site.urls),
    # user registration using djoser urls
    path("api/v1/auth/", include("djoser.urls")),
    path("api/v1/auth/", include("djoser.urls.jwt")),
    # route for profile
    path("api/v1/profiles/", include("core_apps.profiles.urls")),
    # route for blogs
    path("api/v1/blogs/", include("core_apps.blogs.urls")),
    # route for ratings
    path("api/v1/ratings/", include("core_apps.ratings.urls")),
    # route for blog reactions
    path("api/v1/vote/", include("core_apps.reactions.urls")),
    # route for favorting blogs
    path("api/v1/favorite/", include("core_apps.favorites.urls")),
    # route for blog comments
    path("api/v1/comments/", include("core_apps.comments.urls")),
    # route for searching with haystack
    path("api/v1/haystack/", include("core_apps.search.urls")),
]

admin.site.site_header = "Modern Blog API"
admin.site.site_title = "Modern Blog API Admin Portal"
admin.site.index_title = "Welcome to the Modern Blog API Portal"
