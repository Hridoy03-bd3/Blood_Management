from django.urls import path
from . import views

urlpatterns = [
    path('register-choice/', views.registration_choice_view, name='registration_choice'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    # Blood Bank Registration
    path('blood-bank/register/', views.blood_bank_register_view, name='blood_bank_register'),
    # API
    path('api/register/', views.RegisterAPIView.as_view(), name='api_register'),
    path('api/login/', views.LoginAPIView.as_view(), name='api_login'),
    path('api/logout/', views.LogoutAPIView.as_view(), name='api_logout'),
    path('api/me/', views.UserProfileAPIView.as_view(), name='api_me'),
    path('api/donors/', views.DonorListAPIView.as_view(), name='api_donors'),
    path('api/donor/profile/', views.DonorProfileUpdateAPIView.as_view(), name='api_donor_profile'),
    # Blood Bank API
    path('api/blood-bank/register/', views.BloodBankRegisterAPIView.as_view(), name='api_blood_bank_register'),
    path('api/blood-bank/profile/', views.BloodBankProfileAPIView.as_view(), name='api_blood_bank_profile'),
]
