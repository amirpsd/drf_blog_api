from django.utils.translation import gettext as _
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.db import models

from blog_category.models import Category

from extensions.upload_file_path import upload_file_path

from .managers import BlogManager


# Create your models here.

User = get_user_model()


class Blog(models.Model):
    STATUS_CHOICES = (
        ("p", "publish"),
        ("d", "draft"),
    )
    author = models.ForeignKey(
        User,
        default=None,
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        related_name="blogs",
        verbose_name=_("Author"),
    )
    category = models.ManyToManyField(
        Category,
        default=None,
        blank=True,
        related_name="blogs",
        verbose_name=_("Categories"),
    )
    title = models.CharField(max_length=200, verbose_name=_("Title"))
    slug = models.SlugField(
        unique=True,
        blank=True,
        verbose_name=_("Slug"),
        help_text=_("Do not fill in here"),
    )
    body = models.TextField(blank=False, verbose_name=_("Content"))
    image = models.ImageField(upload_to=upload_file_path, verbose_name=_("Image"))
    summary = models.TextField(max_length=400, verbose_name=_("Summary"))
    likes = models.ManyToManyField(
        get_user_model(),
        blank=True,
        related_name="likes",
        verbose_name=_("Likes"),
    )
    dislikes = models.ManyToManyField(
        get_user_model(),
        blank=True,
        related_name="dislikes",
        verbose_name=_("Dislikes"),
    )
    publish = models.DateTimeField(default=timezone.now, verbose_name=_("Publish time"))
    create = models.DateTimeField(auto_now_add=True, verbose_name=_("Create time"))
    updated = models.DateTimeField(auto_now=True, verbose_name=_("Update time"))
    special = models.BooleanField(default=False, verbose_name=_("Is special Blog ?"))
    status = models.CharField(
        max_length=1, choices=STATUS_CHOICES, verbose_name=_("Status")
    )
    visits = models.PositiveIntegerField(default=0, verbose_name=_("Visits"))

    def __str__(self):
        return self.author.username + " | " + self.title

    class Meta:
        ordering = ["-publish", "-updated"]
        verbose_name = _("Blog")
        verbose_name_plural = _("Blogs")

    objects = BlogManager()
