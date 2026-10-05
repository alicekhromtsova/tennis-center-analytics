import pandas as pd
from sqlalchemy import create_engine

engine = create_engine('postgresql+psycopg2://postgres:7255@localhost/tennis_center')
df_client = pd.read_sql('select * from staging.client', engine)
df_booking = pd.read_sql('select * from staging.booking', engine)

# Сводные метрики
summary = pd.DataFrame({
    "metric": ["clients_count", "bookings_count"],
    "value": [len(df_client), len(df_booking)]
})
summary.to_csv("report.csv", index=False)

#Загруженность кортов
court_load = df_booking.groupby("court_number")["id_booking"].count().reset_index()
court_load.columns = ["court_number", "booking_count"]
court_load = court_load.sort_values("booking_count", ascending=False)
court_load.to_csv("court_load.csv", index=False)

#Процент отмен по кортам
cancel_stats = df_booking.pivot_table(values="id_booking", index="court_number", columns="status", aggfunc="count")
cancel_stats["total"] = cancel_stats.sum(axis=1)
cancel_stats["cancel_rate"] = cancel_stats["canceled"] / cancel_stats["total"] * 100
cancel_stats.to_csv("cancel_stats.csv")

print("Отчёты сохранены")