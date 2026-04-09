#!/usr/bin/env python
"""Set admin role for the admin user"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blood_management.settings')
django.setup()

from accounts.models import CustomUser

# Update admin user with admin role
admin = CustomUser.objects.get(username='admin')
admin.role = 'admin'
admin.is_staff = True
admin.is_superuser = True
admin.save()

print(f"✓ Admin user updated successfully")
print(f"  Username: {admin.username}")
print(f"  Role: {admin.role}")
print(f"  Is Staff: {admin.is_staff}")
print(f"  Is Superuser: {admin.is_superuser}")
print("\n✅ Admin now has full admin access!")
