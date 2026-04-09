#!/usr/bin/env python
"""Fix MySQL tablespace issue by dropping and recreating database"""

import MySQLdb
import sys

try:
    # Connect as root (no password, or update if needed)
    conn = MySQLdb.connect(
        host='localhost',
        user='root',
        passwd='',  # Update if root has a password
    )
    cursor = conn.cursor()
    
    # Drop existing database
    cursor.execute("DROP DATABASE IF EXISTS blood_db")
    print("✓ Dropped existing blood_db database")
    
    # Create fresh database with proper charset
    cursor.execute("""
        CREATE DATABASE blood_db
        CHARACTER SET utf8mb4
        COLLATE utf8mb4_unicode_ci
    """)
    print("✓ Created fresh blood_db database")
    
    # Ensure blood_user exists and has privileges
    cursor.execute("DROP USER IF EXISTS 'blood_user'@'localhost'")
    cursor.execute("CREATE USER 'blood_user'@'localhost' IDENTIFIED BY 'StrongPass@123'")
    cursor.execute("GRANT ALL PRIVILEGES ON blood_db.* TO 'blood_user'@'localhost'")
    cursor.execute("FLUSH PRIVILEGES")
    print("✓ Recreated blood_user with proper privileges")
    
    cursor.close()
    conn.close()
    print("\n✅ Database reset successful!")
    sys.exit(0)
    
except MySQLdb.Error as e:
    print(f"❌ MySQL Error: {e}")
    sys.exit(1)
except Exception as e:
    print(f"❌ Error: {e}")
    sys.exit(1)
