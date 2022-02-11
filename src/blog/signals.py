from django.db.models.signals import pre_save, post_delete
from django.utils.text import slugify
from django.dispatch import receiver

from extensions.code_generator import slug_generator

from os import getcwd, remove
from .models import Blog


@receiver(pre_save, sender=Blog)
def save_slug_blog(sender, instance, *args, **kwargs):
    if len(instance.slug) <= 5:
        instance.slug = slugify(slug_generator(10))


@receiver(post_delete, sender=Blog)
def delete_media_blog(sender, instance, *args, **kwargs):
    path = getcwd()
    final_path = path + instance.image.url 
    remove(final_path)