-- إنشاء قاعدة البيانات لو مش موجودة
-- Create database if not exists
CREATE DATABASE ny_taxi;

-- الدخول على قاعدة البيانات
-- Connect to database
\c ny_taxi

-- إنشاء جدول الرحلات
-- Create trips table
CREATE TABLE green_tripdata (
    lpep_pickup_datetime TIMESTAMP,
    lpep_dropoff_datetime TIMESTAMP,
    PULocationID INT,
    DOLocationID INT,
    trip_distance FLOAT,
    tip_amount FLOAT,
    total_amount FLOAT
);

-- إنشاء جدول مناطق التاكسي
-- Create taxi zones table
CREATE TABLE taxi_zone_lookup (
    LocationID INT,
    Borough TEXT,
    Zone TEXT,
    service_zone TEXT
);
