from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.db import models

from .managers import CommentManager

# Create your models here.


class Comment(models.Model):
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name=_("User"),
    )
    name = models.CharField(
        max_length=20, null=True, blank=True, verbose_name=_("Name")
    )
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        related_name="comments",
    )
    object_id = models.PositiveIntegerField(verbose_name=_("object id"))
    content_object = GenericForeignKey("content_type", "object_id")
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        related_name="children",
        null=True,
        blank=True,
        verbose_name=_("parent"),
    )
    body = models.TextField(verbose_name=_("Body"))
    create = models.DateTimeField(auto_now_add=True, verbose_name=_("Create time"))
    updated = models.DateTimeField(auto_now=True, verbose_name=_("Update time"))

    def __str__(self):
        return self.user.phone

    objects = CommentManager()

    class Meta:
        ordering = [
            "-create",
            "-id",
        ]
        verbose_name = _("Comment")
        verbose_name_plural = _("Comments")
