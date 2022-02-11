from django.contrib.contenttypes.models import ContentType
from django.db import models

# Create Manager

class CommentManager(models.Manager):
	
    def filter_by_instance(self , instance):
        comment = ContentType.objects.get_for_model(instance)
        object_id = instance.id
        query = self.filter(content_type=comment, object_id=object_id)
        return query 