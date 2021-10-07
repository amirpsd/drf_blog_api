from django.db.models import Manager

# create manager 

class CategoryManager(Manager):
    def publish(self):
        return self.filter(status=True)

