from django.test import TestCase
from django.utils import timezone

import datetime

from .models import MagicCode
import django_chat_tutorial.settings as settings

max_send_count = settings.MAX_MAGIC_CODE_SEND_TIMES
expire_minutes = settings.MAGIC_CODE_EXPIRE_MINUTES


class MagicCodeTest(TestCase):
    email = "text@exmaple.com"

    def test_valid(self):
        code = MagicCode.create(email=self.email).code
        invalid_code = code == "123456" and "654321" or "123456"

        for _ in range(max_send_count - 1):
            self.assertFalse(MagicCode.is_valid(email=self.email, code=invalid_code))

        self.assertTrue(MagicCode.is_valid(email=self.email, code=code))

    def test_invalid(self):
        code = MagicCode.create(email=self.email).code
        invalid_code = code == "123456" and "654321" or "123456"

        for _ in range(max_send_count):
            self.assertEqual(MagicCode.objects.count(), 1)
            self.assertFalse(MagicCode.is_valid(email=self.email, code=invalid_code))

        self.assertEqual(MagicCode.objects.count(), 0)
        self.assertFalse(MagicCode.is_valid(email=self.email, code=code))

    def test_many_valid(self):
        code = MagicCode.create(
            email=self.email,
            expire_time=timezone.now() - datetime.timedelta(minutes=expire_minutes + 1),
        ).code

        self.assertFalse(MagicCode.is_valid(email=self.email, code=code))
        self.assertEqual(MagicCode.objects.count(), 0)
