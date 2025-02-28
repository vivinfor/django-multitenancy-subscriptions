from django.urls import path
from .views import CustomLoginView, CustomLogoutView, UserProfileView

app_name = 'authentication'

urlpatterns = [
    # Autenticação
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", CustomLogoutView.as_view(), name="logout"),
    path("profile/", UserProfileView.as_view(), name="profile"),
]
