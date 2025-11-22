import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
import urllib

server_name = 'Amatya\SQLEXPRESS'
database_name = 'MyDatabase'
driver = 'ODBC Driver 17 for SQL Server'

print("🔌 Connecting to SQL Server...")
params = urllib.parse.quote_plus(f"DRIVER={{{driver}}};SERVER={server_name};DATABASE={database_name};Trusted_Connection=yes")
engine = create_engine(f"mssql+pyodbc:///?odbc_connect={params}")

print("📊 Fetching Toxicology Data...")
query = "SELECT TestName, Value FROM Fact_Labs WHERE Value < 200"
df = pd.read_sql(query, engine)

print(f"Loaded {len(df)} rows of lab data.")

print("🎨 Generating Toxicity Report...")
plt.figure(figsize=(10, 6))
sns.set_theme(style="whitegrid")

sns.boxplot(x='TestName', y='Value', data=df, palette="Set2", showfliers=False)
sns.stripplot(x='TestName', y='Value', data=df, color='red', alpha=0.3, jitter=True)

plt.title('Automated Anomaly Detection: Liver (ALT) & Kidney (BUN) Markers', fontsize=16)
plt.ylabel('Concentration (IU/L or mg/dL)', fontsize=12)
plt.xlabel('Biomarker', fontsize=12)

output_file = 'Toxicity_Report.png'
plt.savefig(output_file)
print(f"✅ SUCCESS! Chart saved as: {output_file}")
plt.show()