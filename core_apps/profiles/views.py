from typing import Dict, Union

from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.http import HttpRequest
from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from modern_blog_api.settings.development import DEFAULT_FROM_EMAIL

from .exceptions import CantFollowYourself, NotYourProfile
from .models import Profile
from .pagination import ProfilePagination
from .renderers import ProfileJSONRenderer, ProfilesJSONRenderer
from .serializers import FollowingSerializer, ProfileSerializer, UpdateProfileSerializer

# Get user model
User = get_user_model()


# View for listing profiles
class ProfileListAPIView(generics.ListAPIView):
    """
    API view to list profiles.
    """

    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Profile.objects.all()
    renderer_classes = (ProfilesJSONRenderer,)
    pagination_class = ProfilePagination


class ProfileDetailAPIView(generics.RetrieveAPIView):
    """
    API view to retrieve profile details.
    """

    permission_classes = [permissions.IsAuthenticated]
    queryset = Profile.objects.select_related("user")
    serializer_class = ProfileSerializer
    renderer_classes = (ProfileJSONRenderer,)

    def retrieve(
        self,
        request: HttpRequest,
        username: str,
        *args: Union[str, int],
        **kwargs: Dict,
    ):
        try:
            profile = self.queryset.get(user__username=username)
        except Profile.DoesNotExist:
            raise NotFound("A profile with this username does not exist")

        serializer = self.serializer_class(profile, context={"request": request})

        return Response(serializer.data, status=status.HTTP_200_OK)


class UpdateProfileAPIView(APIView):
    """
    API view to update a profile.
    """

    permission_classes = [permissions.IsAuthenticated]
    queryset = Profile.objects.select_related("user")
    renderer_classes = [ProfileJSONRenderer]
    serializer_class = UpdateProfileSerializer

    def patch(self, request: HttpRequest, username: str) -> Response:
        try:
            self.queryset.get(user__username=username)
        except Profile.DoesNotExist:
            raise NotFound("A profile with this username does not exist")

        user_name = request.user.username
        if user_name != username:
            raise NotYourProfile

        data = request.data
        # # Print the data before saving
        # print("Data before saving:", data)

        serializer = UpdateProfileSerializer(
            instance=request.user.profile, data=data, partial=True
        )

        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            print("Validation error:", e.detail)

        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


# change to class based view soon
@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def get_my_followers(request: Request, username: str) -> Response:
    try:
        specific_user = User.objects.get(username=username)
    except User.DoesNotExist:
        raise NotFound("User with that username does not exist")

    userprofile_instance = Profile.objects.get(user__pkid=specific_user.pkid)

    user_followers = userprofile_instance.followed_by.all()
    serializer = FollowingSerializer(user_followers, many=True)
    formatted_response = {
        "status_code": status.HTTP_200_OK,
        "followers": serializer.data,
        "num_of_followers": len(serializer.data),
    }

    return Response(formatted_response, status=status.HTTP_200_OK)


class FollowUnfollowAPIView(generics.GenericAPIView):
    """
    API view to follow/unfollow a user.
    """

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FollowingSerializer

    def get(self, request: HttpRequest, username: str) -> Response:
        try:
            specific_user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise NotFound("User with that username does not exist")

        userprofile_instance = Profile.objects.get(user__pkid=specific_user.pkid)
        my_following_list = userprofile_instance.following_list()
        serializer = ProfileSerializer(my_following_list, many=True)
        formatted_response = {
            "status_code": status.HTTP_200_OK,
            "users_i_follow": serializer.data,
            "num_users_i_follow": len(serializer.data),
        }
        return Response(formatted_response, status=status.HTTP_200_OK)

    def post(self, request: HttpRequest, username: str) -> Response:
        try:
            specific_user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise NotFound("User with that username does not exist")

        if specific_user.pkid == request.user.pkid:
            raise CantFollowYourself

        userprofile_instance = Profile.objects.get(user__pkid=specific_user.pkid)
        current_user_profile = request.user.profile

        if current_user_profile.check_following(userprofile_instance):
            formatted_response = {
                "status_code": status.HTTP_400_BAD_REQUEST,
                "errors": f"You already follow {specific_user.username}",
            }
            return Response(formatted_response, status=status.HTTP_400_BAD_REQUEST)

        current_user_profile.follow(userprofile_instance)

        subject = "A new user follows you"
        message = f"Hi there {specific_user.username}!!, the user {current_user_profile.user.username} now follows you"
        from_email = DEFAULT_FROM_EMAIL
        recipient_list = [specific_user.email]
        send_mail(subject, message, from_email, recipient_list, fail_silently=True)

        return Response(
            {
                "status_code": status.HTTP_200_OK,
                "detail": f"You now follow {specific_user.username}",
            }
        )

    def delete(self, request: HttpRequest, username: str) -> Response:
        try:
            specific_user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise NotFound("User with that username does not exist")

        userprofile_instance = Profile.objects.get(user__pkid=specific_user.pkid)
        current_user_profile = request.user.profile

        if not current_user_profile.check_following(userprofile_instance):
            formatted_response = {
                "status_code": status.HTTP_400_BAD_REQUEST,
                "errors": f"You do not follow {specific_user.username}",
            }
            return Response(formatted_response, status=status.HTTP_400_BAD_REQUEST)

        current_user_profile.unfollow(userprofile_instance)
        formatted_response = {
            "status_code": status.HTTP_200_OK,
            "detail": f"You have unfollowed {specific_user.username}",
        }
        return Response(formatted_response, status=status.HTTP_200_OK)
