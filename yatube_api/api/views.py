from rest_framework import viewsets, permissions, mixins, filters
from posts.models import Post, Group, Comment, Follow
from django.shortcuts import get_object_or_404
from rest_framework.pagination import LimitOffsetPagination
from .serializers import (
    PostSerializer,
    GroupSerializer,
    CommentSerializer,
    FollowSerializer
)
from .permissions import AuthorPermission


class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        AuthorPermission
    ]
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = GroupSerializer
    queryset = Group.objects.all()
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        AuthorPermission
    ]


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        AuthorPermission
    ]

    def get_comment_post(self):
        return get_object_or_404(Post, id=self.kwargs.get("post_id"))

    def perform_create(self, serializer):
        post = self.get_comment_post()
        serializer.save(author=self.request.user, post=post)

    def get_queryset(self):
        post = self.get_comment_post()
        return post.comments.all()


class FollowViewSet(
    mixins.ListModelMixin,    # для GET со списком подписок
    mixins.CreateModelMixin,  # для POST
    viewsets.GenericViewSet
):
    serializer_class = FollowSerializer
    queryset = Follow.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['following__username']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return Follow.objects.filter(user=self.request.user)
