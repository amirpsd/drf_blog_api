from django.contrib.auth import get_user_model
from django.test import TestCase

from blog.models import Blog, Category

# Create your tests here.


class BlogTest(TestCase):

    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(phone="98912888888")
        self.blog = Blog.objects.create(
            author=self.user, 
            title='title-test-1',
            body='title-test-1', 
            summary="summary-test-1",
            special=True,
            status='p',
            visits=1,
        )

    def test_str_method(self):
        self.assertEquals(str(self.blog), f"{self.user.first_name} {self.blog.title}")
        self.assertNotEqual(str(self.blog), f"{self.user.first_name}")

    def test_blog_model(self):
        self.assertEquals(f"{self.blog.title}", "title-test-1")
        self.assertTrue(self.blog.special, True)
        self.assertNotEquals(self.blog.status, 'd')

    def test_is_generate_slug(self):
        self.assertIsNotNone(self.blog.slug)

    def test_the_profile_of_the_author_of_the_blog(self):
        self.assertEquals(self.blog.author.phone, "98912888888")
        self.assertNotEquals(self.blog.author.phone, "99999999999")

    def test_delete_blog(self):
        self.blog.delete()


class CategoryTest(TestCase):

    def setUp(self) -> None:
        self.category1 = Category.objects.create(
            title="category test 1",
            slug="category-test-1",
            status=True,
        )
        self.category2 = Category.objects.create(
            parent=self.category1,
            title="category test 2",
            slug="category-test-2",
            status=True,
        )

    def test_str_method(self):
        self.assertEquals(str(self.category1), self.category1.title)
        self.assertEquals(str(self.category2), self.category2.title)

    def test_category1_model(self):
        self.assertEquals(f"{self.category1.title}", "category test 1")
        self.assertEquals(self.category1.slug, "category-test-1")
        self.assertNotEquals(self.category1.status, False)

    def test_category2_model(self):
        self.assertEquals(f"{self.category2.title}", "category test 2")
        self.assertEquals(self.category2.slug, "category-test-2")
        self.assertNotEquals(self.category2.status, False)

    def test_parent_category(self):
        self.assertIsNone(self.category1.parent)
        self.assertEquals(str(self.category2.parent), self.category1.title)