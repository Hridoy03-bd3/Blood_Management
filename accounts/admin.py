from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, DonorProfile, BloodBankProfile

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'role', 'is_active']
    list_filter = ['role', 'is_active']
    fieldsets = UserAdmin.fieldsets + (('Role & Contact', {'fields': ('role', 'phone')}),)

@admin.register(DonorProfile)
class DonorProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'blood_group', 'city', 'is_available', 'total_donations']
    list_filter = ['blood_group', 'is_available']
    search_fields = ['user__username', 'user__first_name', 'city']

@admin.register(BloodBankProfile)
class BloodBankProfileAdmin(admin.ModelAdmin):
    list_display = ['bank_name', 'city', 'registration_number', 'is_verified', 'is_active']
    list_filter = ['is_verified', 'is_active', 'city']
    search_fields = ['bank_name', 'registration_number', 'city']
    readonly_fields = ['created_at', 'updated_at']
