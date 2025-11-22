Toxicology Data Management 

Project Overview
This project simulates a **Biomedical Data Management workflow**. It is an end-to-end ELT (Extract, Load, Transform) pipeline designed to ingest raw nonclinical safety assessment data, validate it against business rules, and generate regulatory-ready reports.

Goal: To transform messy, disparate CSV files from the Open TG-GATEs database into a clean, relational Star Schema in MS SQL Server for safety signal detection.

## Key Features
Automated Ingestion: Python script capable of bulk-loading 120,000+ records from multiple raw files, handling  encoding (Shift-JIS) and format inconsistencies.
Advanced Data Cleaning (SQL): Stored Procedures utilize Window Functions (`ROW_NUMBER`) to programmatically remove duplicate animal IDs and `TRY_CAST` logic to prevent pipeline failures on garbage data.
Relational Data Modeling: Architected a Star Schema (`Fact_BodyWeights`, `Fact_Labs`, `Dim_Animal`) to optimize query performance and data integrity.

## Tech Stack
* **Languages:** Python 3.10+, SQL (T-SQL)
* **Database:** Microsoft SQL Server 2022 (Express)
* **Libraries:** `pandas`, `sqlalchemy`, `pyodbc`, `seaborn`, `matplotlib`

