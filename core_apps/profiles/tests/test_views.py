import pytest
from django.test import RequestFactory
from rest_framework.exceptions import NotFound

from core_apps.profiles.views import (FollowUnfollowAPIView,
                                      ProfileDetailAPIView,
                                      ProfileListAPIView)
from core_apps.profiles.models import Profile


def test_get_profile_queryset(profile, rf: RequestFactory):
    """Test get profile queryset"""
    view = ProfileListAPIView()
    request = rf.get("/not-real-url/")
    request.user = profile.user

    view.request = request

    assert profile in view.queryset

def test_get_user_profile_wrong_username(profile, rf: RequestFactory):
    """Test get user profile wrong username"""
    view = ProfileDetailAPIView()
    request = rf.get("/not-real-url/")
    request.user = profile.user

    view.request = request

    with pytest.raises(NotFound) as err:
        view.retrieve(request, username="not-real-username")
    assert str(err.value) == "A profile with this username does not exist"

def test_get_profile_detail(profile, rf: RequestFactory):
    """Test get profile detail"""
    view = ProfileDetailAPIView()
    request = rf.get("/not-real-url/")
    request.user = profile.user

    view.request = request

    profile = view.queryset.first()
    response = view.retrieve(request, username=profile.user.username)

    assert response.status_code == 200
    assert response.data["username"] == profile.user.username
    assert response.data["first_name"] == profile.user.first_name
    assert response.data["email"] == profile.user.email
    assert response.data["about_me"] == profile.about_me

def test_follow_unfollow_user(test_profile, test_profile2, rf: RequestFactory):
    """Test follow unfollow user"""
    view = FollowUnfollowAPIView()
    request = rf.post("/not-real-url/")
    request.user = test_profile.user

    view.request = request
    response = view.post(request, username=test_profile2.user.username)
    
    assert response.status_code == 200
    assert response.data["detail"] == f"You now follow {test_profile2.user.username}"
