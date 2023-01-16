from django.urls import path
from account import views

urlpatterns = [
    # Login & Logout Urls
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    # Register Urls
    path('register/', views.RegisterView.as_view(), name='register'),
    path('register/check_otp/', views.CheckOtpView.as_view(), name='check_otp'),
    # Edit Profile Url
    path('profile/', views.EditProfileView.as_view(), name='edit_profile'),
    # Forgot Password Urls
    path('forget_password/', views.ForgetPasswordView.as_view(), name="forget_pass"),
    path('forget_password/check_phone_number/', views.ForgotPasswordCheckView.as_view(), name="forget_pass_check"),
    path('forget_password/done_validation', views.ForgetPasswordDoneView.as_view(), name="forget_pass_done"),
    # Change Password Urls
    path('change_password/', views.ChangePasswordView.as_view(), name="change_pass"),
    path('change_password/complete_change', views.ChangePasswordDoneView.as_view(), name="change_pass_done"),
]
