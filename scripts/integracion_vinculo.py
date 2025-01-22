import pandas as pd
from sqlalchemy import create_engine

engine = create_engine('postgresql://postgres:postgres@localhost/encuesta_accesibilidad')

# Leer los archivos CSV de empleados y estudiantes
empleados = pd.read_csv('data/20250109/empleados_encuestados.csv')
estudiantes = pd.read_csv('data/20250109/estudiantes_encuestados.csv')

# Renombrar la columna de CEDULA para que sea consistente en el merge
empleados = empleados.rename(columns={'CEDULA_EMPLEADO': 'Cedula'})
estudiantes = estudiantes.rename(columns={'CEDULA': 'Cedula'})  # Ajustado para estudiantes

# Crear un DataFrame que combine empleados y estudiantes basado en la cédula
vinculo_universitario = pd.concat([
    empleados[['Cedula', 'ESTAMENTO']].assign(Es_Empleado=True, Es_Estudiante=False, Es_Docente=False),
    estudiantes[['Cedula', 'NOMBRE_FACULTAD']].assign(Es_Empleado=False, Es_Estudiante=True, Es_Docente=False)
])

# Asegurarse de que no haya duplicados
vinculo_universitario = vinculo_universitario.drop_duplicates(subset='Cedula')

# Leer los datos de la encuesta desde PostgreSQL usando pgAdmin4
encuesta = pd.read_sql_query("SELECT * FROM tabla_20250109", engine)

# Unir los datos de la encuesta con la información de vínculo universitario
encuesta_con_vinculo = pd.merge(encuesta, vinculo_universitario, on='Cedula', how='left')

# Guardar el DataFrame combinado
encuesta_con_vinculo.to_csv('data/20250109/encuesta_con_vinculo.csv', index=False)

# Verificación
print(encuesta_con_vinculo.head())
print(f"Total de registros después de la unión: {len(encuesta_con_vinculo)}")