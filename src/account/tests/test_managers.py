from django.contrib.auth import get_user_model
from django.test import TestCase


# Create your tests here.


class ManagersTest(TestCase):
    
    def test_create_user_Without_phone(self):
        with self.assertRaises(TypeError):
            user = get_user_model().objects.create_user(
                first_name="test-user-first-name",
                last_name="test-user-last-name",
            )

    def test_create_user(self):
        user = get_user_model().objects.create_user(
            phone="989101115874",
            first_name="test-user-first-name",
            last_name="test-user-last-name",
        )

        self.assertIsInstance(user, get_user_model())
        self.assertFalse(user.is_staff, user.is_superuser)

    def test_create_superuser(self):
        superuser = get_user_model().objects.create_superuser(
            phone="989101115876",
            first_name="test-superuser-first-name",
            last_name="test-superuser-last-name",
        )

        self.assertIsInstance(superuser, get_user_model())
        self.assertTrue(superuser.is_staff, superuser.is_superuser)

    def test_create_superuser_with_change_attribute(self):
        with self.assertRaises(ValueError):
            superuser = get_user_model().objects.create_superuser(
                phone="989101115876",
                first_name="test-superuser-first-name",
                last_name="test-superuser-last-name",
                is_staff=False,
            )
        with self.assertRaises(ValueError):
            superuser = get_user_model().objects.create_superuser(
                phone="989101115876",
                first_name="test-superuser-first-name",
                last_name="test-superuser-last-name",
                is_superuser=False,
            )
