from django.urls import path



from .views import (
    UsersList, UsersDetailUpdateDelete, UserProfile, 
    Login, Register, VerifyOtp,
    ChangeTwoStepPassword, CreateTwoStepPassword,LogoutView,AddressCreateView,AddressUpdateView
)
from .dokonUser import DokonLogin, DokonRegister
from savdo.views import cashback_user_update
from .QwerCodeLogin import DiveViews, GoustUserViews

app_name = "account"

urlpatterns = [
    path("list/", UsersList.as_view(), name="users-list"),
    path('logaut/',LogoutView.as_view(), name='auth_logout' ),
    path("profile/", UserProfile.as_view(), name="profile"),
    path("login/", Login.as_view(), name="login"),
    path("register/", Register.as_view(), name="register"),
    path("verify/", VerifyOtp.as_view(), name="verify-otp"),
    path('user-data-update/', cashback_user_update , name='user-data-update'),
    path("change-two-step-password/", ChangeTwoStepPassword.as_view(), name="change-two-step-password"),
    path("create-two-step-password/", CreateTwoStepPassword.as_view(), name="create-two-step-password"),
    path("users/<int:pk>/", UsersDetailUpdateDelete.as_view(), name="users-detail"),
    path('address/', AddressCreateView.as_view(), name='address-list'),
    path('address/<user>/', AddressUpdateView.as_view(), name='address-detail'),
    path('dokon-user-login/', DokonLogin.as_view(), name='dokon-user'),
    path('dokon-user-register/', DokonRegister.as_view(), name='dokon-register'),
    # mobile login 
    path('user-mobile-login/<str:uuid_token>/', GoustUserViews.as_view(), name='user-mobile-login'),
    path('devise-user/<int:pk>/', DiveViews.as_view(), name='devise-user'),
]