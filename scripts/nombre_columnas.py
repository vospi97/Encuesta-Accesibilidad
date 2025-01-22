import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.exc import ProgrammingError
import re

# Configuración de conexión usando SQLAlchemy
engine = create_engine('postgresql://postgres:postgres@localhost/encuesta_accesibilidad')

# Lectura del archivo CSV de respuestas de la encuesta previa limpieza de datos
# utilizando node.js
data = pd.read_csv('data/20250109/ArchivoRespuestasFinal-4.csv')

# Ajusta los nombres de las columnas para que coincidan con los de la tabla en la base de datos
column_mapping = {
    'Cedula': 'Cedula',
    'Orden1': 'MayorDeEdadRespondida',
    'Respuesta1': 'RespuestaMayorDeEdad',
    'Orden2': 'AutorizacionMenorRespondida',
    'Respuesta2': 'AutorizacionMenor',
    'Orden3': 'ConsentimientoInformadoRespondida',
    'Respuesta3': 'RespuestaConsentimiento',
    'Orden4': 'DificultadesPermanentesRespondida',
    'Respuesta4_42': 'DificultadVerCercaLejos',
    'Respuesta4_44': 'DificultadOir',
    'Respuesta4_53': 'DificultadMovilidad',
    'Respuesta4_58': 'DificultadCognitiva',
    'Respuesta4_64': 'DificultadInteraccionSocial',
    # Aquí agregarías el resto de mapeos, pero solo hasta Orden4 por ahora
}
# Aplicamos el mapeo y convertimos a minúsculas para evitar problemas de mayúsculas/minúsculas
data.columns = [column_mapping.get(col, col).lower() for col in data.columns]

# Cambia los valores en las columnas de Orden (aunque solo se mencionaron hasta Orden4)
for col in data.columns:
    if re.match(r'^orden\d+$', col):  # Comprueba si la columna es 'orden' seguido por un número
        data[col] = data[col].apply(lambda x: 1 if pd.notna(x) and x != '' else 0)

# Insertar datos en la nueva tabla
try:
    data.to_sql('tabla_20250109', engine, if_exists='replace', index=False)
    print("Datos cargados y tabla creada o actualizada en 'tabla_20250109' en la base de datos.")
except Exception as e:
    print(f"Error al cargar datos en la tabla: {e}")

# Renombrar columnas restantes que no se mapearon por el script de inserción
with engine.connect() as connection:
    try:
        for old_name, new_name in column_mapping.items():
            if old_name.lower().startswith('orden'):  # Solo renombramos columnas que comienzan con Orden
                operation = text(f"ALTER TABLE tabla_20250109 RENAME COLUMN {old_name.lower()} TO {new_name.lower()};")
                try:
                    connection.execute(operation)
                    print(f"Columna '{old_name}' renombrada a '{new_name}'.")
                except ProgrammingError as e:
                    if 'does not exist' in str(e):
                        print(f"La columna '{old_name}' no existe, no se pudo renombrar.")
                    else:
                        raise
    except Exception as e:
        print(f"Error en el proceso de renombramiento: {e}")

def verify_columns(connection):
    result = connection.execute(text("""
        SELECT column_name 
        FROM information_schema.columns 
        WHERE table_name = 'tabla_20250109'
    """))
    existing_columns = [row[0] for row in result]
    expected_columns = list(column_mapping.values())
    missing_columns = set([col.lower() for col in expected_columns]) - set(existing_columns)
    extra_columns = set(existing_columns) - set([col.lower() for col in expected_columns])

    if missing_columns:
        print(f"Columnas esperadas pero no encontradas: {', '.join(missing_columns)}")
    if extra_columns:
        print(f"Columnas adicionales no esperadas: {', '.join(extra_columns)}")

with engine.connect() as connection:
    verify_columns(connection)

print("Proceso de renombramiento y verificación completado.")