from django.db.models import Manager

# create manager 

class BlogManager(Manager):
    def publish(self):
        return self.get_gueryset().filter(status='p')

