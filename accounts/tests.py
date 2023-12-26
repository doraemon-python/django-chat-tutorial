from rest_framework.test import APITestCase
from django.urls import reverse
from django.core import mail

from magiccode.models import MagicCode
from django_chat_tutorial.settings import MAX_MAGIC_CODE_SEND_TIMES as max_send_times

email = "text@example.com"


class LoginTestCase(APITestCase):
    path = reverse("accounts:login")

    def test_create_user(self):
        res = self.client.post(self.path, {"email": email}, format="json")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(MagicCode.objects.count(), 1)
        self.assertEqual(len(mail.outbox), 1)


class ValidateTestCase(APITestCase):
    path = reverse("accounts:validate")

    def setUp(self):
        self.code = MagicCode.create(email).code

    def test_validate(self):
        res = self.client.post(
            self.path, {"email": email, "code": self.code}, format="json"
        )
        self.assertEqual(res.status_code, 200)

    def test_invalidate(self):
        code = self.code == "000000" and "111111" or "000000"
        for _ in range(max_send_times):
            res = self.client.post(
                self.path, {"email": email, "code": code}, format="json"
            )
            self.assertEqual(res.status_code, 400)

        # valid code is used up
        res = self.client.post(
            self.path, {"email": email, "code": self.code}, format="json"
        )
        self.assertEqual(res.status_code, 400)


class AuthTestCase(APITestCase):
    def setUp(self):
        self.code = MagicCode.create(email).code
        self.client.post(
            reverse("accounts:validate"),
            {"email": email, "code": self.code},
            format="json",
        )

    def test_auth(self):
        path = reverse("accounts:home")
        res = self.client.get(path)
        self.assertEqual(res.status_code, 200)
