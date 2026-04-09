-- ============================================================
--  Blood Management System — MySQL Dataset
--  Compatible with: MySQL 8.0+ / MariaDB 10.5+
--  Generated for Django 4.2 project
--  
--  HOW TO USE:
--    1. Create a database:   CREATE DATABASE blood_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
--    2. Import this file:    mysql -u root -p blood_db < blood_management_mysql.sql
--    3. Update settings.py  (see mysql_settings.py in this project)
--    4. Run:                 python manage.py migrate --run-syncdb (skip if tables already exist)
-- ============================================================

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;
SET SQL_MODE = 'NO_AUTO_VALUE_ON_ZERO';
SET time_zone = '+00:00';

-- ─────────────────────────────────────────────
-- Django Required Tables
-- ─────────────────────────────────────────────

CREATE TABLE IF NOT EXISTS `django_content_type` (
  `id`       int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model`    varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model` (`app_label`, `model`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `auth_permission` (
  `id`              int NOT NULL AUTO_INCREMENT,
  `name`            varchar(255) NOT NULL,
  `content_type_id` int NOT NULL,
  `codename`        varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename` (`content_type_id`, `codename`),
  CONSTRAINT `auth_permission_content_type_id_fk` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `auth_group` (
  `id`   int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `auth_group_permissions` (
  `id`            bigint NOT NULL AUTO_INCREMENT,
  `group_id`      int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id` (`group_id`, `permission_id`),
  CONSTRAINT `agp_group_id_fk`      FOREIGN KEY (`group_id`)      REFERENCES `auth_group` (`id`),
  CONSTRAINT `agp_permission_id_fk` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ─────────────────────────────────────────────
-- accounts_customuser
-- ─────────────────────────────────────────────

CREATE TABLE IF NOT EXISTS `accounts_customuser` (
  `id`           bigint       NOT NULL AUTO_INCREMENT,
  `password`     varchar(128) NOT NULL,
  `last_login`   datetime(6)           DEFAULT NULL,
  `is_superuser` tinyint(1)   NOT NULL DEFAULT 0,
  `username`     varchar(150) NOT NULL,
  `first_name`   varchar(150) NOT NULL DEFAULT '',
  `last_name`    varchar(150) NOT NULL DEFAULT '',
  `email`        varchar(254) NOT NULL DEFAULT '',
  `is_staff`     tinyint(1)   NOT NULL DEFAULT 0,
  `is_active`    tinyint(1)   NOT NULL DEFAULT 1,
  `date_joined`  datetime(6)  NOT NULL,
  `role`         varchar(10)  NOT NULL DEFAULT 'donor',
  `phone`        varchar(15)  NOT NULL DEFAULT '',
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Passwords are Django pbkdf2_sha256 hashes
-- Plaintext: admin → Admin@1234  |  donors → Donor@1234
INSERT INTO `accounts_customuser`
  (`id`,`password`,`last_login`,`is_superuser`,`username`,`first_name`,`last_name`,`email`,`is_staff`,`is_active`,`date_joined`,`role`,`phone`)
VALUES
  (1,
   'pbkdf2_sha256$1200000$IA1rxHsEkoMVlGo5pFAqfV$4fmTraBqUcFGboEPLcfnbbQ2TxiA1t/JjXudeBw1yb4=',
   NULL,1,'admin','System','Admin','admin@bloodms.com',1,1,'2026-04-07 03:31:04.134841','admin',''),

  (2,
   'pbkdf2_sha256$1200000$XcLoQbEr0pUto1pioQwBgL$0dOedNy2lgw5NHEPBqRyKXxPAKzAm8iJxU1JRqFesww=',
   NULL,0,'rahul_donor','Rahul','Islam','rahul@ex.com',0,1,'2026-04-07 03:31:04.522514','donor','01700000000'),

  (3,
   'pbkdf2_sha256$1200000$ICaF15ko9aqM205F5DYs9J$m/kVDX1k2gvqtUql8csU3Aew2mPhkCSQaduTUlOWKgs=',
   NULL,0,'fatima_d','Fatima','Khan','fatima@ex.com',0,1,'2026-04-07 03:31:04.884717','donor','01700000000'),

  (4,
   'pbkdf2_sha256$1200000$Y3d3z1nDr0t0dJulPTvkEG$vTdonIw6v13uCyn8h+Qr+J1UtKmBPK1osZwXxuNmo00=',
   NULL,0,'sohel_d','Sohel','Rana','sohel@ex.com',0,1,'2026-04-07 03:31:05.263675','donor','01700000000'),

  (5,
   'pbkdf2_sha256$1200000$NtEGazkjD47He2attYZTRa$WbC8Eo6AsqNfICmeVLNotMy07DAtVyn1qWoAzw4oKZk=',
   NULL,0,'nasreen_d','Nasreen','Akter','nasreen@ex.com',0,1,'2026-04-07 03:31:05.635424','donor','01700000000'),

  (6,
   'pbkdf2_sha256$1200000$UZlC2vYVU6a7f6NXo0SrR5$9giiyx69T/54G0uCbYYjY7Z3ybM639flOSgIPCSXZ0Q=',
   NULL,0,'karim_d','Abdul','Karim','karim@ex.com',0,1,'2026-04-07 03:31:06.033272','donor','01700000000');

-- ─────────────────────────────────────────────
-- accounts_donorprofile
-- ─────────────────────────────────────────────

CREATE TABLE IF NOT EXISTS `accounts_donorprofile` (
  `id`                 bigint      NOT NULL AUTO_INCREMENT,
  `user_id`            bigint      NOT NULL,
  `blood_group`        varchar(3)  NOT NULL,
  `date_of_birth`      date                 DEFAULT NULL,
  `gender`             varchar(10) NOT NULL DEFAULT '',
  `city`               varchar(100) NOT NULL DEFAULT '',
  `area`               varchar(100) NOT NULL DEFAULT '',
  `address`            longtext    NOT NULL,
  `is_available`       tinyint(1)  NOT NULL DEFAULT 1,
  `last_donation_date` date                 DEFAULT NULL,
  `profile_photo`      varchar(100) NOT NULL DEFAULT '',
  `bio`                longtext    NOT NULL,
  `total_donations`    int unsigned NOT NULL DEFAULT 0,
  `created_at`         datetime(6) NOT NULL,
  `updated_at`         datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `donorprofile_user_id_fk` FOREIGN KEY (`user_id`) REFERENCES `accounts_customuser` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO `accounts_donorprofile`
  (`id`,`user_id`,`blood_group`,`date_of_birth`,`gender`,`city`,`area`,`address`,`is_available`,`last_donation_date`,`profile_photo`,`bio`,`total_donations`,`created_at`,`updated_at`)
VALUES
  (1,2,'A+', NULL,'','Dhaka','Mirpur',   '',1,'2026-01-07','','',2,'2026-04-07 03:31:04.878034','2026-04-07 03:31:04.878051'),
  (2,3,'B+', NULL,'','Chittagong','GEC', '',1,'2026-01-07','','',2,'2026-04-07 03:31:05.235472','2026-04-07 03:31:05.235486'),
  (3,4,'O+', NULL,'','Dhaka','Uttara',   '',1,'2026-01-07','','',2,'2026-04-07 03:31:05.629000','2026-04-07 03:31:05.629015'),
  (4,5,'AB+',NULL,'','Sylhet','Zindabazar','',1,'2026-01-07','','',2,'2026-04-07 03:31:06.027041','2026-04-07 03:31:06.027056'),
  (5,6,'O-', NULL,'','Dhaka','Dhanmondi','',1,'2026-01-07','','',2,'2026-04-07 03:31:06.399233','2026-04-07 03:31:06.399250');

-- ─────────────────────────────────────────────
-- blood_bloodbank
-- ─────────────────────────────────────────────

CREATE TABLE IF NOT EXISTS `blood_bloodbank` (
  `id`             bigint       NOT NULL AUTO_INCREMENT,
  `name`           varchar(200) NOT NULL,
  `location`       varchar(300) NOT NULL,
  `city`           varchar(100) NOT NULL,
  `contact_number` varchar(15)  NOT NULL,
  `email`          varchar(254) NOT NULL DEFAULT '',
  `is_active`      tinyint(1)   NOT NULL DEFAULT 1,
  `created_at`     datetime(6)  NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO `blood_bloodbank` (`id`,`name`,`location`,`city`,`contact_number`,`email`,`is_active`,`created_at`)
VALUES
  (1,'Dhaka Central Blood Bank','Shahbagh','Dhaka','02-9661111','dhaka@bloodbank.com',1,'2026-04-07 03:31:06.405922'),
  (2,'Chittagong Blood Center','Agrabad','Chittagong','031-714455','ctg@bloodbank.com',1,'2026-04-07 03:31:06.412634'),
  (3,'BSMMU Blood Bank','Shahbagh, Dhaka','Dhaka','02-9661100','',1,'2026-04-07 03:31:06.419325');

-- ─────────────────────────────────────────────
-- blood_bloodinventory
-- ─────────────────────────────────────────────

CREATE TABLE IF NOT EXISTS `blood_bloodinventory` (
  `id`              bigint     NOT NULL AUTO_INCREMENT,
  `blood_bank_id`   bigint     NOT NULL,
  `blood_group`     varchar(3) NOT NULL,
  `units_available` int unsigned NOT NULL DEFAULT 0,
  `updated_at`      datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `blood_bloodinventory_bank_group` (`blood_bank_id`,`blood_group`),
  CONSTRAINT `inventory_bank_id_fk` FOREIGN KEY (`blood_bank_id`) REFERENCES `blood_bloodbank` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO `blood_bloodinventory` (`id`,`blood_bank_id`,`blood_group`,`units_available`,`updated_at`)
VALUES
  -- Dhaka Central Blood Bank
  ( 1,1,'A+', 18,'2026-04-07 03:31:06.425883'),
  ( 2,1,'A-', 24,'2026-04-07 03:31:06.433228'),
  ( 3,1,'B+', 15,'2026-04-07 03:31:06.440560'),
  ( 4,1,'B-',  1,'2026-04-07 03:31:06.447648'),
  ( 5,1,'AB+',25,'2026-04-07 03:31:06.454276'),
  ( 6,1,'AB-',21,'2026-04-07 03:31:06.460726'),
  ( 7,1,'O+',  2,'2026-04-07 03:31:06.466684'),
  ( 8,1,'O-', 20,'2026-04-07 03:31:06.472409'),
  -- Chittagong Blood Center
  ( 9,2,'A+', 17,'2026-04-07 03:31:06.478573'),
  (10,2,'A-', 10,'2026-04-07 03:31:06.484466'),
  (11,2,'B+',  1,'2026-04-07 03:31:06.490141'),
  (12,2,'B-', 24,'2026-04-07 03:31:06.496315'),
  (13,2,'AB+', 8,'2026-04-07 03:31:06.502294'),
  (14,2,'AB-',13,'2026-04-07 03:31:06.509428'),
  (15,2,'O+',  5,'2026-04-07 03:31:06.515575'),
  (16,2,'O-',  3,'2026-04-07 03:31:06.521916'),
  -- BSMMU Blood Bank
  (17,3,'A+', 21,'2026-04-07 03:31:06.527726'),
  (18,3,'A-', 18,'2026-04-07 03:31:06.533800'),
  (19,3,'B+', 24,'2026-04-07 03:31:06.539756'),
  (20,3,'B-', 17,'2026-04-07 03:31:06.545637'),
  (21,3,'AB+', 4,'2026-04-07 03:31:06.551536'),
  (22,3,'AB-',14,'2026-04-07 03:31:06.556925'),
  (23,3,'O+', 14,'2026-04-07 03:31:06.564581'),
  (24,3,'O-',  9,'2026-04-07 03:31:06.571489');

-- ─────────────────────────────────────────────
-- blood_blooddonation
-- ─────────────────────────────────────────────

CREATE TABLE IF NOT EXISTS `blood_blooddonation` (
  `id`            bigint      NOT NULL AUTO_INCREMENT,
  `donor_id`      bigint      NOT NULL,
  `blood_bank_id` bigint               DEFAULT NULL,
  `blood_group`   varchar(3)  NOT NULL,
  `units`         int unsigned NOT NULL DEFAULT 1,
  `donation_date` date        NOT NULL,
  `status`        varchar(10) NOT NULL DEFAULT 'pending',
  `notes`         longtext    NOT NULL,
  `admin_remarks` longtext    NOT NULL,
  `created_at`    datetime(6) NOT NULL,
  `updated_at`    datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `donation_donor_id`      (`donor_id`),
  KEY `donation_blood_bank_id` (`blood_bank_id`),
  CONSTRAINT `donation_donor_id_fk`      FOREIGN KEY (`donor_id`)      REFERENCES `accounts_customuser` (`id`) ON DELETE CASCADE,
  CONSTRAINT `donation_blood_bank_id_fk` FOREIGN KEY (`blood_bank_id`) REFERENCES `blood_bloodbank`    (`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO `blood_blooddonation`
  (`id`,`donor_id`,`blood_bank_id`,`blood_group`,`units`,`donation_date`,`status`,`notes`,`admin_remarks`,`created_at`,`updated_at`)
VALUES
  (1, 2,1,'A+',1,'2026-04-07','approved','Healthy, no issues.','','2026-04-07 03:31:06.577012','2026-04-07 03:31:06.577026'),
  (2, 2,2,'A+',1,'2026-01-07','approved','',                   '','2026-04-07 03:31:06.583048','2026-04-07 03:31:06.583060'),
  (3, 3,2,'B+',1,'2026-03-28','approved','Healthy, no issues.','','2026-04-07 03:31:06.588506','2026-04-07 03:31:06.588517'),
  (4, 3,3,'B+',1,'2026-01-02','approved','',                   '','2026-04-07 03:31:06.594379','2026-04-07 03:31:06.594389'),
  (5, 4,3,'O+',1,'2026-03-18','pending', 'Healthy, no issues.','','2026-04-07 03:31:06.600458','2026-04-07 03:31:06.600471'),
  (6, 4,1,'O+',1,'2025-12-28','approved','',                   '','2026-04-07 03:31:06.605804','2026-04-07 03:31:06.605815'),
  (7, 5,1,'AB+',1,'2026-03-08','rejected','Healthy, no issues.','','2026-04-07 03:31:06.612001','2026-04-07 03:31:06.612013'),
  (8, 5,2,'AB+',1,'2025-12-23','approved','',                  '','2026-04-07 03:31:06.617902','2026-04-07 03:31:06.617913'),
  (9, 6,2,'O-', 1,'2026-02-26','approved','Healthy, no issues.','','2026-04-07 03:31:06.623984','2026-04-07 03:31:06.624003'),
  (10,6,3,'O-', 1,'2025-12-18','approved','',                  '','2026-04-07 03:31:06.629800','2026-04-07 03:31:06.629814');

-- ─────────────────────────────────────────────
-- blood_bloodrequest
-- ─────────────────────────────────────────────

CREATE TABLE IF NOT EXISTS `blood_bloodrequest` (
  `id`             bigint       NOT NULL AUTO_INCREMENT,
  `requester_id`   bigint       NOT NULL,
  `blood_group`    varchar(3)   NOT NULL,
  `units_needed`   int unsigned NOT NULL DEFAULT 1,
  `patient_name`   varchar(200) NOT NULL,
  `hospital_name`  varchar(200) NOT NULL,
  `hospital_city`  varchar(100) NOT NULL DEFAULT '',
  `contact_number` varchar(15)  NOT NULL,
  `urgency`        varchar(10)  NOT NULL DEFAULT 'normal',
  `status`         varchar(10)  NOT NULL DEFAULT 'pending',
  `reason`         longtext     NOT NULL,
  `admin_remarks`  longtext     NOT NULL,
  `required_date`  date                  DEFAULT NULL,
  `created_at`     datetime(6)  NOT NULL,
  `updated_at`     datetime(6)  NOT NULL,
  PRIMARY KEY (`id`),
  KEY `request_requester_id` (`requester_id`),
  CONSTRAINT `request_requester_id_fk` FOREIGN KEY (`requester_id`) REFERENCES `accounts_customuser` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO `blood_bloodrequest`
  (`id`,`requester_id`,`blood_group`,`units_needed`,`patient_name`,`hospital_name`,`hospital_city`,`contact_number`,`urgency`,`status`,`reason`,`admin_remarks`,`required_date`,`created_at`,`updated_at`)
VALUES
  (1,2,'A+', 2,'Hasan Mahmud','DMCH',          'Dhaka',      '01700111222','urgent',  'pending', 'Surgery needed','',NULL,'2026-04-07 03:31:06.637144','2026-04-07 03:31:06.637167'),
  (2,3,'O-', 1,'Rina Begum',  'CMH Chittagong','Chittagong',  '01800333444','critical','approved','',              '',NULL,'2026-04-07 03:31:06.643131','2026-04-07 03:31:06.643146'),
  (3,4,'B+', 3,'Rafiq Ahmed', 'BSMMU',         'Dhaka',      '01900555666','normal',  'fulfilled','',             '',NULL,'2026-04-07 03:31:06.649396','2026-04-07 03:31:06.649412');

-- ─────────────────────────────────────────────
-- Django Sessions & Admin Log (empty — Django will populate)
-- ─────────────────────────────────────────────

CREATE TABLE IF NOT EXISTS `django_session` (
  `session_key`  varchar(40)  NOT NULL,
  `session_data` longtext     NOT NULL,
  `expire_date`  datetime(6)  NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `django_admin_log` (
  `id`              int          NOT NULL AUTO_INCREMENT,
  `action_time`     datetime(6)  NOT NULL,
  `object_id`       longtext,
  `object_repr`     varchar(200) NOT NULL,
  `action_flag`     smallint unsigned NOT NULL,
  `change_message`  longtext     NOT NULL,
  `content_type_id` int                   DEFAULT NULL,
  `user_id`         bigint       NOT NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT `admin_log_user_id_fk`         FOREIGN KEY (`user_id`)         REFERENCES `accounts_customuser` (`id`) ON DELETE CASCADE,
  CONSTRAINT `admin_log_content_type_id_fk` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `accounts_customuser_groups` (
  `id`       bigint NOT NULL AUTO_INCREMENT,
  `customuser_id` bigint NOT NULL,
  `group_id` int    NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `accounts_customuser_groups_customuser_id_group_id` (`customuser_id`,`group_id`),
  CONSTRAINT `cug_customuser_id_fk` FOREIGN KEY (`customuser_id`) REFERENCES `accounts_customuser` (`id`) ON DELETE CASCADE,
  CONSTRAINT `cug_group_id_fk`      FOREIGN KEY (`group_id`)      REFERENCES `auth_group`          (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `accounts_customuser_user_permissions` (
  `id`            bigint NOT NULL AUTO_INCREMENT,
  `customuser_id` bigint NOT NULL,
  `permission_id` int    NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `accounts_customuser_user_perms_customuser_id_permission_id` (`customuser_id`,`permission_id`),
  CONSTRAINT `cup_customuser_id_fk` FOREIGN KEY (`customuser_id`) REFERENCES `accounts_customuser` (`id`) ON DELETE CASCADE,
  CONSTRAINT `cup_permission_id_fk` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission`     (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

SET FOREIGN_KEY_CHECKS = 1;

-- ─────────────────────────────────────────────
-- Summary
-- ─────────────────────────────────────────────
-- Tables created  : 13
-- Users           : 6  (1 admin + 5 donors)
-- Donor Profiles  : 5
-- Blood Banks     : 3
-- Inventory rows  : 24 (8 blood groups × 3 banks)
-- Donations       : 10
-- Blood Requests  : 3
--
-- Demo credentials:
--   Admin  → username: admin       password: Admin@1234
--   Donor  → username: rahul_donor password: Donor@1234
--   Donor  → username: fatima_d    password: Donor@1234
-- ─────────────────────────────────────────────
