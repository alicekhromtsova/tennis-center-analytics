DROP SCHEMA IF EXISTS marts CASCADE;

CREATE SCHEMA marts;

CREATE TABLE marts.mart_new_clients AS
	SELECT registration_month as month,
		COUNT(*) as new_clients_count
	FROM dwh.dim_client
	GROUP BY registration_month
	ORDER BY registration_month;

CREATE TABLE marts.mart_client_retention AS
	WITH client_bookings AS(
		SELECT c.client_id, count(b.booking_id) as booking_count
		FROM dwh.fact_contract c
		JOIN dwh.fact_booking b ON c.contract_id = b.contract_id
		GROUP BY c.client_id
	)
	SELECT COUNT(*) AS total_clients, 
		SUM(CASE WHEN booking_count > 1 THEN 1 ELSE 0 END) AS returning_clients,
		ROUND(100.0 * SUM(CASE WHEN booking_count > 1 THEN 1 ELSE 0 END) / COUNT(*),2) AS retention_rate
	FROM client_bookings;

CREATE TABLE marts.mart_court_load AS
	SELECT 
		court_number, 
		count(*) AS booking_count, 
		SUM(CASE WHEN status = 'canceled' THEN 1 ELSE 0 END) AS canceled_count
	FROM dwh.fact_booking
	GROUP BY court_number;