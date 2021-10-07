from django.db import models

from .managers import CategoryManager

# Create your models here.

class Category(models.Model):
    parent = models.ForeignKey(
        'self',
        null=True,
        default=None,
        blank=True,
        on_delete=models.CASCADE,
        related_name='children',
    )
    title = models.CharField(max_length=150,blank=False)
    slug = models.SlugField(unique=True,blank=False)
    status = models.BooleanField(default=False)


    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-id']
        verbose_name = 'category'
        verbose_name_plural = 'categories' 

    objects = CategoryManager()
    