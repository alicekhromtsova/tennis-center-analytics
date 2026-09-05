CREATE SCHEMA staging;

--Статусы--
CREATE TYPE booking_status AS ENUM ('booked', 'completed', 'canceled');
CREATE TYPE subscription_type AS ENUM ('hourly', 'group');
CREATE TYPE contract_status AS ENUM ('active', 'expired');
CREATE TYPE user_role AS ENUM ('admin', 'manager');

--Таблица клиентов--
CREATE TABLE staging.client(
	id_client         SERIAL       PRIMARY KEY,
	last_name         VARCHAR(100) NOT NULL,
	first_name        VARCHAR(100) NOT NULL,
	middle_name       VARCHAR(100),
	phone             VARCHAR(15) NOT NULL,
	birth_date        DATE        NOT NULL,
	registration_date DATE        DEFAULT CURRENT_DATE
);

--Таблица абонемента--
CREATE TABLE staging.subscription(
	id_subscription SERIAL      PRIMARY KEY,
	name            VARCHAR(50) NOT NULL,
	type subscription_type      DEFAULT 'hourly',
	hours_amount    INT,
	duration_days   INT,
	price           DECIMAL(10,2)
);

--Таблица договор--
CREATE TABLE staging.contract(
	id_contract     SERIAL PRIMARY KEY,
	id_client       INT    REFERENCES staging.client(id_client),
	id_subscription INT    REFERENCES staging.subscription(id_subscription),
	start_date      DATE,
	end_date        DATE,
	hours_remaining INT,
	status contract_status DEFAULT 'active'
);

--Таблица работники--
CREATE TABLE staging.employee(
	id_employee SERIAL       PRIMARY KEY,
	login       VARCHAR(50)  UNIQUE NOT NULL,
	password    VARCHAR(50)  NOT NULL,
	role user_role,
	name        VARCHAR(100) NOT NULL,
	phone       VARCHAR(15)
);

--Табоица бронирования--
CREATE TABLE staging.booking(
	id_booking SERIAL PRIMARY KEY,
	id_contract INT REFERENCES staging.contract(id_contract),
	id_employee INT REFERENCES staging.employee(id_employee),
	booking_date DATE,
	start_time TIME,
	end_time TIME,
	court_number INT,
	hours_spent INT,
	status booking_status DEFAULT 'booked'
);
