from rest_framework import serializers
from .models import BloodBank, BloodInventory, BloodDonation, BloodRequest
from accounts.serializers import DonorProfileSerializer

class BloodInventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BloodInventory
        fields = '__all__'

class BloodBankSerializer(serializers.ModelSerializer):
    inventory = BloodInventorySerializer(many=True, read_only=True)

    class Meta:
        model = BloodBank
        fields = '__all__'

class BloodDonationSerializer(serializers.ModelSerializer):
    donor_name = serializers.SerializerMethodField()
    blood_bank_name = serializers.SerializerMethodField()

    class Meta:
        model = BloodDonation
        fields = '__all__'
        read_only_fields = ['donor', 'status', 'admin_remarks', 'created_at', 'updated_at']

    def get_donor_name(self, obj):
        return obj.donor.get_full_name() or obj.donor.username

    def get_blood_bank_name(self, obj):
        return obj.blood_bank.name if obj.blood_bank else ''


class BloodRequestSerializer(serializers.ModelSerializer):
    requester_name = serializers.SerializerMethodField()

    class Meta:
        model = BloodRequest
        fields = '__all__'
        read_only_fields = ['requester', 'status', 'admin_remarks', 'created_at', 'updated_at']

    def get_requester_name(self, obj):
        return obj.requester.get_full_name() or obj.requester.username
