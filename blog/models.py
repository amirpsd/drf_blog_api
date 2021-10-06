from django.contrib.auth import get_user_model
from django.utils import timezone
from django.db import models

from blog_category.models import Category

from extensions.upload_file_path import upload_file_path



# Create your models here.

User = get_user_model()


class Blog(models.Model):
    STATUS_CHOICES = (
        ('p','publish'),
        ('d','draft'),
    )
    author = models.ForeignKey(
        User,
        default=None,
        null=True,
        on_delete=models.CASCADE,
        related_name='blogs',
    )
    category = models.ManyToManyField(
        Category,
        default=None,
        blank=True,
        related_name="blogs",
    )
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True,blank=True)
    body = models.TextField(blank=False)
    image = models.ImageField(upload_to=upload_file_path)
    publish = models.DateTimeField(default=timezone.now)
    create = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_special = models.BooleanField(default=False)
    status = models.CharField(max_length=1,choices=STATUS_CHOICES)


    def __str__(self):
        return  self.author.username + " | " + self.title 

    
    class Meta:
        ordering = ['-publish','-updated']
        verbose_name = "blog"
        verbose_name_plural = "blogs"