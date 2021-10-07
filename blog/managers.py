from django.db.models import Manager

# create manager 

class BlogManager(Manager):
    def publish(self):
        return self.filter(status='p')

