from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.db import models

from extensions.upload_file_path import upload_file_path

from .managers import BlogManager, CategoryManager


# Create your models here.



class Blog(models.Model):
    STATUS_CHOICES = (
        ("p", "publish"),
        ("d", "draft"),
    )
    author = models.ForeignKey(
        get_user_model(),
        default=None,
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        related_name="blogs",
        verbose_name=_("Author"),
    )
    category = models.ManyToManyField(
        "Category",
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
    image = models.ImageField(
        upload_to=upload_file_path, blank=True,
        null=True, verbose_name=_("Image"),
    )
    summary = models.TextField(max_length=400, verbose_name=_("Summary"))
    likes = models.ManyToManyField(
        get_user_model(),
        blank=True,
        related_name="blogs_like",
        verbose_name=_("Likes"),
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
        return f"{self.author.first_name} {self.title}"

    class Meta:
        ordering = ["-publish", "-updated"]
        verbose_name = _("Blog")
        verbose_name_plural = _("Blogs")

    objects = BlogManager()


class Category(models.Model):
    parent = models.ForeignKey(
        "self",
        null=True,
        default=None,
        blank=True,
        on_delete=models.CASCADE,
        related_name="children",
        verbose_name=_("Subcategory"),
    )
    title = models.CharField(max_length=150, blank=False, verbose_name=_("Title"))
    slug = models.SlugField(
        unique=True,
        blank=False,
        verbose_name=_("Slug"),
        help_text=_("Do not fill in here"),
    )
    status = models.BooleanField(default=False, verbose_name=_("Status"))

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-id"]
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    objects = CategoryManager()
