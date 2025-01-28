import pandas as pd
from sqlalchemy import create_engine

# Crear una conexión a la base de datos PostgreSQL
engine = create_engine('postgresql://postgres:postgres@localhost/encuesta_accesibilidad')

# Leer los archivos CSV de empleados y estudiantes
empleados_path = 'data/20250109/empleados_encuestados.csv'
estudiantes_path = 'data/20250109/estudiantes_encuestados.csv'

empleados = pd.read_csv(empleados_path)
estudiantes = pd.read_csv(estudiantes_path)

# Renombrar la columna de CEDULA para que sea consistente en el merge
empleados = empleados.rename(columns={'CEDULA_EMPLEADO': 'Cedula'})
estudiantes = estudiantes.rename(columns={'CEDULA': 'Cedula'})

# Crear un DataFrame para empleados (incluyendo clasificación de docentes)
empleados['Es_Docente'] = empleados['ESTAMENTO'].isin(['DOCEN', 'DOCAT'])  # Identificar docentes
empleados['Es_Empleado'] = ~empleados['Es_Docente']  # Si no es docente, es empleado
empleados = empleados[['Cedula', 'ESTAMENTO', 'Es_Empleado', 'Es_Docente']]

# Crear un DataFrame para estudiantes
estudiantes['Es_Estudiante'] = True
estudiantes = estudiantes[['Cedula', 'NOMBRE_FACULTAD', 'Es_Estudiante']]

# Concatenar empleados (docentes y no docentes) con estudiantes
# Cada persona tendrá una categoría única: docente, empleado o estudiante
vinculo_universitario = pd.concat([
    empleados[['Cedula', 'Es_Empleado', 'Es_Docente']].assign(Es_Estudiante=False),
    estudiantes[['Cedula', 'Es_Estudiante']].assign(Es_Empleado=False, Es_Docente=False)
], ignore_index=True)

# Asegurarse de que no haya duplicados
vinculo_universitario = vinculo_universitario.drop_duplicates(subset='Cedula')

# Leer los datos de la encuesta desde la base de datos PostgreSQL
encuesta_query = "SELECT * FROM tabla_20250109"
encuesta = pd.read_sql_query(encuesta_query, engine)

# Unir los datos de la encuesta con la información de vínculo universitario
encuesta_con_vinculo = pd.merge(encuesta, vinculo_universitario, on='Cedula', how='left')

# Guardar el DataFrame combinado como CSV
output_path = 'data/20250109/encuesta_con_vinculo.csv'
encuesta_con_vinculo.to_csv(output_path, index=False)

# Verificación de resultados
print(encuesta_con_vinculo.head())
print(f"Total de registros en la encuesta después de la unión: {len(encuesta_con_vinculo)}")
