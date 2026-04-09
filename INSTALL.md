# 🩸 BloodLife — Complete A-to-Z Installation Guide

---

## 📋 Table of Contents
1. Prerequisites
2. MySQL Database Setup
3. Project Installation
4. Environment Configuration
5. Running the Server
6. Creating Admin User
7. API Reference
8. Troubleshooting

---

## 1. Prerequisites

### Required Software
| Software | Minimum Version | Check Command |
|----------|----------------|---------------|
| Python   | 3.10+          | `python --version` |
| MySQL    | 8.0+           | `mysql --version` |
| pip      | 23+            | `pip --version` |
| Git      | Any            | `git --version` |

### Install Python (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv python3-dev
```

### Install Python (Windows)
Download from https://python.org — check "Add to PATH"

### Install MySQL (Ubuntu/Debian)
```bash
sudo apt install mysql-server libmysqlclient-dev
sudo systemctl start mysql
sudo systemctl enable mysql
```

### Install MySQL (Windows)
Download MySQL Installer from https://dev.mysql.com/downloads/installer/

---

## 2. MySQL Database Setup

### Step 1: Log into MySQL
```bash
# Linux
sudo mysql -u root -p

# Windows
mysql -u root -p
```

### Step 2: Create the database and user
```sql
-- Create database
CREATE DATABASE blood_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Create dedicated user (recommended)
CREATE USER 'blooduser'@'localhost' IDENTIFIED BY 'StrongPassword123!';
GRANT ALL PRIVILEGES ON blood_db.* TO 'blooduser'@'localhost';
FLUSH PRIVILEGES;

-- Verify
SHOW DATABASES LIKE 'blood_db';
EXIT;
```

### Step 3: Import the SQL dump
```bash
mysql -u root -p blood_db < blood_management_mysql.sql
```

---

## 3. Project Installation

### Step 1: Extract the project
```bash
unzip blood_management_full.zip
cd blood_management
```

### Step 2: Create virtual environment
```bash
# Linux / macOS
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### Step 3: Install dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

> **Note:** If `mysqlclient` fails to install on Linux, run:
> ```bash
> sudo apt install default-libmysqlclient-dev build-essential pkg-config
> pip install mysqlclient
> ```
>
> On Windows, try PyMySQL instead:
> ```bash
> pip install PyMySQL
> ```
> Then add to `manage.py` top:
> ```python
> import pymysql
> pymysql.install_as_MySQLdb()
> ```

---

## 4. Environment Configuration

### Step 1: Create your `.env` file
```bash
cp .env.example .env
```

### Step 2: Edit `.env`
```ini
SECRET_KEY=django-insecure-REPLACE-WITH-RANDOM-50-CHARS
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# MySQL credentials
DB_NAME=blood_db
DB_USER=blooduser
DB_PASSWORD=StrongPassword123!
DB_HOST=localhost
DB_PORT=3306
```

> Generate a secure SECRET_KEY:
> ```bash
> python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
> ```

---

## 5. Database Migration

```bash
# Apply migrations
python manage.py migrate

# If the SQL was already imported and you get errors, use:
python manage.py migrate --fake-initial
```

### Collect static files
```bash
python manage.py collectstatic --noinput
```

---

## 6. Creating Admin User

```bash
python manage.py createsuperuser
```

You'll be prompted for:
- **Username:** admin
- **Email:** admin@example.com
- **Password:** (min 8 chars)

Then in the Django shell, set the role to 'admin':
```bash
python manage.py shell
```
```python
from accounts.models import CustomUser
u = CustomUser.objects.get(username='admin')
u.role = 'admin'
u.is_staff = True
u.is_superuser = True
u.save()
print("Done! Admin role set.")
exit()
```

---

## 7. Running the Development Server

```bash
python manage.py runserver
```

Visit: **http://127.0.0.1:8000/**

| URL | Description |
|-----|-------------|
| `/` | Home page |
| `/accounts/login/` | Login |
| `/accounts/register/` | Register |
| `/dashboard/` | Dashboard |
| `/admin/users/` | User Management (admin only) |
| `/donations/` | Donations list |
| `/requests/` | Blood requests |
| `/blood-banks/` | Blood banks |
| `/donors/` | Find donors |
| `/admin/` | Django admin panel |

---

## 8. All Models Overview

### `accounts` App
| Model | Description |
|-------|-------------|
| `CustomUser` | Extended user: `username, email, role (admin/donor), phone` |
| `DonorProfile` | Donor details: `blood_group, city, area, total_donations, last_donation_date, is_available, profile_photo` |

### `blood` App
| Model | Description |
|-------|-------------|
| `BloodBank` | `name, location, city, contact_number, email, is_active` |
| `BloodInventory` | `blood_bank (FK), blood_group, units_available` |
| `BloodDonation` | `donor (FK), blood_bank (FK), blood_group, units, donation_date, status (pending/approved/rejected)` |
| `BloodRequest` | `requester (FK), blood_group, patient_name, hospital_name, urgency (normal/urgent/critical), status` |

---

## 9. Admin Interface Routes

| Route | View | Access |
|-------|------|--------|
| `/admin/users/` | List + search all users | Admin |
| `/admin/users/<id>/` | View user details | Admin |
| `/admin/users/<id>/delete/` | Delete user | Admin |
| `/admin/users/<id>/toggle/` | Activate/Deactivate user | Admin |
| `/admin/users/<id>/promote/` | Promote to admin / demote to donor | Admin |

---

## 10. REST API Endpoints

### Authentication
```
POST /accounts/api/register/     — Register new user
POST /accounts/api/login/        — Login (returns JWT tokens)
POST /accounts/api/logout/       — Logout (blacklists token)
GET  /accounts/api/me/           — Get current user profile
```

### Blood Banks
```
GET  /api/blood-banks/           — List active blood banks
POST /api/blood-banks/           — Create bank (admin)
GET  /api/blood-banks/<id>/      — Bank detail
```

### Inventory
```
GET  /api/inventory/             — Blood inventory (filterable by blood_group)
```

### Donations
```
GET  /api/donations/             — List donations
POST /api/donations/             — Submit donation
POST /api/donations/<id>/action/ — Approve/reject (admin) {action, remarks}
```

### Blood Requests
```
GET  /api/requests/              — List requests
POST /api/requests/              — Submit request
POST /api/requests/<id>/action/  — Approve/reject/fulfill (admin)
```

### Statistics (Admin only)
```
GET  /api/statistics/            — Full system stats
```

### Donor Search
```
GET  /api/donors/search/?blood_group=A+&city=Dhaka
```

---

## 11. Troubleshooting

### ❌ `django.db.OperationalError: (1045, "Access denied")`
→ Wrong MySQL credentials. Check `.env` DB_USER and DB_PASSWORD.

### ❌ `No module named 'MySQLdb'`
→ Run: `pip install mysqlclient` or use PyMySQL fallback.

### ❌ `django.db.OperationalError: (1049, "Unknown database 'blood_db'")`
→ Create the database first in MySQL: `CREATE DATABASE blood_db;`

### ❌ `Static files not loading`
→ Run: `python manage.py collectstatic`

### ❌ Migrations conflict
→ Run: `python manage.py migrate --fake-initial`

### ❌ Admin panel not accessible
→ Ensure user has `role='admin'` AND `is_staff=True`. Use the shell commands above.

---

## 12. Production Deployment Checklist

```ini
# .env for production
DEBUG=False
SECRET_KEY=<very-long-random-key>
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
```

```bash
# Install gunicorn
pip install gunicorn

# Run with gunicorn
gunicorn blood_management.wsgi:application --bind 0.0.0.0:8000 --workers 4
```

Use Nginx as reverse proxy and serve static/media files directly.

---

*Built with Django 4.2 + MySQL + Bootstrap 5 + REST Framework*
