import pandas as pd
from sqlalchemy import create_engine

# --- 1. EXTRACT ---#
df = pd.read_csv('superstore-dataset.csv', encoding='latin1')
print(" Extraction complete.")

# --- 2. TRANSFORM ---
# Normalize column names for SQL (lowercase, replace spaces with underscores)
df.columns = df.columns.str.lower().str.replace(' ', '_')

# Convert string dates to datetime objects
df['order_date'] = pd.to_datetime(df['order_date'])
df['ship_date'] = pd.to_datetime(df['ship_date'])

# Remove duplicate rows and any rows missing critical IDs
df = df.drop_duplicates()
df = df.dropna(subset=['order_id', 'customer_id'])

# Create derived columns
df['mes_venta'] = df['order_date'].dt.month
df['categoria_precio'] = df['sales'].apply(lambda x: 'Alto' if x > 100 else 'Bajo')

print("✅ Transformation complete.")

# --- 3. QUALITY VALIDATIONS ---
# Assertions stop the script if data quality fails
assert df.isnull().sum().sum() == 0, " Error: Null values found."
assert df.duplicated().sum() == 0, " Error: Duplicate rows exist."
assert df[df['sales'] < 0].shape[0] == 0, " Error: Negative sales found."

print("✅ Quality checks passed.")

# --- 4. LOAD (PostgreSQL) ---

engine = create_engine('postgresql://postgres:jeas-888@localhost:5433/superstore')

# Create Star Schema: Extract unique values and load to database

# Dimension 1: Customers
dim_clientes = df[['customer_id', 'customer_name', 'segment', 'region']].drop_duplicates(subset=['customer_id'])
dim_clientes.to_sql('dim_clientes', engine, if_exists='replace', index=False)

# Dimension 2: Products
dim_productos = df[['product_id', 'category', 'sub-category', 'product_name']].drop_duplicates(subset=['product_id'])
dim_productos.to_sql('dim_productos', engine, if_exists='replace', index=False)

# --- TIME DIMENSION GENERATION ---

# 1. range 
fecha_inicio = '2014-01-01'
fecha_fin = '2018-12-31'

df_tiempo = pd.DataFrame({'fecha': pd.date_range(start=fecha_inicio, end=fecha_fin)})

# 2. Extract Attributes
df_tiempo['id_tiempo'] = df_tiempo['fecha'].dt.strftime('%Y%m%d').astype(int) 
df_tiempo['ano'] = df_tiempo['fecha'].dt.year
df_tiempo['mes'] = df_tiempo['fecha'].dt.month
df_tiempo['trimestre'] = df_tiempo['fecha'].dt.quarter
df_tiempo['dia'] = df_tiempo['fecha'].dt.day
df_tiempo['dia_semana'] = df_tiempo['fecha'].dt.dayofweek + 1

meses = {1: 'Enero', 2: 'Febrero', 3: 'Marzo', 4: 'Abril', 5: 'Mayo', 6: 'Junio', 
         7: 'Julio', 8: 'Agosto', 9: 'Septiembre', 10: 'Octubre', 11: 'Noviembre', 12: 'Diciembre'}
dias = {0: 'Lunes', 1: 'Martes', 2: 'Miércoles', 3: 'Jueves', 4: 'Viernes', 5: 'Sábado', 6: 'Domingo'}

df_tiempo['nombre_mes'] = df_tiempo['mes'].map(meses)
df_tiempo['nombre_dia'] = (df_tiempo['fecha'].dt.dayofweek).map(dias)

# Reorder the columns
df_tiempo = df_tiempo[['id_tiempo', 'fecha', 'ano', 'mes', 'nombre_mes', 'trimestre', 'dia', 'dia_semana', 'nombre_dia']]


df_tiempo.to_sql('dim_tiempo', engine, if_exists='replace', index=False)
# Fact Table: Sales (Transactional data & metrics)
fact_ventas = df[['order_id', 'customer_id', 'product_id', 'order_date', 'sales', 'quantity', 'profit', 'discount']]
fact_ventas.to_sql('fact_ventas', engine, if_exists='replace', index=False)

print(" SUCCESS: ETL pipeline finished and loaded into Star Schema.")