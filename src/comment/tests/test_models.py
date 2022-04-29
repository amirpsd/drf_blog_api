from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model
from django.test import TestCase

from comment.models import Comment
from blog.models import Blog

# Create your tests here.


class CommentTest(TestCase):

    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            phone="98912888888",
        )
        self.blog = Blog.objects.create(
            author=self.user, 
            title='title-test-1',
            body='title-test-1', 
            summary="summary-test-1",
            special=True,
            status='p',
            visits=1,
        )
        self.comment1 = Comment.objects.create(
            user=self.user,
            name="test-name-1",
            content_type=ContentType.objects.get_for_model(self.blog),
            object_id=self.blog.pk,
            parent=None,
            body="test-body-1",
        )
        self.comment2 = Comment.objects.create(
            user=self.user,
            name="test-name-2",
            content_type=ContentType.objects.get_for_model(self.blog),
            object_id=self.blog.pk,
            parent=self.comment1,
            body="test-body-2",
        )

    def test_str_method(self):
        self.assertEquals(str(self.comment1), self.user.phone)
        self.assertEquals(str(self.comment2), self.user.phone)
        self.assertNotEquals(str(self.comment1), self.user.first_name)

    def test_comment1_instance(self):
        self.assertEquals(self.comment1.body, "test-body-1")
        self.assertEquals(self.comment1.user, self.user)
        self.assertIsNone(self.comment1.parent)

    def test_comment2_instance(self):
        self.assertEquals(self.comment2.body, "test-body-2")
        self.assertEquals(self.comment2.user, self.user)
        self.assertIsNotNone(self.comment2.parent)

    def test_model_manager(self):
        query = Comment.objects.filter_by_instance(self.blog)
        self.assertQuerysetEqual(query, [self.comment2, self.comment1])

  