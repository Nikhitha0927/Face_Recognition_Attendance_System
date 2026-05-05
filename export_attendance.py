from sqlalchemy import create_engine
import pandas as pd

engine = create_engine(
    "postgresql://postgres:your_password@localhost:5433/face_db"
)

query = "SELECT * FROM attendance ORDER BY date DESC"

df = pd.read_sql(query, engine)

df.to_excel("attendance.xlsx", index=False)

print("Attendance exported to attendance.xlsx")
