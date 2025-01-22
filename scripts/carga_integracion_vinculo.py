import pandas as pd
from sqlalchemy import create_engine, text

# Configuración de la conexión a PostgreSQL
engine = create_engine('postgresql://postgres:postgres@localhost/encuesta_accesibilidad')

# Cargar el CSV en un DataFrame
df = pd.read_csv('data/20250109/encuesta_con_vinculo.csv')

# Cargar el DataFrame en PostgreSQL
try:
    df.to_sql('encuesta_con_vinculo', engine, if_exists='replace', index=False)
    print("Datos cargados exitosamente en la tabla 'encuesta_con_vinculo'.")
except Exception as e:
    print(f"Error al cargar los datos en PostgreSQL: {e}")

# Verificación
with engine.connect() as connection:
    # Usamos text() para hacer la consulta como texto SQL
    result = connection.execute(text("SELECT COUNT(*) FROM encuesta_con_vinculo"))
    count = result.scalar()
    print(f"Número de registros en la tabla: {count}")


