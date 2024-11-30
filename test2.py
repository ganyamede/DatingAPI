from sqlalchemy import create_engine
import pandas as pd

# Подключение к PostgreSQL
engine = create_engine('postgresql://getapple:010203@localhost/getapple')

# Экспорт таблицы в CSV
query = "SELECT * FROM Profiles"
df = pd.read_sql(query, engine)
df.to_csv("table_export.csv", index=False)
