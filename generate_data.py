import psycopg2
import random
from datetime import date, timedelta
from datetime import time


"""
---------------------------------
Подключение таблиц с их пересозданием
---------------------------------
"""
conn = psycopg2.connect(
    host="localhost",
    dbname="tennis_center",
    user="postgres",
    password="7255"
)
cursor = conn.cursor()

with open("sql/schema.sql", "r", encoding="utf-8") as f:
    schema_sql = f.read()

cursor.execute(schema_sql)
conn.commit()

print("Таблицы созданы")


"""
---------------------------------
Генерация сотрудников
---------------------------------
"""

cursor.execute("""
    INSERT INTO staging.employee (login, password, role, name, phone)
    VALUES ('admin', 'admin123', 'admin', 'Администратор', '79990000001'),
    ('manager1', 'manager123', 'manager', 'Менеджер Ольга', '79990000002')    
""")

print("Сотрудники созданы")


"""
---------------------------------
Создание массивов для случайных данных клиентов
---------------------------------
"""

last_names = [
    "Иванов", "Петров", "Смирнов", "Кузнецов", "Волков",
    "Соколов", "Морозов", "Новиков", "Фёдоров", "Михайлов"
]
first_names = [
    "Александр", "Мария", "Дмитрий", "Анна", "Сергей",
    "Елена", "Игорь", "Ольга", "Павел", "Татьяна"
]
middle_names = [
    "Александрович", "Сергеевна", "Игоревна", "Дмитриевич",
    "Олеговна", "Павлович", "Андреевна", "Николаевич"
]

"""
---------------------------------
Генерация клиентов
---------------------------------
"""

for i in range(50):
    last_name = random.choice(last_names)
    first_name = random.choice(first_names)
    middle_name = random.choice(middle_names)
    phone = '8999' + str(random.randint(1000000, 9999999))
    birth_date = date(random.randint(1970, 2005), random.randint(1, 12), random.randint(1, 28))
    registration_date = date.today() - timedelta(days=random.randint(0, 180))
    cursor.execute("""
    INSERT INTO staging.client (last_name, first_name, middle_name, phone, birth_date, registration_date)
    VALUES (%s, %s, %s, %s, %s, %s)
    """, (last_name, first_name, middle_name, phone, birth_date, registration_date))



"""
---------------------------------
Виды абонементов
---------------------------------
"""
cursor.execute("""
    INSERT INTO staging.subscription (name, type, hours_amount, duration_days, price)
    VALUES
    ('Разовое занятие', 'hourly', 1, 30, 1500.00),
    ('Абонемент на 4 занятия', 'hourly', 4, 30, 5500.00),
    ('Абонемент на 8 занятий', 'hourly', 8, 60, 10000.00),
    ('Групповая тренировка', 'group', NULL, 30, 800.00),
    ('Месячный безлимит', 'hourly', 30, 30, 20000.00)
""")



"""
---------------------------------
Генерация договоров
---------------------------------
"""
cursor.execute("SELECT id_client FROM staging.client")
clients_ids = [row[0] for row in cursor.fetchall()]

cursor.execute("SELECT id_subscription, duration_days FROM staging.subscription")
subscriptions = cursor.fetchall()

for client_id in clients_ids:
    for i in range(random.randint(1, 3)):
        subscription_id, duration_days = random.choice(subscriptions)
        start_date = date.today() - timedelta(days=random.randint(0, 180))
        end_date = start_date + timedelta(days=duration_days)
        hours_remaining = random.randint(0, 10)
        status = random.choice(['active', 'expired'])
        cursor.execute("""
            INSERT INTO staging.contract (id_client, id_subscription, start_date, end_date, hours_remaining, status)
            VALUES (%s, %s, %s, %s, %s, %s)
                       """, (client_id, subscription_id, start_date, end_date, hours_remaining, status))


"""
---------------------------------
Генерация бронирований
---------------------------------
"""

cursor.execute("SELECT id_contract FROM staging.contract")
contract_ids = [row[0] for row in cursor.fetchall()]
cursor.execute("SELECT id_employee FROM staging.employee")
employee_ids = [row[0] for row in cursor.fetchall()]

for contract_id in contract_ids:
    for _ in range(random.randint(0, 5)):
        employee_id = random.choice(employee_ids)
        rand_date = date.today() - timedelta(days=random.randint(0, 90))
        start_time = time(random.randint(8, 20), 0)
        end_time = time(start_time.hour + 1, 0)
        court = random.randint(1, 4)
        hours_spent = 1
        status = random.choice(['booked', 'completed', 'canceled'])
        cursor.execute("""
        INSERT INTO staging.booking (id_contract, id_employee, booking_date, start_time, end_time, court_number, hours_spent, status)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (contract_id, employee_id, rand_date, start_time, end_time, court, hours_spent, status))

print("Тестовые данные сгенерированы")

conn.commit()