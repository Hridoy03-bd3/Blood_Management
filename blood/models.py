from django.db import models
from accounts.models import CustomUser, BLOOD_GROUPS

class BloodBank(models.Model):
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=300)
    city = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=15)
    email = models.EmailField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} - {self.city}"

    class Meta:
        ordering = ['name']


class BloodInventory(models.Model):
    blood_bank = models.ForeignKey(BloodBank, on_delete=models.CASCADE, related_name='inventory')
    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUPS)
    units_available = models.PositiveIntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.blood_bank.name} - {self.blood_group}: {self.units_available} units"

    class Meta:
        unique_together = ['blood_bank', 'blood_group']


class BloodDonation(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    donor = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='donations')
    blood_bank = models.ForeignKey(BloodBank, on_delete=models.SET_NULL, null=True, related_name='donations')
    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUPS)
    units = models.PositiveIntegerField(default=1)
    donation_date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    notes = models.TextField(blank=True)
    admin_remarks = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.donor.get_full_name()} - {self.blood_group} ({self.status})"

    class Meta:
        ordering = ['-created_at']


class BloodRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('fulfilled', 'Fulfilled'),
    ]
    URGENCY_CHOICES = [
        ('normal', 'Normal'),
        ('urgent', 'Urgent'),
        ('critical', 'Critical'),
    ]
    requester = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='blood_requests')
    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUPS)
    units_needed = models.PositiveIntegerField(default=1)
    patient_name = models.CharField(max_length=200)
    hospital_name = models.CharField(max_length=200)
    hospital_city = models.CharField(max_length=100, blank=True)
    contact_number = models.CharField(max_length=15)
    urgency = models.CharField(max_length=10, choices=URGENCY_CHOICES, default='normal')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    reason = models.TextField(blank=True)
    admin_remarks = models.TextField(blank=True)
    required_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.patient_name} - {self.blood_group} ({self.status})"

    class Meta:
        ordering = ['-created_at']
