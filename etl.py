import psycopg2
from datetime import date, timedelta


conn = psycopg2.connect(
    host="localhost",
    user="postgres",
    password="7255",
    database="tennis_center",
)

cursor = conn.cursor()

cursor.execute("SELECT id_client, last_name, first_name, middle_name, birth_date, registration_date FROM staging.client")
rows = cursor.fetchall()

for row in rows:
    today = date.today()
    id_client, last_name, first_name, middle_name, birth_date, registration_date = row
    full_name = f"{last_name} {first_name} {middle_name}"
    age = (today - birth_date).days // 365
    registration_month = date(registration_date.year, registration_date.month, 1)
    cursor.execute("""
    INSERT INTO dwh.dim_client (client_id, full_name, birth_date, age, registration_date, registration_month) 
    VALUES (%s, %s, %s, %s, %s, %s)
    """, (id_client, full_name, birth_date, age, registration_date, registration_month))


cursor.execute("SELECT id_subscription, name, type, hours_amount, duration_days, price from staging.subscription")
rows = cursor.fetchall()
for row in rows:
    subscription_id, name, type, hours_amount, duration_days, price = row
    cursor.execute("""
    INSERT INTO dwh.dim_subscription (subscription_id, name, type, hours_amount, duration_days, price) 
    VALUES (%s, %s, %s, %s, %s, %s)
    """, (subscription_id, name, type, hours_amount, duration_days, price))


cursor.execute("SELECT id_contract, id_client, id_subscription, start_date, end_date, hours_remaining, status "
               "from staging.contract")
rows = cursor.fetchall()
for row in rows:
    contract_id, client_id, subscription_id, start_date, end_date, hours_remaining, status = row
    cursor.execute("""
    INSERT INTO dwh.fact_contract (contract_id, client_id, subscription_id, start_date, end_date, hours_remaining, status) 
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (contract_id, client_id, subscription_id, start_date, end_date, hours_remaining, status))


cursor.execute("SELECT id_booking, id_contract, id_employee, booking_date, start_time, end_time, court_number, "
               "hours_spent, status from staging.booking")
rows = cursor.fetchall()
for row in rows:
    booking_id, id_contract, id_employee, booking_date, start_time, end_time, court_number, hours_spent, status = row
    cursor.execute("""
    INSERT INTO dwh.fact_booking (booking_id, contract_id, user_id, booking_date, start_time, end_time, court_number, 
    hours_spent, status)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (booking_id, id_contract, id_employee, booking_date, start_time, end_time, court_number, hours_spent, status))

current_date = date(2024, 1, 1)
months = ["Январь", "Февраль", "Март", "Апрель", "Май", "Июнь",
          "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"]
end_date = date.today()
weekdays = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]

while current_date <= end_date:
    full_date = current_date
    day_of_week = weekdays[current_date.weekday()]
    month_name = months[current_date.month - 1]
    date_id = current_date.strftime("%Y%m%d")
    cursor.execute("""
    INSERT INTO dwh.dim_date (date_id, full_date, day_of_week, month_num, month_name, year_num)
    VALUES (%s, %s, %s, %s, %s, %s)
    """, (date_id, full_date, day_of_week, current_date.month, month_name, current_date.year))
    current_date += timedelta(days=1)

conn.commit()