from rest_framework import serializers

from blog_comment.models import Comment


class CommentListSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    def get_user(self, obj):
        return {
            "name":obj.user.first_name,
        }


    class Meta:
        model = Comment
        fields = [
            'user',
            'name',
            'parent',
            'body',
            'create',
            'object_id',
        ]


class CommentUpdateCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = [
            'object_id',
            'name',
            'parent',
            'body',
        ]