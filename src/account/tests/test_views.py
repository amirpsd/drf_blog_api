from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.utils import timezone
from django.urls import reverse

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.test import APITestCase
from rest_framework import status

from account.api import serializers

from datetime import timedelta
import json

# Create your tests here.


class ViewsTest(APITestCase):
    
    def setUp(self) -> None:
        cache.clear()

        self.user = get_user_model().objects.create_user(
            phone="989101115874",
            first_name="test-user-first-name",
            last_name="test-user-last-name",
            special_user=timezone.now() + timedelta(days=30),
        )
        self.refresh_for_user = RefreshToken.for_user(self.user)

        self.author = get_user_model().objects.create_user(
            phone="989101115875",
            first_name="test-author-first-name",
            last_name="test-author-last-name",
            author=True,
        )
        self.refresh_for_author = RefreshToken.for_user(self.author)

        self.superuser = get_user_model().objects.create_superuser(
            phone="989101115876",
            first_name="test-superuser-first-name",
            last_name="test-superuser-last-name",
        )
        self.refresh_for_superuser = RefreshToken.for_user(self.superuser)

        self.invalid_phone = {
            "phone": "450404146044",
        }
        self.user_phone = {
            "phone": f"{self.user.phone}",
        }
        self.new_phone = {
            "phone": "989101115878",
        }

    def test_users_list_with_user(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.refresh_for_user.access_token}"
        )
        response = self.client.get(reverse("account:api:users-list"))

        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_users_list_with_author(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.refresh_for_author.access_token}"
        )
        response = self.client.get(reverse("account:api:users-list"))

        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_users_list_with_superuser(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.refresh_for_superuser.access_token}"
        )
        response = self.client.get(reverse("account:api:users-list") + "?ordering=id")
        users = get_user_model().objects.all()
        serializer = serializers.UsersListSerializer(users, many=True)

        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data, serializer.data)

    def test_search_users_list(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.refresh_for_superuser.access_token}"
        )
        path = reverse("account:api:users-list")

        response = self.client.get(path + "?ordering=-id&search=wrong+search")
        content = json.loads(response.content)
        self.assertEquals(len(content), 0)

        response = self.client.get(path + "?ordering=-id&search=test-user")
        content = json.loads(response.content)
        self.assertEquals(len(content), 1)

        response = self.client.get(path + "?ordering=id&author=true")
        content, data = json.loads(response.content), response.data
        self.assertEquals(len(content), 1)
        self.assertEquals(data[0]["phone"], self.author.phone)

    def test_users_detail(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.refresh_for_superuser.access_token}"
        )
        path = reverse("account:api:users-detail", kwargs={"pk": self.user.pk})
        response = self.client.get(path=path)

        user = get_user_model().objects.get(pk=self.user.pk)
        serializer = serializers.UserDetailUpdateDeleteSerializer(user)

        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data, serializer.data)

        path = reverse("account:api:users-detail", kwargs={"pk": "0"})
        response = self.client.get(path=path)
        self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_profile(self):
        path = reverse("account:api:profile")
        response = self.client.get(path)
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.refresh_for_user.access_token}"
        )
        response = self.client.get(path)
        serializer = serializers.UserProfileSerializer(self.user)

        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data, serializer.data)

    def test_update_profile(self):
        path = reverse("account:api:profile")

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.refresh_for_user.access_token}"
        )
        updated_data = {
            "first_name": "update-test-user-first-name",
            "last_name": "update-test-user-last-name",
        }
        response = self.client.put(
            path=path,
            data=updated_data,
        )
        content = json.loads(response.content)

        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(content.get("first_name"), updated_data.get("first_name"))

    def test_login_with_invalid_phone(self):
        path = reverse("account:api:login")
        response = self.client.post(
            path=path,
            data=self.invalid_phone,
        )

        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_with_unavailable_number(self):
        path = reverse("account:api:login")
        response = self.client.post(
            path=path,
            data=self.new_phone,
        )

        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_with_user(self):
        path = reverse("account:api:login")
        response = self.client.post(
            path=path,
            data=self.user_phone,
        )
        otp_code = {
            "code": json.loads(response.content).get("otp"),
        }

        path = reverse("account:api:verify-otp")
        wrong_otp_code = {
            "code": "566486",
        }
        response = self.client.post(
            path=path,
            data=wrong_otp_code,
        )
        self.assertEquals(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)

        response = self.client.post(
            path=path,
            data=otp_code,
        )
        content = json.loads(response.content)

        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertTrue(content["refresh"], content["access"])
        self.assertFalse(content["created"])

    def test_login_with_two_step_password(self):
        self.author.set_password("test")
        self.author.two_step_password = True
        self.author.save(update_fields=["password", "two_step_password"])

        path = reverse("account:api:login")
        author_phone = {
            "phone": f"{self.author.phone}",
        }
        response = self.client.post(
            path=path,
            data=author_phone,
        )
        otp_code = {
            "code": json.loads(response.content).get("otp"),
        }

        path = reverse("account:api:verify-otp")
        response = self.client.post(
            path=path,
            data=otp_code,
        )
        self.assertEquals(response.status_code, status.HTTP_200_OK)

        path = reverse("account:api:verify-two-step-password")
        wrong_two_step_password = {
            "password": "test1",
            "confirm_password": "test1",
        }
        response = self.client.post(
            path=path,
            data=wrong_two_step_password,
        )
        self.assertEquals(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)

        two_step_password = {
            "password": "test",
            "confirm_password": "test",
        }
        response = self.client.post(
            path=path,
            data=two_step_password,
        )
        content = json.loads(response.content)

        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertTrue(content["refresh"], content["access"])

    def test_throttling_login_view(self):
        path = reverse("account:api:login")
        for _ in range(6):
            response = self.client.post(
                path=path,
                data=self.user_phone,
            )

        self.assertEquals(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)

    def test_valid_otp_code(self):
        path = reverse("account:api:verify-otp")
        data = {
            "code": "abcdef",
        }
        response = self.client.post(
            path=path,
            data=data,
        )

        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_with_invalid_phone(self):
        path = reverse("account:api:register")
        response = self.client.post(
            path=path,
            data=self.invalid_phone,
        )

        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_with_exists_phone(self):
        path = reverse("account:api:register")
        response = self.client.post(
            path=path,
            data=self.user_phone,
        )

        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_register_with_new_phone(self):
        path = reverse("account:api:register")
        response = self.client.post(
            path=path,
            data=self.new_phone,
        )
        otp_code = {
            "code": json.loads(response.content).get("otp"),
        }

        path = reverse("account:api:verify-otp")
        response = self.client.post(
            path=path,
            data=otp_code,
        )
        content = json.loads(response.content)

        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertTrue(content["refresh"], content["access"])
        self.assertTrue(content["created"])

    def test_throttling_register_view(self):
        path = reverse("account:api:register")
        for _ in range(6):
            response = self.client.post(
                path=path,
                data=self.new_phone,
            )

        self.assertEquals(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)

    def test_throttling_verify_otp_view(self):
        path = reverse("account:api:verify-otp")
        otp_code = {
            "code": "123456",
        }
        for _ in range(9):
            response = self.client.post(
                path=path,
                data=otp_code,
            )

        self.assertEquals(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)

    def test_create_two_step_password_with_simple_password(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.refresh_for_user.access_token}"
        )
        path = reverse("account:api:create-two-step-password")

        data = {
            "password": "test",
            "confirm_password": "test",
        }
        response = self.client.post(
            path=path,
            data=data,
        )

        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_and_change_two_step_password_with_user(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.refresh_for_user.access_token}"
        )
        path = reverse("account:api:create-two-step-password")

        data = {
            "password": "djangorestframework",
            "confirm_password": "djangorestframework",
        }
        response = self.client.post(
            path=path,
            data=data,
        )
        self.assertEquals(response.status_code, status.HTTP_200_OK)

        path = reverse("account:api:change-two-step-password")
        change_password = {
            "old_password": "djangorestframework",
            "password": "pythonanddjango",
            "confirm_password": "pythonanddjango",
        }
        response = self.client.post(
            path=path,
            data=change_password,
        )
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_validation_create_two_step_password(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.refresh_for_user.access_token}"
        )
        path = reverse("account:api:create-two-step-password")

        data = {
            "password": "1234",
            "confirm_password": "4321",
        }
        response = self.client.post(
            path=path,
            data=data,
        )

        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_account(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.refresh_for_user.access_token}"
        )
        path = reverse("account:api:delete-account")

        response = self.client.delete(
            path=path,
        )

        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_account_with_two_step_password(self):
        self.user.set_password("test")
        self.user.two_step_password = True
        self.user.save(update_fields=["password", "two_step_password"])

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.refresh_for_user.access_token}"
        )
        path = reverse("account:api:delete-account")

        response = self.client.delete(
            path=path,
        )
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

        wrong_data = {
            "password": "1234",
            "confirm_password": "1234",
        }
        response = self.client.delete(
            path=path,
            data=wrong_data,
        )
        self.assertEquals(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)

        data = {
            "password": "test",
            "confirm_password": "test",
        }
        response = self.client.delete(
            path=path,
            data=data,
        )
        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)
