# MySQL Setup Guide — Blood Management System

## Step 1 — Install MySQL driver

```bash
# Option A: mysqlclient (recommended, C-based, faster)
pip install mysqlclient

# Option B: PyMySQL (pure Python, no C compiler needed)
pip install PyMySQL
```

If using PyMySQL, add these two lines at the top of `manage.py` and `blood_management/wsgi.py`:

```python
import pymysql
pymysql.install_as_MySQLdb()
```

---

## Step 2 — Create the database

```sql
CREATE DATABASE blood_db_v2
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

CREATE USER 'blood_user'@'localhost' IDENTIFIED BY 'StrongPass@123';
GRANT ALL PRIVILEGES ON blood_db.* TO 'blood_user'@'localhost';
FLUSH PRIVILEGES;
```

---

## Step 3 — Import the dataset

**For Linux/Mac:**
```bash
mysql -u blood_user -p blood_db < blood_management_mysql.sql
```

**For Windows (PowerShell):**
```powershell
# Option 1: Use Command Prompt
cmd /c "mysql -u blood_user -p blood_db < blood_management_mysql.sql"

# Option 2: Use Get-Content pipe
Get-Content blood_management_mysql.sql | mysql -u blood_user -p blood_db
```

**Note:** If MySQL is not in your PATH, find the full path to mysql.exe in your MySQL Server installation directory.

---

## Step 4 — Update settings.py

In `blood_management/settings.py`, **replace** the `DATABASES` block:

```python
DATABASES = {
    'default': {
        'ENGINE':   'django.db.backends.mysql',
        'NAME':     'blood_db',
        'USER':     'blood_user',
        'PASSWORD': 'StrongPass@123',
        'HOST':     'localhost',
        'PORT':     '3306',
        'OPTIONS': {
            'charset': 'utf8mb4',
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}
```

---

## Step 5 — Run fake initial migration (tables already exist from SQL import)

```bash
python manage.py migrate --fake-initial
```

Or if starting fresh (no SQL import):

```bash
python manage.py migrate
```

---

## Step 6 — Run the server

```bash
python manage.py runserver
```

---

## Demo Login Credentials

| Role  | Username       | Password     |
|-------|----------------|--------------|
| Admin | `admin`        | `Admin@1234` |
| Donor | `rahul_donor`  | `Donor@1234` |
| Donor | `fatima_d`     | `Donor@1234` |
| Donor | `sohel_d`      | `Donor@1234` |
| Donor | `nasreen_d`    | `Donor@1234` |
| Donor | `karim_d`      | `Donor@1234` |

---

## Database Schema Overview

```
accounts_customuser          — All users (admin + donors)
accounts_donorprofile        — Extended donor info (blood group, city, etc.)
blood_bloodbank              — Registered blood banks
blood_bloodinventory         — Units per blood group per bank
blood_blooddonation          — Donation records with approval status
blood_bloodrequest           — Blood requests with urgency & status
```

---

## Troubleshooting

| Error | Fix |
|---|---|
| `django.db.utils.OperationalError: (1045)` | Wrong MySQL username/password in settings |
| `No module named 'MySQLdb'` | Run `pip install mysqlclient` |
| `django_content_type already exists` | Use `--fake-initial` flag on migrate |
| Emoji/encoding error | Ensure DB charset is `utf8mb4` |
| `MariaDB Strict Mode is not set` (warning) | Add `'init_command': "SET sql_mode='STRICT_TRANS_TABLES'"` to OPTIONS in DATABASES |
| `Tablespace for table exists` (error 1813) | Run the `fix_db.py` script provided to reset the database |
| `mysql: command not found` (Windows) | Add MySQL bin directory to PATH or use full path to mysql.exe |
