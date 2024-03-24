from typing import Dict, List

from rest_framework import serializers

from core_apps.blogs.models import Blog, BlogViews
from core_apps.comments.serializers import CommentListSerializer
from core_apps.ratings.serializers import RatingSerializer

from .custom_tag_field import TagRelatedField


class BlogViewsSerializer(serializers.ModelSerializer):
    """
    Serializer for Blog Views.

    Serializes views of a blog.

    Attributes:
    - Meta: Metadata class for BlogViewsSerializer.
        - model: The model being serialized (BlogViews).
        - exclude: Fields to exclude from serialization.
    """

    class Meta:
        """
        Metadata class for BlogViewsSerializer.

        Attributes:
        - model: The model being serialized (BlogViews).
        - exclude: Fields to exclude from serialization (updated_at, pkid).
        """

        model = BlogViews
        exclude = ["updated_at", "pkid"]


class BlogSerializer(serializers.ModelSerializer):
    """
    Serializer for Blog.

    Serializes blog data.

    Attributes:
    - author_info: Serializer method field for author information.
    - banner_image: Serializer method field for fetching banner image.
    - read_time: Readonly field for blog read time.
    - ratings: Serializer method field for fetching ratings.
    - num_ratings: Serializer method field for counting ratings.
    - average_rating: Readonly field for average rating.
    - likes: Readonly field for blog likes.
    - dislikes: Readonly field for blog dislikes.
    - tagList: Custom tag field for tags associated with the blog.
    - comments: Serializer method field for fetching comments.
    - num_comments: Serializer method field for counting comments.
    - created_at: Serializer method field for fetching creation date.
    - updated_at: Serializer method field for fetching update date.

    Methods:
    - get_banner_image: Get the banner image for the blog.
    - get_created_at: Get the creation date of the blog.
    - get_updated_at: Get the update date of the blog.
    - get_author_info: Get the information of the author of the blog.
    - get_ratings: Get the ratings of the blog.
    - get_num_ratings: Get the count of ratings for the blog.
    - get_comments: Get the comments on the blog.
    - get_num_comments: Get the count of comments on the blog.

    Attributes:
    - Meta: Metadata class for BlogSerializer.
        - model: The model being serialized (Blog).
        - fields: Fields to include in serialization.
    """

    author_info = serializers.SerializerMethodField(read_only=True)
    banner_image = serializers.SerializerMethodField()
    read_time = serializers.ReadOnlyField(source="blog_read_time")
    ratings = serializers.SerializerMethodField()
    num_ratings = serializers.SerializerMethodField()
    average_rating = serializers.ReadOnlyField(source="get_average_rating")
    likes = serializers.ReadOnlyField(source="blog_reactions.likes")
    dislikes = serializers.ReadOnlyField(source="blog_reactions.dislikes")
    tagList = TagRelatedField(many=True, required=False, source="tags")
    comments = serializers.SerializerMethodField()
    num_comments = serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()

    def get_banner_image(self, obj: Blog) -> str:
        """
        Get the banner image for the blog.

        Args:
        - obj (Blog): Blog object.

        Returns:
        - str: URL of the banner image.
        """
        return obj.banner_image.url

    def get_created_at(self, obj: Blog) -> str:
        """
        Get the creation date of the blog.

        Args:
        - obj (Blog): Blog object.

        Returns:
        - str: Formatted creation date.
        """
        now = obj.created_at
        formatted_date = now.strftime("%m/%d/%Y, %H:%M:%S")
        return formatted_date

    def get_updated_at(self, obj: Blog) -> str:
        """
        Get the update date of the blog.

        Args:
        - obj (Blog): Blog object.

        Returns:
        - str: Formatted update date.
        """
        then = obj.updated_at
        formatted_date = then.strftime("%m/%d/%Y, %H:%M:%S")
        return formatted_date

    def get_author_info(self, obj: Blog) -> Dict:
        """
        Get the information of the author of the blog.

        Args:
        - obj (Blog): Blog object.

        Returns:
        - Dict: Author information.
        """
        return {
            "username": obj.author.username,
            "fullname": obj.author.get_full_name,
            "about_me": obj.author.profile.about_me,
            "profile_photo": obj.author.profile.profile_photo.url,
            "email": obj.author.email,
            "twitter_handle": obj.author.profile.twitter_handle,
            "facebook_account": obj.author.profile.facebook_account,
            "github_account": obj.author.profile.github_account,
        }

    def get_ratings(self, obj: Blog) -> List:
        """
        Get the ratings of the blog.

        Args:
        - obj (Blog): Blog object.

        Returns:
        - List: List of serialized ratings.
        """
        reviews = obj.blog_ratings.all()
        serializer = RatingSerializer(reviews, many=True)
        return serializer.data

    def get_num_ratings(self, obj: Blog) -> int:
        """
        Get the count of ratings for the blog.

        Args:
        - obj (Blog): Blog object.

        Returns:
        - int: Number of ratings.
        """
        num_reviews = obj.blog_ratings.all().count()
        return num_reviews

    def get_comments(self, obj: Blog) -> List:
        """
        Get the comments on the blog.

        Args:
        - obj (Blog): Blog object.

        Returns:
        - List: List of serialized comments.
        """
        comments = obj.comments.all()
        serializer = CommentListSerializer(comments, many=True)
        return serializer.data

    def get_num_comments(self, obj: Blog) -> int:
        """
        Get the count of comments on the blog.

        Args:
        - obj (Blog): Blog object.

        Returns:
        - int: Number of comments.
        """
        num_comments = obj.comments.all().count()
        return num_comments

    class Meta:
        """
        Metadata class for BlogSerializer.

        Attributes:
        - model: The model being serialized (Blog).
        - fields: Fields to include in serialization.
        """

        model = Blog
        fields = [
            "id",
            "title",
            "slug",
            "tagList",
            "description",
            "body",
            "banner_image",
            "read_time",
            "author_info",
            "likes",
            "dislikes",
            "ratings",
            "num_ratings",
            "average_rating",
            "views",
            "num_comments",
            "comments",
            "created_at",
            "updated_at",
        ]


class BlogCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating Blog.

    Serializes data required for creating a new blog.

    Attributes:
    - Meta: Metadata class for BlogCreateSerializer.
        - model: The model being serialized (Blog).
        - exclude: Fields to exclude from serialization (updated_at, pkid).
    """

    tags = TagRelatedField(many=True, required=False)
    banner_image = serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField()

    class Meta:
        """
        Meta class for BlogCreateSerializer.

        Attributes:
        - model: The model being serialized (Blog).
        - exclude: Fields to exclude from serialization
        (updated_at, pkid).
        """

        model = Blog
        exclude = ["updated_at", "pkid"]

    def get_created_at(self, obj: Blog) -> str:
        """
        Get the created at date.

        Args:
        - obj (Blog): The Blog object.

        Returns:
        - str: Formatted created at date.
        """
        now = obj.created_at
        formatted_date = now.strftime("%m/%d/%Y, %H:%M:%S")
        return formatted_date

    def get_banner_image(self, obj: Blog) -> str:
        """
        Get the banner image.

        Args:
        - obj (Blog): The Blog object.

        Returns:
        - str: URL of the banner image.
        """

        return obj.banner_image.url


class BlogUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating Blog.

    Serializes data required for updating an existing blog.

    Attributes:
    - Meta: Metadata class for BlogUpdateSerializer.
        - model: The model being serialized (Blog).
        - fields: Fields to include in serialization
            (title, description, body, banner_image, tags, updated_at).
    """

    tags = TagRelatedField(many=True, required=False)
    updated_at = serializers.SerializerMethodField()

    class Meta:
        """
        Meta class for BlogUpdateSerializer.

        Attributes:
        - model: The model being serialized (Blog).
        - fields: Fields to include in serialization
            (title, description, body, banner_image, tags, updated_at).
        """

        model = Blog
        fields = ["title", "description", "body", "banner_image", "tags", "updated_at"]

    def get_updated_at(self, obj: Blog) -> str:
        """
        Get the updated at date.

        Args:
        - obj (Blog): The Blog object.

        Returns:
        - str: Formatted updated at date.
        """
        then = obj.updated_at
        formatted_date = then.strftime("%m/%d/%Y, %H:%M:%S")
        return formatted_date
