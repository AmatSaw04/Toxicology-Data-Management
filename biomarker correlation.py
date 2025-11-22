import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
import urllib

server_name = 'Amatya\SQLEXPRESS'
database_name = 'MyDatabase'
driver = 'ODBC Driver 17 for SQL Server'
params = urllib.parse.quote_plus(f"DRIVER={{{driver}}};SERVER={server_name};DATABASE={database_name};Trusted_Connection=yes")
engine = create_engine(f"mssql+pyodbc:///?odbc_connect={params}")

print("📊 Fetching Lab Data...")
query = "SELECT AnimalID, TestName, Value FROM Fact_Labs"
df = pd.read_sql(query, engine)

# Turn rows into columns
df_pivot = df.pivot_table(index='AnimalID', columns='TestName', values='Value')
print("🎨 Generating Correlation Matrix...")
plt.figure(figsize=(10, 8))

corr = df_pivot.corr()

sns.heatmap(corr, annot=True, cmap='coolwarm', fmt=".2f", linewidths=.5)

plt.title('Biomarker Correlation Matrix (Organ System Interdependency)', fontsize=16)
plt.tight_layout()

plt.savefig('Correlation_Heatmap.png')
print("✅ Saved: Correlation_Heatmap.png")
plt.show()