from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.test import APITestCase
from rest_framework import status

import json

from comment.api import serializers
from comment.models import Comment
from blog.models import Blog

# Create your tests here.


class ViewsTest(APITestCase):

    def setUp(self) -> None:
        self.user1 = get_user_model().objects.create_user(
            phone="98912888888",
        )
        self.refresh_for_user1 = RefreshToken.for_user(self.user1)

        self.user2 = get_user_model().objects.create_user(
            phone="98912888889",
        )
        self.refresh_for_user2 = RefreshToken.for_user(self.user2)

        self.blog = Blog.objects.create(
            id=1,
            author=self.user1,
            title="title-test-1",
            body="title-test-1",
            summary="summary-test-1",
            special=True,
            status="p",
            visits=1,
        )
        self.comment1 = Comment.objects.create(
            user=self.user1,
            name="test-name-1",
            content_type=ContentType.objects.get_for_model(self.blog),
            object_id=1,
            parent=None,
            body="test-body-1",
        )
        self.comment2 = Comment.objects.create(
            user=self.user1,
            name="test-name-2",
            content_type=ContentType.objects.get_for_model(self.blog),
            object_id=1,
            parent=self.comment1,
            body="test-body-2",
        )
        self.valid_data = {
            "object_id": self.blog.pk,
            "name": "test-name-3",
            "body": "test-body-3",
            "parent": None,
        }
        self.updated_data = {
            "object_id": self.blog.pk,
            "name": "update-test-name-3",
            "body": "update-test-body-3",
            "parent": self.comment1.pk,
        }
        self.invalid_data = {
            "name": "invalid-data-test-invalid-data-test",
        }

    def test_comments_list(self):
        path = reverse("comment:api:list", args=[self.blog.pk])
        response = self.client.get(path)
        blog = Blog.objects.publish().get(pk=self.blog.pk)
        comment = Comment.objects.filter_by_instance(blog)
        serializer = serializers.CommentListSerializer(comment, many=True)

        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data, serializer.data)

    def test_comment_create(self):
        path = reverse("comment:api:create")
        serializer = serializers.CommentUpdateCreateSerializer(data=self.valid_data)
        serializer.is_valid(raise_exception=True)

        response = self.client.post(
            path=path,
            data=serializer.data,
        )
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.refresh_for_user1.access_token}"
        )
        response = self.client.post(
            path=path,
            data=serializer.data,
        )
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertEquals(json.loads(response.content), self.valid_data)

    def test_comment_create_with_invalid_data(self):
        path = reverse("comment:api:create")
        data = json.dumps(self.invalid_data)

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.refresh_for_user1.access_token}"
        )
        response = self.client.post(
            path=path,
            data=data,
        )
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_comment_update(self):
        path = reverse("comment:api:update-delete", args=[self.comment1.pk])
        serializer = serializers.CommentUpdateCreateSerializer(data=self.updated_data)
        serializer.is_valid(raise_exception=True)

        response = self.client.put(
            path=path,
            data=serializer.data,
        )
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.refresh_for_user1.access_token}"
        )
        response = self.client.put(
            path=path,
            data=serializer.data,
        )
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(json.loads(response.content), self.updated_data)

    def test_comment_update_with_invalid_data(self):
        path = reverse("comment:api:update-delete", args=[self.comment1.pk])
        invalid_data = json.dumps(self.invalid_data)

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.refresh_for_user1.access_token}"
        )
        response = self.client.put(
            path=path,
            data=invalid_data,
        )
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_comment_delete(self):
        path = reverse("comment:api:update-delete", args=[self.comment1.pk])

        response = self.client.delete(path)
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.refresh_for_user2.access_token}"
        )
        response = self.client.delete(path)
        self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND)

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.refresh_for_user1.access_token}"
        )
        response = self.client.delete(path)
        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)
