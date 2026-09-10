from datetime import datetime
from operations import (
    search_clients,
    register_client,
    create_contract,
    renew_contract,
    delete_contract,
    create_booking,
    mark_attendance,
    get_client_contracts,
    get_client_bookings,
)


def main():
    while True:
        print("\nМеню:")
        print("1 - Найти клиента")
        print("2 - Зарегистрировать клиента")
        print("3 - Оформить договор")
        print("4 - Продлить договор")
        print("5 - Удалить договор")
        print("6 - Создать бронирование")
        print("7 - Отметить посещение")
        print("0 - Выход")

        choice = input("Выберите пункт: ")

        # 1. Поиск клиента по части ФИО или телефону
        if choice == "1":
            term = input("Введите строку для поиска: ")
            results = search_clients(term)
            if not results:
                print("Ничего не найдено")
                continue
            for row in results:
                client_id, last_name, first_name, middle_name, phone, birth_date, reg_date = row
                print(f"{client_id} | {last_name} {first_name} {middle_name} | {phone} | "
                      f"род. {birth_date.strftime('%d.%m.%Y')} | рег. {reg_date.strftime('%d.%m.%Y')}")

        # 2. Регистрация нового клиента
        elif choice == "2":
            last_name = input("Фамилия: ")
            first_name = input("Имя: ")
            middle_name = input("Отчество: ")
            phone = input("Телефон: ")
            birth_date = datetime.strptime(input("Дата рождения (ГГГГ-ММ-ДД): "), "%Y-%m-%d").date()
            client_id = register_client(last_name, first_name, middle_name, phone, birth_date)
            print(f"Клиент создан с id = {client_id}")

        # 3. Оформление нового договора
        elif choice == "3":
            client_id = int(input("Введите id клиента: "))
            print("Виды абонементов:")
            print("1 - Разовое занятие")
            print("2 - Абонемент на 4 занятия")
            print("3 - Абонемент на 8 занятий")
            print("4 - Групповая тренировка")
            print("5 - Месячный безлимит")
            subscription_id = int(input("Введите id абонемента: "))
            start_date = datetime.strptime(input("Дата начала (ГГГГ-ММ-ДД): "), "%Y-%m-%d").date()
            contract_id = create_contract(client_id, subscription_id, start_date)
            print(f"Договор создан с id = {contract_id}")

        # 4. Продление активного договора
        elif choice == "4":
            client_id = int(input("Введите id клиента: "))
            contract_id = renew_contract(client_id)
            print(f"Договор продлён, новый id = {contract_id}")

        # 5. Удаление договора
        elif choice == "5":
            client_id = int(input("Введите id клиента: "))
            contracts = get_client_contracts(client_id)
            if not contracts:
                print("У клиента нет договоров")
                continue
            print("Договоры клиента:")
            for row in contracts:
                contract_id, sub_name, start, end, hours, status = row
                print(f"{contract_id} | {sub_name} | {start} — {end} | часов: {hours} | {status}")
            contract_id = int(input("Введите id договора для удаления: "))
            print(delete_contract(contract_id))

        # 6. Создание бронирования
        elif choice == "6":
            client_id = int(input("Введите id клиента: "))
            contracts = get_client_contracts(client_id)
            if not contracts:
                print("У клиента нет договоров")
                continue
            print("Договоры клиента:")
            for row in contracts:
                contract_id, sub_name, start, end, hours, status = row
                print(f"{contract_id} | {sub_name} | {start} — {end} | часов: {hours} | {status}")

            contract_id = int(input("Введите id договора: "))
            print("Сотрудники:")
            print("1 - администратор")
            print("2 - менеджер")
            employee_id = int(input("Введите id сотрудника: "))
            booking_date = datetime.strptime(input("Дата бронирования (ГГГГ-ММ-ДД): "), "%Y-%m-%d").date()
            start_time = datetime.strptime(input("Время начала (ЧЧ:ММ): "), "%H:%M").time()
            end_time = datetime.strptime(input("Время окончания (ЧЧ:ММ): "), "%H:%M").time()
            court_number = int(input("Номер корта: "))
            print(create_booking(contract_id, employee_id, booking_date, start_time, end_time, court_number))

        # 7. Отметка посещения по бронированию
        elif choice == "7":
            client_id = int(input("Введите id клиента: "))
            bookings = get_client_bookings(client_id)
            if not bookings:
                print("У клиента нет бронирований")
                continue
            print("Бронирования клиента:")
            for row in bookings:
                booking_id, bdate, stime, etime, court, status = row
                print(f"{booking_id} | {bdate} | {stime}–{etime} | корт {court} | {status}")
            booking_id = int(input("Введите id бронирования: "))
            print(mark_attendance(booking_id))

        # 0. Выход
        elif choice == "0":
            print("Выход")
            break

        else:
            print("Неизвестная команда")


if __name__ == '__main__':
    main()