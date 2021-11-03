from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model
from django.db import models

from .managers import CommentManager

# Create your models here.


class Comment(models.Model):
    user = models.ForeignKey(
        get_user_model(), 
        on_delete=models.CASCADE, 
        related_name="comments",
    )
    name = models.CharField(max_length=20, null=True, blank=True)
    content_type = models.ForeignKey(
        ContentType, 
        on_delete=models.CASCADE, 
        related_name="comments",
    )
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    body = models.TextField()
    create = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.user.username

    objects = CommentManager()

    class Meta:
        ordering = ['-create', '-id',]
        verbose_name = "Comment"
        verbose_name_plural = "Comments"

