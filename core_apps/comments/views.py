from rest_framework import generics, permissions, status
from rest_framework.exceptions import NotFound
from rest_framework.response import Response

from core_apps.blogs.models import Blog

from .models import Comment
from .serializers import CommentListSerializer, CommentSerializer


class CommentAPIView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CommentSerializer

    def post(self, request: Request, **kwargs: dict) -> Response:
        """Create a new comment."""
        try:
            slug = self.kwargs.get("slug")
            blog = Blog.objects.get(slug=slug)
        except Blog.DoesNotExist:
            raise NotFound("That blog does not exist in our catalog")

        comment = request.data
        author = request.user
        comment["author"] = author.pkid
        comment["blog"] = blog.pkid
        serializer = self.serializer_class(data=comment)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request: Request, **kwargs: dict) -> Response:
        """Get all comments for a blog."""
        try:
            slug = self.kwargs.get("slug")
            blog = Blog.objects.get(slug=slug)
        except Blog.DoesNotExist:
            raise NotFound("That blog does not exist in our catalog")

        try:
            comments = Comment.objects.filter(article_id=blog.pkid)
        except Comment.DoesNotExist:
            raise NotFound("No comments found")

        serializer = CommentListSerializer(
            comments, many=True, context={"request": request}
        )
        return Response(
            {"num_comments": len(serializer.data), "comments": serializer.data},
            status=status.HTTP_200_OK,
        )


class CommentUpdateDeleteAPIView(generics.GenericAPIView):
    """Update and delete a comment class"""
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CommentSerializer

    def put(self, request: Request, slug: str, id: int) -> Response:
        """Update a comment."""
        try:
            comment_to_update = Comment.objects.get(id=id)
        except Comment.DoesNotExist:
            raise NotFound("Comment does not exist")

        data = request.data
        serializer = self.serializer_class(comment_to_update, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response = {
            "message": "Comment updated successfully",
            "comment": serializer.data,
        }
        return Response(response, status=status.HTTP_200_OK)

    def delete(self, request: Request, slug: str, id: int) -> Response:
        """Delete a comment."""
        try:
            comment_to_delete = Comment.objects.get(id=id)
        except Comment.DoesNotExist:
            raise NotFound("Comment does not exist")

        comment_to_delete.delete()
        response = {"message": "Comment deleted successfully!"}
        return Response(response, status=status.HTTP_200_OK)
