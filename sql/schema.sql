-- Типы статусов 
CREATE TYPE booking_status AS ENUM ('booked', 'completed', 'canceled');
CREATE TYPE contract_status AS ENUM ('active', 'expired');
CREATE TYPE subscription_type AS ENUM ('hourly', 'group');
CREATE TYPE user_role AS ENUM ('admin', 'manager');

-- Таблица клиентов
CREATE TABLE staging.client (
    id_client         SERIAL PRIMARY KEY,
    last_name         VARCHAR(50) NOT NULL,
    first_name        VARCHAR(50) NOT NULL,
    middle_name       VARCHAR(50),
    phone             VARCHAR(11) NOT NULL,
    birth_date        DATE,
    registration_date DATE DEFAULT CURRENT_DATE
);

-- Таблица типов абонементов
CREATE TABLE staging.subscription (
    id_subscription SERIAL PRIMARY KEY,
    name            VARCHAR(50) NOT NULL,
    type            subscription_type NOT NULL,
    hours_amount    INT,
    duration_days   INT NOT NULL,
    price           DECIMAL(10,2) NOT NULL
);

-- Таблица договоров
CREATE TABLE staging.contract (
    id_contract     SERIAL PRIMARY KEY,
    id_client       INT NOT NULL REFERENCES staging.client(id_client),
    id_subscription INT NOT NULL REFERENCES staging.subscription(id_subscription),
    start_date      DATE NOT NULL,
    end_date        DATE NOT NULL,
    hours_remaining INT,
    status          contract_status DEFAULT 'active'
);

-- Таблица пользователей
CREATE TABLE staging."user" (
    id_user   SERIAL PRIMARY KEY,
    login     VARCHAR(50) UNIQUE NOT NULL,
    password  VARCHAR(50) NOT NULL,
    role      user_role NOT NULL,
    name      VARCHAR(150) NOT NULL,
    phone     VARCHAR(11)
);

-- Таблица бронирований
CREATE TABLE staging.booking (
    id_booking   SERIAL PRIMARY KEY,
    id_contract  INT NOT NULL REFERENCES staging.contract(id_contract),
    id_user      INT NOT NULL REFERENCES staging."user"(id_user),
    booking_date DATE NOT NULL,
    start_time   TIME NOT NULL,
    end_time     TIME NOT NULL,
    court_number INT NOT NULL,
    hours_spent  INT,
    status       booking_status DEFAULT 'booked'
);
