# Función para renombrar columnas en la base de datos (solo aplica a columnas específicas)
def rename_columns(column_mapping, table_name):
    with engine.connect() as connection:
        try:
            # Obtener las columnas actuales de la tabla
            result = connection.execute(text(f"""
                SELECT column_name
                FROM information_schema.columns
                WHERE table_name = '{table_name}'
            """))
            existing_columns = [row[0] for row in result]
            
            for old_name, new_name in column_mapping.items():
                if old_name.lower() in existing_columns:
                    operation = text(f"ALTER TABLE {table_name} RENAME COLUMN \"{old_name.lower()}\" TO \"{new_name}\";")
                    try:
                        connection.execute(operation)
                        print(f"Columna '{old_name}' renombrada a '{new_name}'.")
                    except ProgrammingError as e:
                        print(f"Error al renombrar columna '{old_name}': {e}")
                else:
                    print(f"La columna '{old_name}' no existe, omitiendo renombramiento.")
            print("3. Renombramiento de columnas: Completo")
        except Exception as e:
            logging.error(f"Error al renombrar columnas: {e}")
            raise
