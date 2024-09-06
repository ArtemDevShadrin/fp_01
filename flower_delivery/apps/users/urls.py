from django.urls import path
from .views import LoginView, RegisterView, ProfileView, LogoutView, ProfileEditView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("edit/", ProfileEditView.as_view(), name="profile_edit"),
]
