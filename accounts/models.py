from django.contrib.auth.models import AbstractUser
from django.db import models

BLOOD_GROUPS = [
    ('A+', 'A+'), ('A-', 'A-'),
    ('B+', 'B+'), ('B-', 'B-'),
    ('AB+', 'AB+'), ('AB-', 'AB-'),
    ('O+', 'O+'), ('O-', 'O-'),
]

class CustomUser(AbstractUser):
    ROLE_CHOICES = [('admin', 'Admin'), ('donor', 'Donor'), ('blood_bank', 'Blood Bank')]
    role = models.CharField(max_length=15, choices=ROLE_CHOICES, default='donor')
    phone = models.CharField(max_length=15, blank=True)
    
    def is_admin_user(self):
        return self.role == 'admin'
    
    def is_donor(self):
        return self.role == 'donor'
    
    def is_blood_bank(self):
        return self.role == 'blood_bank'


class DonorProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='donor_profile')
    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUPS)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=[('male','Male'),('female','Female'),('other','Other')], blank=True)
    city = models.CharField(max_length=100, blank=True)
    area = models.CharField(max_length=100, blank=True)
    address = models.TextField(blank=True)
    is_available = models.BooleanField(default=True)
    last_donation_date = models.DateField(null=True, blank=True)
    profile_photo = models.ImageField(upload_to='donor_photos/', null=True, blank=True)
    bio = models.TextField(blank=True)
    total_donations = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.blood_group}"

    class Meta:
        ordering = ['-created_at']


class BloodBankProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='blood_bank_profile')
    bank_name = models.CharField(max_length=200)
    registration_number = models.CharField(max_length=50, unique=True)
    contact_number = models.CharField(max_length=15)
    email = models.EmailField()
    location = models.CharField(max_length=300)
    city = models.CharField(max_length=100)
    address = models.TextField()
    license_number = models.CharField(max_length=100, blank=True)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.bank_name} - {self.city}"

    class Meta:
        ordering = ['-created_at']
