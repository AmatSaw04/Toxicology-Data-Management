import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
import urllib

# --- CONNECT ---
server_name = 'Amatya\SQLEXPRESS'
database_name = 'MyDatabase'
driver = 'ODBC Driver 17 for SQL Server'
params = urllib.parse.quote_plus(f"DRIVER={{{driver}}};SERVER={server_name};DATABASE={database_name};Trusted_Connection=yes")
engine = create_engine(f"mssql+pyodbc:///?odbc_connect={params}")

# --- FETCH DATA ---
print("📊 Fetching Weight Data...")
query = """
SELECT 
    A.Sex,
    W.Day,
    W.Weight_g
FROM Dim_Animal A
JOIN Fact_BodyWeights W ON A.AnimalID = W.AnimalID
WHERE W.Day <= 29 -- Focus on first month for clarity
"""
df = pd.read_sql(query, engine)

print("🎨 Generating Growth Trends...")
plt.figure(figsize=(12, 7))
sns.set_theme(style="darkgrid")


sns.lineplot(data=df, x='Day', y='Weight_g', hue='Sex', style='Sex', markers=True, dashes=False, palette="deep")

plt.title('In-Vivo Body Weight Trajectory (Growth Analysis)', fontsize=16)
plt.ylabel('Body Weight (g)', fontsize=12)
plt.xlabel('Study Day', fontsize=12)
plt.legend(title='Subject Sex')
plt.savefig('Growth_Trends.png')
print("✅ Saved: Growth_Trends.png")
plt.show()