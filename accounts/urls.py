from django.urls import path
from .views import HomeView, LoginView, MagicNumberView

app_name = "accounts"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("login/", LoginView.as_view(), name="login"),
    path("validate/", MagicNumberView.as_view(), name="validate"),
]
