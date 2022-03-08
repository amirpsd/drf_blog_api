from django.urls import reverse, resolve
from django.test import SimpleTestCase

from blog.api import views


# Create your tests here.

class UrlsTest(SimpleTestCase):

    def test_app_name(self):
        self.assertEquals(resolve("/blog/api/").app_name, "blog:api")

    def test_blog_list(self):
        path = reverse('blog:api:list')
        self.assertEquals(resolve(path).func.view_class, views.BlogsList)

    def test_blog_create(self):
        path = reverse('blog:api:create')
        self.assertEquals(resolve(path).func.view_class, views.BlogCreate)
        self.assertNotEquals(resolve(path).func.view_class, views.BlogsList)

    def test_category_list(self):
        path = reverse('blog:api:category-list')
        self.assertEquals(resolve(path).func.view_class, views.CategoryList)

    def test_category_blog(self):
        path = reverse('blog:api:category-blog', args=["test-category-slug"])
        self.assertEquals(resolve(path).func.view_class, views.CategoryBlog)

    def test_blog_detail(self):
        path = reverse('blog:api:detail', args=["test-blog-slug"])
        self.assertEquals(resolve(path).func.view_class, views.BlogDetailUpdateDelete)
        self.assertNotEquals(resolve(path).func.view_class, views.BlogCreate)

    def test_like_blog(self):
        path = reverse('blog:api:like', args=[1])
        self.assertEquals(resolve(path).func.view_class, views.LikeBlog)
