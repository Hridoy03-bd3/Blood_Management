from django.urls import path
from . import views

urlpatterns = [
    # Template views
    path('', views.home_view, name='home'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('donations/', views.donation_list_view, name='donation_list'),
    path('donations/new/', views.donation_create_view, name='donation_create'),
    path('donations/<int:pk>/approve/', views.approve_donation_view, name='approve_donation'),
    path('requests/', views.request_list_view, name='request_list'),
    path('requests/new/', views.request_create_view, name='request_create'),
    path('requests/<int:pk>/approve/', views.approve_request_view, name='approve_request'),
    path('blood-banks/', views.blood_bank_list_view, name='blood_bank_list'),
    path('blood-banks/manage/', views.blood_bank_manage_view, name='blood_bank_manage'),
    path('donors/', views.donor_list_view, name='donor_list'),

    # Admin User Management
    path('admin/users/', views.admin_user_management_view, name='admin_user_management'),
    path('admin/users/<int:pk>/', views.admin_user_detail_view, name='admin_user_detail'),
    path('admin/users/<int:pk>/delete/', views.admin_delete_user_view, name='admin_delete_user'),
    path('admin/users/<int:pk>/toggle/', views.admin_toggle_user_view, name='admin_toggle_user'),
    path('admin/users/<int:pk>/promote/', views.admin_promote_user_view, name='admin_promote_user'),

    # API
    path('api/blood-banks/', views.BloodBankListCreateAPIView.as_view(), name='api_blood_banks'),
    path('api/blood-banks/<int:pk>/', views.BloodBankDetailAPIView.as_view(), name='api_blood_bank_detail'),
    path('api/inventory/', views.BloodInventoryAPIView.as_view(), name='api_inventory'),
    path('api/donations/', views.BloodDonationListCreateAPIView.as_view(), name='api_donations'),
    path('api/donations/<int:pk>/', views.BloodDonationDetailAPIView.as_view(), name='api_donation_detail'),
    path('api/donations/<int:pk>/action/', views.ApproveDonationAPIView.as_view(), name='api_approve_donation'),
    path('api/requests/', views.BloodRequestListCreateAPIView.as_view(), name='api_requests'),
    path('api/requests/<int:pk>/', views.BloodRequestDetailAPIView.as_view(), name='api_request_detail'),
    path('api/requests/<int:pk>/action/', views.ApproveRequestAPIView.as_view(), name='api_approve_request'),
    path('api/statistics/', views.StatisticsAPIView.as_view(), name='api_statistics'),
    path('api/donors/search/', views.DonorSearchAPIView.as_view(), name='api_donor_search'),
]
