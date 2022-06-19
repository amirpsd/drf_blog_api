from django.urls import reverse, resolve
from django.test import SimpleTestCase

from account.api import views

# Create your tests here.


class UrlsTest(SimpleTestCase):
    
    def test_app_name(self):
        self.assertEquals(resolve("/account/api/").app_name, "account:api")

    def test_users_list(self):
        path = reverse("account:api:users-list")
        self.assertEquals(resolve(path).func.view_class, views.UsersList)
        self.assertNotEquals(
            resolve(path).func.view_class, views.UsersDetailUpdateDelete
        )

    def test_user_profile(self):
        path = reverse("account:api:profile")
        self.assertEquals(resolve(path).func.view_class, views.UserProfile)
        self.assertNotEquals(resolve(path).func.view_class, views.UsersList)

    def test_login(self):
        path = reverse("account:api:login")
        self.assertEquals(resolve(path).func.view_class, views.Login)
        self.assertNotEquals(resolve(path).func.view_class, views.Register)

    def test_register(self):
        path = reverse("account:api:register")
        self.assertEquals(resolve(path).func.view_class, views.Register)
        self.assertNotEquals(resolve(path).func.view_class, views.Login)

    def test_verify_otp(self):
        path = reverse("account:api:verify-otp")
        self.assertEquals(resolve(path).func.view_class, views.VerifyOtp)
        self.assertNotEquals(resolve(path).func.view_class, views.Login)

    def test_change_two_step_password(self):
        path = reverse("account:api:change-two-step-password")
        self.assertEquals(resolve(path).func.view_class, views.ChangeTwoStepPassword)
        self.assertNotEquals(resolve(path).func.view_class, views.CreateTwoStepPassword)

    def test_create_two_step_password(self):
        path = reverse("account:api:create-two-step-password")
        self.assertEquals(resolve(path).func.view_class, views.CreateTwoStepPassword)
        self.assertNotEquals(resolve(path).func.view_class, views.ChangeTwoStepPassword)

    def test_delete_account(self):
        path = reverse("account:api:delete-account")
        self.assertEquals(resolve(path).func.view_class, views.DeleteAccount)
        self.assertNotEquals(resolve(path).func.view_class, views.Register)

    def test_users_detail_update_delete(self):
        path = reverse("account:api:users-detail", args=[1])
        self.assertEquals(resolve(path).func.view_class, views.UsersDetailUpdateDelete)
        self.assertNotEquals(resolve(path).func.view_class, views.UsersList)
