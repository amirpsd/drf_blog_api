from rest_framework import serializers

from blog.models import Blog

# create serializers 

class BlogListSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField(method_name='get_author')
    category = serializers.SerializerMethodField(method_name='get_category')

    def get_author(self,obj):
        return {
            "username":obj.author.username,
            "first_name":obj.author.first_name,
            "last_name":obj.author.last_name,
        }

    def get_category(self,obj):
        category = [cat.title for cat in obj.category.get_queryset()]
        return category

    class Meta:
        model = Blog
        exclude = [
            'id',
            'create',
            'body',
            'status',
            'updated',
        ]


class BlogCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Blog
        fields = [
            'title',
            'body',
            'image',
            'summary',
            'category',
            'publish',
            'special',
            'status',
        ]

class BlogDetailUpdateDeleteSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField(method_name='get_author')
    slug = serializers.ReadOnlyField()

    def get_author(self,obj):
        return {
            "username":obj.author.username,
            "first_name":obj.author.first_name,
            "last_name":obj.author.last_name,
        }

    class Meta:
        model = Blog
        fields = [
            'id',
            'author',
            'title',
            'slug',
            'body',
            'image',
            'category',
            'publish',
            'special',
            'status',
            'updated',
        ]