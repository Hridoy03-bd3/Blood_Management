from django.contrib import admin
from .models import BloodBank, BloodInventory, BloodDonation, BloodRequest

@admin.register(BloodBank)
class BloodBankAdmin(admin.ModelAdmin):
    list_display = ['name', 'city', 'contact_number', 'is_active']

@admin.register(BloodInventory)
class BloodInventoryAdmin(admin.ModelAdmin):
    list_display = ['blood_bank', 'blood_group', 'units_available']

@admin.register(BloodDonation)
class BloodDonationAdmin(admin.ModelAdmin):
    list_display = ['donor', 'blood_group', 'blood_bank', 'donation_date', 'status']
    list_filter = ['status', 'blood_group']
    actions_on_bottom = True

@admin.register(BloodRequest)
class BloodRequestAdmin(admin.ModelAdmin):
    list_display = ['patient_name', 'blood_group', 'hospital_name', 'urgency', 'status']
    list_filter = ['status', 'urgency', 'blood_group']
