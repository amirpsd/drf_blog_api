from django.db.models import Manager

# create manager 

class BlogManager(Manager):
    def publish(self):
        return self.filter(status='p')


class CategoryManager(Manager):
    def active(self):
        return self.filter(status=True)
