from rest_framework import serializers

from core_apps.articles.models import Article, ArticleViews
from core_apps.comments.serializers import CommentListSerializer
from core_apps.ratings.serializers import RatingSerializer

from .custom_tag_field import TagRelatedField


class BlogViewsSerializer(serializers.ModelSerializer):
    """Blog views serializer"""
    class Meta:
        """Meta class"""
        model = BlogViews
        exclude = ["updated_at", "pkid"]


class BlogSerializer(serializers.ModelSerializer):
    """Blog serializer"""
    author_info = serializers.SerializerMethodField(read_only=True)
    banner_image = serializers.SerializerMethodField()
    read_time = serializers.ReadOnlyField(source="article_read_time")
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
        """Get the banner image"""
        return obj.banner_image.url

    def get_created_at(self, obj: Blog) -> str:
        """Get the created at date"""
        now = obj.created_at
        formatted_date = now.strftime("%m/%d/%Y, %H:%M:%S")
        return formatted_date

    def get_updated_at(self, obj: Blog) -> str:
        """Get the updated at date"""
        then = obj.updated_at
        formatted_date = then.strftime("%m/%d/%Y, %H:%M:%S")
        return formatted_date

    def get_author_info(self, obj: Blog) -> dict:
        """Get the author info"""
        return {
            "username": obj.author.username,
            "fullname": obj.author.get_full_name,
            "about_me": obj.author.profile.about_me,
            "profile_photo": obj.author.profile.profile_photo.url,
            "email": obj.author.email,
            "twitter_handle": obj.author.profile.twitter_handle,
        }

    def get_ratings(self, obj: Blog) -> list:  # check typing
        """Get the ratings"""
        reviews = obj.blog_ratings.all()
        serializer = RatingSerializer(reviews, many=True)
        return serializer.data

    def get_num_ratings(self, obj: Blog) -> int:
        """Get the number of ratings"""
        num_reviews = obj.blog_ratings.all().count()
        return num_reviews

    def get_comments(self, obj: Blog) -> list:  # check typing
        """Get the comments"""
        comments = obj.comments.all()
        serializer = CommentListSerializer(comments, many=True)
        return serializer.data

    def get_num_comments(self, obj: Blog) -> int:
        """Get the number of comments"""
        num_comments = obj.comments.all().count()
        return num_comments

    class Meta:
        """Meta class"""
        model = Article
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
    tags = TagRelatedField(many=True, required=False)
    banner_image = serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField()

    class Meta:
        """Meta class"""
        model = Blog
        exclude = ["updated_at", "pkid"]

    def get_created_at(self, obj: Blog) -> str:
        """Get the created at date"""
        now = obj.created_at
        formatted_date = now.strftime("%m/%d/%Y, %H:%M:%S")
        return formatted_date

    def get_banner_image(self, obj: Blog) -> str:
        """Get the banner image"""
        return obj.banner_image.url


class BlogUpdateSerializer(serializers.ModelSerializer):
    tags = TagRelatedField(many=True, required=False)
    updated_at = serializers.SerializerMethodField()

    class Meta:
        """Meta class"""
        model = Blog
        fields = ["title", "description", "body",
                  "banner_image", "tags", "updated_at"]

    def get_updated_at(self, obj: Blog) -> str:
        """Get the updated at date"""
        then = obj.updated_at
        formatted_date = then.strftime("%m/%d/%Y, %H:%M:%S")
        return formatted_date
