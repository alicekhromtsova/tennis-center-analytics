DROP SCHEMA IF EXISTS dwh CASCADE;

CREATE SCHEMA dwh;


CREATE TABLE dwh.dim_client(
	client_id          INT          PRIMARY KEY,
	full_name          VARCHAR(150) NOT NULL,
	birth_date         DATE,
	age                INT,
	registration_date  DATE         NOT NULL,
	registration_month DATE         NOT NULL
);

CREATE TABLE dwh.dim_subscription(
	subscription_id INT           PRIMARY KEY,
	name            VARCHAR(50)   NOT NULL,
	type            VARCHAR(20)   NOT NULL,
	hours_amount    INT,
	duration_days   INT           NOT NULL,
	price           DECIMAL(10,2) NOT NULL
);

CREATE TABLE dwh.dim_date(
	date_id     INT         PRIMARY KEY,
	full_date   DATE        NOT NULL,
	day_of_week VARCHAR(20),
	month_num   INT,
	month_name  VARCHAR(20),
	year_num    INT
);

CREATE TABLE dwh.fact_contract(
	contract_id     INT  PRIMARY KEY,
	client_id       INT  NOT NULL REFERENCES dwh.dim_client(client_id),
	subscription_id INT  NOT NULL REFERENCES dwh.dim_subscription(subscription_id),
	start_date      DATE NOT NULL,
	end_date        DATE NOT NULL,
	hours_remaining INT,
	status          VARCHAR(20)
);

CREATE TABLE dwh.fact_booking(
	booking_id   INT  PRIMARY KEY,
	contract_id  INT  NOT NULL REFERENCES dwh.fact_contract(contract_id),
	user_id      INT  NOT NULL,
	booking_date DATE NOT NULL,
	start_time   TIME NOT NULL,
	end_time     TIME NOT NULL,
	court_number INT  NOT NULL,
	hours_spent  INT,
	status       VARCHAR(20)
);