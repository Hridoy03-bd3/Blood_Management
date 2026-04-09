#!/usr/bin/env python
"""Create admin user with credentials: admin / Admin@1234"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blood_management.settings')
django.setup()

from accounts.models import CustomUser

# Delete existing admin if present
CustomUser.objects.filter(username='admin').delete()
print("✓ Deleted existing admin user (if any)")

# Create new admin user
admin_user = CustomUser.objects.create_superuser(
    username='admin',
    email='admin@example.com',
    password='Admin@1234',
    is_staff=True,
    is_superuser=True,
)
print(f"✓ Admin user created successfully")
print(f"  Username: {admin_user.username}")
print(f"  Email: {admin_user.email}")
print(f"  Password: Admin@1234")
print("\n✅ Admin login credentials are ready!")
