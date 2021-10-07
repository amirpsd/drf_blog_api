from django.db.models import Manager

# create manager 

class CategoryManager(Manager):
    def publish(self):
        return self.get_gueryset().filter(status=True)

