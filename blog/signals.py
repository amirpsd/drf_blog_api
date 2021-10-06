from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.dispatch import receiver

from extensions.code_generator import code_generator

from .models import Blog

@receiver(pre_save, sender=Blog)
def save_slug_blog(sender,instance,*args,**kwargs):
    if len(instance.slug) <= 5:
        instance.slug = slugify(code_generator(10)) 