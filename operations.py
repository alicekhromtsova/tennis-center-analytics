import psycopg2
from datetime import date, timedelta

conn = psycopg2.connect(
    host="localhost",
    dbname="tennis_center",
    user="postgres",
    password="7255"
)
cursor = conn.cursor()

"""Добавляет нового клиента и возвращает его id"""
def register_client(last_name, first_name, middle_name, phone, birth_date):
    if not last_name or not first_name or not phone:
        raise ValueError("Фамилия, имя и телефон обязательны")

    cursor.execute("""
        INSERT INTO staging.client (last_name, first_name, middle_name, phone, birth_date)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING id_client
    """, (last_name, first_name, middle_name, phone, birth_date))

    conn.commit()
    return cursor.fetchone()[0]


"""Поиск клиента"""
def search_clients(search_term):
    cursor.execute("""
        SELECT * FROM staging.client
        WHERE last_name LIKE %s OR first_name LIKE %s OR middle_name LIKE %s OR phone LIKE %s
    """, (f"%{search_term}%", f"%{search_term}%", f"%{search_term}%", f"%{search_term}%"))
    conn.commit()
    return cursor.fetchall()


"""Оформляет новый договор"""
def create_contract(client_id, subscription_id, start_date):
    cursor.execute("SELECT duration_days, hours_amount FROM staging.subscription WHERE id_subscription = %s",
                   (subscription_id,))
    subscription = cursor.fetchone()
    if not subscription:
        raise ValueError("Абонемент не найден")
    duration_days, hours_amount = subscription
    cursor.execute("SELECT COUNT(*) FROM staging.contract WHERE id_client = %s AND status = 'active'",
                   (client_id,))
    active_count = cursor.fetchone()[0]
    if active_count > 0:
        raise ValueError("У клиента уже есть активный договор")
    end_date = start_date + timedelta(days=duration_days)
    hours_remaining = hours_amount
    cursor.execute("""
            INSERT INTO staging.contract (id_client, id_subscription, start_date, end_date, hours_remaining, status)
            VALUES (%s, %s, %s, %s, %s, 'active')
            RETURNING id_contract
        """, (client_id, subscription_id, start_date, end_date, hours_remaining))
    conn.commit()
    return cursor.fetchone()[0]



"""Продление договора"""
def renew_contract(client_id):
    cursor.execute("""
        SELECT id_contract, id_subscription, hours_remaining
        FROM staging.contract
        WHERE id_client = %s AND status = 'active'
    """, (client_id,))
    contract = cursor.fetchone()
    if not contract:
        raise ValueError("Активный договор не найден")
    contract_id, id_subscription, hours_remaining = contract
    cursor.execute("SELECT duration_days FROM staging.subscription WHERE id_subscription = %s",
                   (id_subscription,))
    duration_days = cursor.fetchone()[0]
    start_date = date.today()
    end_date = start_date + timedelta(days=duration_days)
    cursor.execute("""
            INSERT INTO staging.contract (id_client, id_subscription, start_date, end_date, hours_remaining, status)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id_contract
        """, (client_id, id_subscription, start_date, end_date, hours_remaining, 'active'))
    conn.commit()
    return cursor.fetchone()[0]


"""Удаление договора"""
def get_client_contracts(client_id):
    cursor.execute("""
        SELECT c.id_contract, s.name, c.start_date, c.end_date, c.hours_remaining, c.status
        FROM staging.contract c
        JOIN staging.subscription s ON c.id_subscription = s.id_subscription
        WHERE c.id_client = %s
        ORDER BY c.id_contract
    """, (client_id,))
    return cursor.fetchall()
    return cursor.fetchall()
def delete_contract(contract_id):
    cursor.execute("DELETE FROM staging.booking WHERE id_contract = %s", (contract_id,))
    cursor.execute("DELETE FROM staging.contract WHERE id_contract = %s", (contract_id,))
    conn.commit()
    return f"Договор {contract_id} удалён"


"""Создание бронирования"""
def create_booking(contract_id, employee_id, booking_date, start_time, end_time, court_number):
    hours_spent = end_time.hour - start_time.hour
    cursor.execute("SELECT hours_remaining, status from staging.contract WHERE id_contract = %s",(contract_id,))
    hours_remaining, status = cursor.fetchone()
    if hours_remaining < hours_spent or status != 'active':
        raise ValueError("Недостаточно часов на абонементе")
    cursor.execute("""
    INSERT INTO staging.booking (id_contract, id_employee, booking_date, start_time, end_time, court_number, hours_spent, status)
    VALUES (%s, %s, %s, %s, %s, %s, %s, 'booked')
    """, (contract_id, employee_id,booking_date, start_time, end_time, court_number, hours_spent))
    cursor.execute("""
    UPDATE staging.contract
    SET hours_remaining = hours_remaining - %s
    WHERE id_contract = %s
    """, (hours_spent, contract_id))
    conn.commit()
    return f"Корт {court_number} забронирован на {booking_date} {start_time}"



"""Отметка посещаемости"""
def get_client_bookings(client_id):
    cursor.execute("""
        SELECT b.id_booking, b.booking_date, b.start_time, b.end_time, b.court_number, b.status
        FROM staging.booking b
        JOIN staging.contract c ON b.id_contract = c.id_contract
        WHERE c.id_client = %s
        ORDER BY b.booking_date DESC
    """, (client_id,))
    return cursor.fetchall()
def mark_attendance(booking_id):
    cursor.execute("SELECT status FROM staging.booking WHERE id_booking = %s", (booking_id,))
    status = cursor.fetchone()[0]
    if not status:
        raise ValueError("Такого бронирования не существует")
    cursor.execute("""
    UPDATE staging.booking
    SET status = 'completed'
    WHERE id_booking = %s""", (booking_id,))
    conn.commit()
    return "Посещение отмечено"