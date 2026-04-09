# 🩸 Blood Management System

A full-stack Blood Management System built with **Django**, **Django REST Framework**, and **Django Templates** (Bootstrap 5). This system manages blood donors, donations, blood banks, and blood requests with role-based access for Admins and Donors.

---

## 📋 Features

### 👤 Authentication
- User Registration (Donor role by default)
- Login / Logout
- Session-based auth for templates + JWT for API

### 🛡️ Admin Features
- Admin Dashboard with live statistics (donors, donations, requests, inventory)
- Manage Blood Banks (add / deactivate)
- Review & Approve / Reject blood donations
- Review & Approve / Reject / Fulfill blood requests
- View all donors, donations, and requests with filters

### 🩸 Donor Features
- Personal Dashboard with donation history and blood availability
- Register a blood donation at any blood bank
- Submit a blood request (for self or family)
- Update profile (blood group, city, photo, availability)
- View donation & request status tracking
- Search donors by blood group and city

### 🔌 REST API (DRF)
Full API available at:
| Endpoint | Methods | Description |
|---|---|---|
| `/accounts/api/register/` | POST | Register new user |
| `/accounts/api/login/` | POST | Login, returns JWT tokens |
| `/accounts/api/logout/` | POST | Invalidate refresh token |
| `/accounts/api/me/` | GET, PUT | Current user profile |
| `/accounts/api/donors/` | GET | List donors (filterable) |
| `/api/blood-banks/` | GET, POST | List / create blood banks |
| `/api/inventory/` | GET | Blood inventory |
| `/api/donations/` | GET, POST | List / create donations |
| `/api/donations/<id>/action/` | POST | Approve or reject donation |
| `/api/requests/` | GET, POST | List / create blood requests |
| `/api/requests/<id>/action/` | POST | Approve/reject/fulfill request |
| `/api/statistics/` | GET | Admin statistics |
| `/api/donors/search/` | GET | Search donors by group/city |
| `/api/token/refresh/` | POST | Refresh JWT access token |

---

## 🚀 Setup & Installation

### Prerequisites
- Python 3.10+
- pip

### Step 1 — Clone the repository
```bash
git clone https://github.com/yourusername/blood-management-system.git
cd blood-management-system
```

### Step 2 — Create and activate a virtual environment
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux / macOS
source venv/bin/activate
```

### Step 3 — Install dependencies
```bash
pip install -r requirements.txt
```

### Step 4 — Apply migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 5 — Create a superuser (Admin)
```bash
python manage.py createsuperuser
```

Or use the included seed script to create demo data:
```bash
python manage.py shell < seed_data.py
```

### Step 6 — Run the development server
```bash
python manage.py runserver
```
Visit: **http://127.0.0.1:8000/**

---

## 🔐 Demo Credentials

| Role  | Username       | Password     |
|-------|----------------|--------------|
| Admin | `admin`        | `Admin@1234` |
| Donor | `rahul_donor`  | `Donor@1234` |
| Donor | `fatima_d`     | `Donor@1234` |

---

## 🏗️ Project Structure

```
blood_management/
├── accounts/               # User auth, custom user model, donor profile
│   ├── models.py           # CustomUser, DonorProfile
│   ├── serializers.py      # DRF serializers
│   ├── views.py            # Auth views (template + API)
│   └── urls.py
├── blood/                  # Core blood management logic
│   ├── models.py           # BloodBank, BloodInventory, BloodDonation, BloodRequest
│   ├── serializers.py
│   ├── views.py            # Dashboard, donations, requests, banks
│   └── urls.py
├── templates/              # Django HTML templates (Bootstrap 5)
│   ├── base.html           # Base layout with sidebar navigation
│   ├── home.html
│   ├── accounts/
│   │   ├── login.html
│   │   ├── register.html
│   │   └── profile.html
│   └── blood/
│       ├── admin_dashboard.html
│       ├── donor_dashboard.html
│       ├── donation_form.html
│       ├── donation_list.html
│       ├── approve_donation.html
│       ├── request_form.html
│       ├── request_list.html
│       ├── approve_request.html
│       ├── donor_list.html
│       ├── bank_list.html
│       └── bank_manage.html
├── blood_management/       # Django project settings
│   ├── settings.py
│   └── urls.py
├── requirements.txt
├── manage.py
└── README.md
```

---

## 🌐 Deployment (Render / Railway)

### For Render:
1. Add `whitenoise` to middleware in `settings.py`:
```python
MIDDLEWARE = [
    ...
    'whitenoise.middleware.WhiteNoiseMiddleware',
    ...
]
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
```
2. Set environment variables: `SECRET_KEY`, `DEBUG=False`, `ALLOWED_HOSTS`
3. Build command: `pip install -r requirements.txt && python manage.py migrate && python manage.py collectstatic --noinput`
4. Start command: `gunicorn blood_management.wsgi`

### For PythonAnywhere:
1. Upload project files
2. Set up a virtual environment
3. Configure WSGI file to point to `blood_management.wsgi`
4. Run `python manage.py collectstatic`

---

## 🗃️ Database Models

### CustomUser
Extends Django's AbstractUser. Adds `role` (admin/donor) and `phone`.

### DonorProfile
Links 1-to-1 with CustomUser. Stores blood group, city, availability, donation count, photo.

### BloodBank
Name, location, city, contact info, active status.

### BloodInventory
Tracks units per blood group per blood bank.

### BloodDonation
Links donor → blood bank. Status: pending / approved / rejected.

### BloodRequest
Links requester → patient info, hospital, urgency. Status: pending / approved / rejected / fulfilled.

---

## ✅ Validation

- **Backend**: Unique username/email check, password match, minimum length, blood group validation via choices
- **Frontend**: Required field enforcement via HTML5 validation, blood group select (only valid choices shown), date pickers

---

## 📦 Tech Stack

| Layer    | Technology                             |
|----------|----------------------------------------|
| Backend  | Django 4.2, Django REST Framework 3.14 |
| Auth     | Session auth + JWT (SimpleJWT)         |
| Frontend | Django Templates + Bootstrap 5         |
| Icons    | Font Awesome 6                         |
| Database | SQLite (dev) / PostgreSQL (production) |
| Deploy   | Gunicorn + Whitenoise                  |

---

## 🎯 Bonus Features Implemented

- ✅ Blood request status tracking (pending → approved → fulfilled)
- ✅ Profile photo upload for donors
- ✅ Search donors by blood group AND location (city/area)
- ✅ Full REST API with JWT authentication
- ✅ Admin statistics endpoint with blood-group breakdown
- ✅ Responsive design (Bootstrap 5)
- ✅ Role-based access control (admin vs donor views)
- ✅ Django admin panel integration

---

*Built as the final project for the Django + DRF + React course.*
