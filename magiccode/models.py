from django.db import models
from django.utils import timezone
from django.utils.crypto import get_random_string
from rest_framework.exceptions import ValidationError

import datetime

import django_chat_tutorial.settings as settings

code_length = settings.MAGIC_CODE_LENGTH
expire_minutes = settings.MAGIC_CODE_EXPIRE_MINUTES
max_send_count = settings.MAX_MAGIC_CODE_SEND_TIMES


def generate_magic_code():
    return get_random_string(length=code_length, allowed_chars="0123456789")


class MagicCode(models.Model):
    code = models.CharField(max_length=code_length, unique=True, editable=False)
    email = models.EmailField(editable=False, unique=True)
    expire_time = models.DateTimeField(
        default=timezone.now() + datetime.timedelta(minutes=expire_minutes),
        editable=False,
    )
    send_count = models.PositiveSmallIntegerField(default=0)

    @classmethod
    def create(cls, email: str, **kwargs):
        while True:
            code = generate_magic_code()
            if not cls.objects.filter(code=code).exists():
                break
        return cls.objects.create(email=email, code=code, **kwargs)

    @classmethod
    def is_valid(cls, email, code):
        try:
            magic_code = cls.objects.get(email=email)
        except cls.DoesNotExist:
            raise ValidationError("このメールアドレスは登録されていません")

        if magic_code.expire_time < timezone.now():
            raise ValidationError("認証コードの有効期限が切れています")

        magic_code.send_count += 1

        if magic_code.send_count > max_send_count:
            raise ValidationError("認証コードの送信回数が上限に達しました")

        if magic_code.code != code:
            if magic_code.send_count >= max_send_count:
                magic_code.delete()
            else:
                magic_code.save()

            raise ValidationError("認証コードが間違っています")

        magic_code.delete()
        return True
