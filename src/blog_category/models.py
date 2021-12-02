from django.utils.translation import gettext as _
from django.db import models

from .managers import CategoryManager

# Create your models here.


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
