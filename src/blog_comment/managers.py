from django.contrib.contenttypes.models import ContentType
from django.db import models

# create manager

class CommentManager(models.Manager):
	
    def filter_by_instance(self , instance):
        comment_for_model = ContentType.objects.get_for_model(instance)
        object_id = instance.id
        qs = self.filter(content_type=comment_for_model , object_id=object_id)
        return qs 