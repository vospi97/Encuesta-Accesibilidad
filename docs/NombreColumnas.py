import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.exc import ProgrammingError
import logging
import re

# Configuración de conexión usando SQLAlchemy
engine = create_engine('postgresql://postgres:postgres@localhost/encuesta_accesibilidad')

# Configuración de logging para manejar errores
logging.basicConfig(filename='error_log.txt', level=logging.ERROR, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Función para normalizar los nombres de las columnas
def normalize_column_names(columns):
    return [col.lower().strip().replace(" ", "_") for col in columns]

# Función para leer y transformar datos
def read_and_transform_data(csv_file, column_mapping):
    try:
        # Leer datos desde un archivo CSV
        data = pd.read_csv(csv_file)
        # Normalizar nombres de columnas
        data.columns = [column_mapping.get(col, col).lower() for col in data.columns]
        # Transformar columnas tipo 'Orden'
        for col in data.columns:
            if re.match(r'^orden\d+$', col):  # Verifica si la columna es 'ordenX'
                data[col] = data[col].apply(lambda x: 1 if pd.notna(x) and x != '' else 0)
        print("1. Lectura y transformación de datos: Completo")
        return data
    except Exception as e:
        logging.error(f"Error al leer y transformar datos: {e}")
        raise

# Función para hacer una copia de seguridad de la tabla existente
def backup_table(original_table_name, backup_table_name):
    with engine.connect() as connection:
        try:
            connection.execute(text(f"CREATE TABLE {backup_table_name} AS TABLE {original_table_name};"))
            print(f"Tabla '{original_table_name}' copiada a '{backup_table_name}'.")
        except Exception as e:
            logging.error(f"Error al crear la copia de la tabla: {e}")
            raise

# Función para cargar los datos en la base de datos
def load_data_to_db(data, table_name):
    try:
        data.to_sql(table_name, engine, if_exists='replace', index=False)
        print(f"2. Datos cargados en la tabla '{table_name}' en la base de datos.")
    except Exception as e:
        logging.error(f"Error al cargar datos en la tabla '{table_name}': {e}")
        raise

# Función para renombrar columnas en la base de datos
def rename_columns(column_mapping, table_name):
    with engine.connect() as connection:
        try:
            for old_name, new_name in column_mapping.items():
                operation = text(f"ALTER TABLE {table_name} RENAME COLUMN \"{old_name.lower()}\" TO \"{new_name.lower()}\";")
                try:
                    connection.execute(operation)
                    print(f"Columna '{old_name}' renombrada a '{new_name}'.")
                except ProgrammingError as e:
                    if 'does not exist' in str(e):
                        print(f"La columna '{old_name}' no existe, no se renombró.")
                    else:
                        raise
            print("3. Renombramiento de columnas: Completo")
        except Exception as e:
            logging.error(f"Error al renombrar columnas: {e}")
            raise

# Flujo principal
if __name__ == "__main__":
    # Archivo CSV
    csv_file = 'data/20250109/ArchivoRespuestasFinal-4.csv'
    table_name = 'tabla_20250109'
    backup_table_name = f'{table_name}_backup'

    # Mapeo de columnas
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
    }

    try:
        # Leer y transformar los datos
        data = read_and_transform_data(csv_file, column_mapping)

        # Hacer una copia de seguridad de la tabla existente
        backup_table(table_name, backup_table_name)

        # Cargar datos en la tabla
        load_data_to_db(data, table_name)

        # Renombrar columnas
        rename_columns(column_mapping, table_name)

        print("Proceso completado con éxito.")
    except Exception as e:
        print(f"Se produjo un error: {e}")
