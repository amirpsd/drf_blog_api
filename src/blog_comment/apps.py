from django.apps import AppConfig


class BlogCommentConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'blog_comment'
    verbose_name = "Comments"