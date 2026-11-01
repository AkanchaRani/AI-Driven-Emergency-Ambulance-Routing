-- Reference copy of the table design (MySQL 8.0 syntax).
-- Generated from backend/app/database/models.py - do NOT run this file;
-- tables are created by Alembic migrations (see database.sql).

CREATE TABLE hospitals (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	name VARCHAR(150) NOT NULL, 
	address VARCHAR(255) NOT NULL, 
	phone VARCHAR(20), 
	latitude FLOAT NOT NULL, 
	longitude FLOAT NOT NULL, 
	total_beds INTEGER NOT NULL, 
	available_beds INTEGER NOT NULL, 
	has_icu BOOL NOT NULL, 
	has_trauma_centre BOOL NOT NULL, 
	created_at DATETIME NOT NULL, 
	updated_at DATETIME NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (name)
);

CREATE TABLE users (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	full_name VARCHAR(100) NOT NULL, 
	email VARCHAR(120) NOT NULL, 
	phone VARCHAR(20), 
	password_hash VARCHAR(255) NOT NULL, 
	`role` VARCHAR(20) NOT NULL, 
	is_active BOOL NOT NULL, 
	created_at DATETIME NOT NULL, 
	updated_at DATETIME NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (email)
);

CREATE TABLE ambulances (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	registration_number VARCHAR(30) NOT NULL, 
	ambulance_type VARCHAR(20) NOT NULL, 
	status VARCHAR(20) NOT NULL, 
	driver_id INTEGER, 
	base_hospital_id INTEGER, 
	current_latitude FLOAT, 
	current_longitude FLOAT, 
	created_at DATETIME NOT NULL, 
	updated_at DATETIME NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (registration_number), 
	FOREIGN KEY(driver_id) REFERENCES users (id) ON DELETE SET NULL, 
	FOREIGN KEY(base_hospital_id) REFERENCES hospitals (id) ON DELETE SET NULL
);
CREATE INDEX ix_ambulances_status ON ambulances (status);

CREATE TABLE emergency_requests (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	caller_name VARCHAR(100) NOT NULL, 
	caller_phone VARCHAR(20) NOT NULL, 
	patient_name VARCHAR(100), 
	patient_age INTEGER, 
	patient_gender VARCHAR(10), 
	emergency_type VARCHAR(30) NOT NULL, 
	description TEXT, 
	severity VARCHAR(10) NOT NULL, 
	status VARCHAR(20) NOT NULL, 
	location_address VARCHAR(255) NOT NULL, 
	latitude FLOAT, 
	longitude FLOAT, 
	created_by INTEGER, 
	created_at DATETIME NOT NULL, 
	updated_at DATETIME NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(created_by) REFERENCES users (id) ON DELETE SET NULL
);
CREATE INDEX ix_emergency_created_at ON emergency_requests (created_at);
CREATE INDEX ix_emergency_severity ON emergency_requests (severity);
CREATE INDEX ix_emergency_status ON emergency_requests (status);

CREATE TABLE assignments (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	emergency_id INTEGER NOT NULL, 
	ambulance_id INTEGER NOT NULL, 
	hospital_id INTEGER, 
	assigned_by INTEGER, 
	status VARCHAR(20) NOT NULL, 
	notes VARCHAR(255), 
	assigned_at DATETIME NOT NULL, 
	updated_at DATETIME NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(emergency_id) REFERENCES emergency_requests (id) ON DELETE CASCADE, 
	FOREIGN KEY(ambulance_id) REFERENCES ambulances (id) ON DELETE RESTRICT, 
	FOREIGN KEY(hospital_id) REFERENCES hospitals (id) ON DELETE SET NULL, 
	FOREIGN KEY(assigned_by) REFERENCES users (id) ON DELETE SET NULL
);
CREATE INDEX ix_assignments_ambulance ON assignments (ambulance_id);
CREATE INDEX ix_assignments_emergency ON assignments (emergency_id);

CREATE TABLE emergency_status_history (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	emergency_id INTEGER NOT NULL, 
	old_status VARCHAR(20), 
	new_status VARCHAR(20) NOT NULL, 
	changed_by INTEGER, 
	remarks VARCHAR(255), 
	changed_at DATETIME NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(emergency_id) REFERENCES emergency_requests (id) ON DELETE CASCADE, 
	FOREIGN KEY(changed_by) REFERENCES users (id) ON DELETE SET NULL
);
CREATE INDEX ix_status_history_emergency ON emergency_status_history (emergency_id);

CREATE TABLE notifications (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	user_id INTEGER NOT NULL, 
	emergency_id INTEGER, 
	title VARCHAR(150) NOT NULL, 
	message VARCHAR(500) NOT NULL, 
	is_read BOOL NOT NULL, 
	created_at DATETIME NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(user_id) REFERENCES users (id) ON DELETE CASCADE, 
	FOREIGN KEY(emergency_id) REFERENCES emergency_requests (id) ON DELETE CASCADE
);
CREATE INDEX ix_notifications_user_read ON notifications (user_id, is_read);

CREATE TABLE routes (
	id INTEGER NOT NULL AUTO_INCREMENT, 
	assignment_id INTEGER NOT NULL, 
	route_type VARCHAR(20) NOT NULL, 
	distance_km NUMERIC(8, 2), 
	estimated_minutes NUMERIC(6, 1), 
	geometry TEXT, 
	source VARCHAR(30) NOT NULL, 
	created_at DATETIME NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(assignment_id) REFERENCES assignments (id) ON DELETE CASCADE
);
CREATE INDEX ix_routes_assignment ON routes (assignment_id);
