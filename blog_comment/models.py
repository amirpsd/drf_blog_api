from django.contrib.auth import get_user_model
from django.db import models

from blog.models import Blog
# Create your models here.

class Comment(models.Model):
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        default=None,
        blank=False,
        null=False,
    )
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        related_name='children',
        default=None,
        blank=True,
        null=True,
    )
    blog = models.ForeignKey(
        Blog,
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        related_name="comments",
    )
    body = models.TextField(max_length=300)
    create = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return self.user.username

    class Meta:
        ordering = ['-create', '-id',]
        verbose_name = "Comment"
        verbose_name_plural = "Comments"