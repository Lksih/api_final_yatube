from rest_framework import serializers
from django.contrib.auth import get_user_model
from posts.models import Comment, Post, Group, Follow

User = get_user_model()


class PostSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        required=False, read_only=True, slug_field='username',)

    class Meta:
        fields = ('id', 'text', 'author', 'image', 'group', 'pub_date')
        model = Post


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        required=False, read_only=True, slug_field='username',)

    class Meta:
        fields = ('id', 'author', 'post', 'text', 'created')
        model = Comment
        read_only_fields = ('post',)


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'title', 'slug', 'description')
        model = Group


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )
    following = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all()
    )

    class Meta:
        fields = ('user', 'following')
        model = Follow

    def validate(self, data):
        request = self.context.get('request')
        following = data.get('following')

        if request and request.user.is_authenticated:
            if request.user == following:
                raise serializers.ValidationError(
                    "Зачем подписываться на самого себя?"
                )
            if Follow.objects.filter(
                user=request.user,
                following=following
            ).exists():
                raise serializers.ValidationError(
                    "Зачем подписываться на кого-то 2 раза?"
                )

        return data
