from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import CustomUser, DonorProfile, BloodBankProfile

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    confirm_password = serializers.CharField(write_only=True)
    blood_group = serializers.CharField(write_only=True, required=False)
    phone = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'password', 'confirm_password', 'phone', 'blood_group']

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match.")
        if CustomUser.objects.filter(email=data.get('email', '')).exists():
            raise serializers.ValidationError("Email already registered.")
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        blood_group = validated_data.pop('blood_group', 'A+')
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            password=validated_data['password'],
            phone=validated_data.get('phone', ''),
            role='donor',
        )
        DonorProfile.objects.create(user=user, blood_group=blood_group)
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(username=data['username'], password=data['password'])
        if not user:
            raise serializers.ValidationError("Invalid credentials.")
        if not user.is_active:
            raise serializers.ValidationError("Account is disabled.")
        data['user'] = user
        return data


class DonorProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    full_name = serializers.SerializerMethodField()
    phone = serializers.CharField(source='user.phone', read_only=True)

    class Meta:
        model = DonorProfile
        fields = ['id', 'username', 'email', 'full_name', 'phone', 'blood_group',
                  'date_of_birth', 'gender', 'city', 'area', 'address',
                  'is_available', 'last_donation_date', 'profile_photo',
                  'bio', 'total_donations', 'created_at']

    def get_full_name(self, obj):
        return obj.user.get_full_name() or obj.user.username


class UserSerializer(serializers.ModelSerializer):
    donor_profile = DonorProfileSerializer(read_only=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'role', 'phone', 'donor_profile']
        read_only_fields = ['role']


class BloodBankProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = BloodBankProfile
        fields = ['id', 'bank_name', 'registration_number', 'contact_number', 'email', 'location', 'city', 'address', 'license_number', 'is_verified', 'is_active']
        read_only_fields = ['is_verified']


class BloodBankRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    confirm_password = serializers.CharField(write_only=True)
    bank_name = serializers.CharField()
    registration_number = serializers.CharField()
    contact_number = serializers.CharField()
    location = serializers.CharField()
    city = serializers.CharField()
    address = serializers.CharField()

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'confirm_password', 'phone', 'bank_name', 'registration_number', 'contact_number', 'location', 'city', 'address']

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match.")
        if CustomUser.objects.filter(email=data.get('email', '')).exists():
            raise serializers.ValidationError("Email already registered.")
        if BloodBankProfile.objects.filter(registration_number=data.get('registration_number', '')).exists():
            raise serializers.ValidationError("Blood Bank with this registration number already exists.")
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        bank_name = validated_data.pop('bank_name')
        registration_number = validated_data.pop('registration_number')
        contact_number = validated_data.pop('contact_number')
        location = validated_data.pop('location')
        city = validated_data.pop('city')
        address = validated_data.pop('address')

        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            phone=validated_data.get('phone', ''),
            role='blood_bank',
        )
        
        BloodBankProfile.objects.create(
            user=user,
            bank_name=bank_name,
            registration_number=registration_number,
            contact_number=contact_number,
            email=validated_data['email'],
            location=location,
            city=city,
            address=address,
        )
        return user
