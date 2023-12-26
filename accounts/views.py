from django.core.mail import send_mail
from rest_framework.views import APIView
from rest_framework.serializers import Serializer, EmailField, CharField
from rest_framework.parsers import JSONParser
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from rest_framework.authtoken.models import Token

from .models import User
from magiccode.models import MagicCode
import django_chat_tutorial.settings as settings

code_length = settings.MAGIC_CODE_LENGTH
from_email = settings.EMAIL_HOST_USER


class HomeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request: Request):
        return Response({"username": request.user.username})


class LoginSerializer(Serializer):
    email = EmailField(required=True)


class LoginView(APIView):
    serializer_class = LoginSerializer
    parser_classes = [JSONParser]

    def post(self, request: Request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            MagicCode.objects.filter(email=email).delete()
            code = MagicCode.create(email).code
            send_mail(
                subject="Magic number Test",
                message=f"Your magic number is {code}",
                from_email=from_email,
                recipient_list=[email],
            )
            return Response()
        return Response(serializer.errors, status=400)


class MagicNumberSerializer(Serializer):
    email = EmailField(required=True)
    code = CharField(min_length=code_length, max_length=code_length, required=True)

    def validate(self, attrs):
        email, code = attrs["email"], attrs["code"]
        if MagicCode.is_valid(email, code):
            return attrs
        raise ValidationError("認証情報が間違っています")


class MagicNumberView(APIView):
    serializer_class = MagicNumberSerializer
    parser_classes = [JSONParser]

    def post(self, request: Request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                user = User.objects.create_user(email)
            return Response({"token": Token.objects.get_or_create(user=user)[0].key})
        return Response(serializer.errors, status=400)
