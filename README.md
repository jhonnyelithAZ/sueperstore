# 📊 Data Analytics Pipeline: Superstore Sales ETL & BI Dashboard

## 📝 Project Overview
This project is an end-to-end Data Engineering and Data Analytics test. It demonstrates the ability to build a complete data pipeline: extracting raw sales data, cleaning and transforming it using Python, loading it into a relational database using a Star Schema, and finally, generating business insights through an interactive Power BI dashboard.

## 🛠️ Tech Stack
* **Language:** Python 3.x
* **Data Processing:** Pandas
* **Database:** PostgreSQL
* **Database Connector:** SQLAlchemy & Psycopg2
* **Data Visualization:** Power BI

## 📂 Dataset
* **Source:** [Superstore Sales Dataset (Kaggle)](https://www.kaggle.com/datasets/vivek468/superstore-dataset-final)
* **Description:** Retail sales data containing roughly 10,000 rows and 21 columns, including temporal, categorical, and numerical variables.

## ⚙️ Pipeline Architecture (ETL)
The pipeline is divided into 4 main stages:

1. **Extract:** Raw CSV file downloaded from Kaggle is loaded into a Pandas DataFrame.
2. **Transform:** 
   * Normalization of column names (snake_case).
   * Data type corrections (Date parsing).
   * Handling of missing values and removal of duplicates.
   * Creation of derived columns (`mes_venta` and `categoria_precio`).
   * Quality checks (Asserts) to ensure zero nulls/duplicates post-cleaning.
3. **Load:** Data is pushed to a local **PostgreSQL** database. To optimize querying, the data is modeled into a **Star Schema** with one fact table (`fact_ventas`) and two dimension tables (`dim_clientes`, `dim_productos`).
4. **Consume:** Power BI connects directly to the PostgreSQL database to visualize the data.

## 📈 Business Questions Answered (Power BI)
The dashboard addresses 5 key business questions:
1. **Time Trend:** How have sales evolved over the months and years? *(Line Chart)*
2. **Top Categories:** What are the Top 5 sub-categories generating the most revenue? *(Bar Chart)*
3. **Distribution:** How is profit distributed across different regions? *(Pie/Donut Chart)*
4. **Period Comparison:** What is the sales variation compared to the previous year? *(Clustered Column Chart)*
5. **Variable Relationship:** Is there a correlation between discounts given and profits? *(Scatter Plot)*

## 🚀 How to Run the Project
1. **Clone the repository** and ensure you have the `superstore-dataset-final.csv` file in the root folder.
2. **Install dependencies:**
   `pip install pandas sqlalchemy psycopg2-binary`
3. **Database Setup:** Create a new empty database in PostgreSQL named `prueba_analitica`.
4. **Run the ETL Script:** Execute the Jupyter Notebook or `.py` file to clean the data and populate your database.
5. **Open Dashboard:** Open the `.pbix` file with Power BI Desktop to view the interactive visualizations.

## 📬 Contact
* **GitHub:** [jhonnyelithAZ](https://github.com/jhonnyelithAZ)
* **Email:** [jhonatanayala3478@gmail.com](mailto:jhonatanayala3478@gmail.com)
* **Phone:** 3004606002
  