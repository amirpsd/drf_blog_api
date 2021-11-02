from rest_framework import serializers

from blog_comment.models import Comment


class CommentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = [
            'name',
            'body',           
            'rate', 
            'object_id',
        ]
