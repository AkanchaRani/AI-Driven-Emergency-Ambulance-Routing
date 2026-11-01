-- ============================================================================
-- AI-Driven Emergency Ambulance Routing System - database creation script
-- Target: MySQL 8.0
--
-- This file only creates the (empty) database.
-- The TABLES are created and updated by Alembic migrations, so that future
-- changes never require dropping the database or losing data:
--
--     cd backend
--     python -m app.database.initialize_db
--
-- The full table design is listed in database/schema_snapshot.sql (reference).
-- ============================================================================

CREATE DATABASE IF NOT EXISTS ambulance_routing_db
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE ambulance_routing_db;
