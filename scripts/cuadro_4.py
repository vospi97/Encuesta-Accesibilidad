import pandas as pd
from io import StringIO
import re

# Crear un DataFrame desde el texto proporcionado
data = '''...'''  # He omitido pegar los datos para no repetir el contenido en la respuesta
df = pd.read_csv(StringIO(data), sep='\t', header=None)

# Crear un diccionario de mapeo para las columnas desde el primer registro
column_mapping = {}
for i, item in enumerate(df.iloc[0]):
    column_name = item.strip()
    if not column_name.startswith('Orden'):
        column_mapping[i] = column_name

# Renombrar las columnas basado en el mapeo
df = df.rename(columns=column_mapping)

# Eliminar la primera fila que ahora son los nombres de las columnas
df = df[1:]

# Convertir 'Cedula' a tipo numérico y establecer como índice
df['Cedula'] = pd.to_numeric(df['Cedula'], errors='coerce')
df = df.set_index('Cedula')

# Verificación de respuestas completas
df['Respuestas_Completas'] = (df['RespuestaConsentimiento'] == 'SÍ') & (df['DificultadesPermanentesRespondida'].notna())

# Función para contar respuestas
def count_responses(df, condition):
    total = len(df)
    completas = sum(condition)
    incompletas = total - completas
    return pd.Series({
        'Respuestas general': total,
        'Respuestas completas': completas,
        'Respuestas incompletas': incompletas
    })

# Listado de todas las categorías y subcategorías de discapacidad
discapacidades = [
    ('Discapacidad Visual', ['Persona Ciega', 'Persona con baja visión']),
    ('Discapacidad auditiva', [
        'Persona sorda profunda (usuaria de la LSC como primera lengua)', 
        'Persona sorda profunda (usuaria del español como primera lengua)', 
        'Persona con hipoacusia (usuaria de la LSC como primera lengua)', 
        'Persona con hipoacusia (usuaria del español como primera lengua)'
    ]),
    ('Discapacidad Física', [
        'Persona con compromiso en miembros superiores', 
        'Persona con compromiso en miembros inferiores', 
        'Personas con compromiso en miembros superiores e inferiores'
    ]),
    ('Discapacidad Talla Baja', ['Discapacidad Talla Baja']),
    ('Discapacidad Sordoceguera', ['Discapacidad Sordoceguera']),
    ('Discapacidad Intelectual', ['Discapacidad Intelectual']),
    ('Discapacidad Psicosocialmental', ['Discapacidad Psicosocialmental']),
    ('Discapacidad Múltiple', ['Discapacidad Múltiple'])
]

# Preparar el dataframe para los resultados
results = []

# Iterar sobre las categorías y subcategorías
for categoria, subcategorias in discapacidades:
    subtotals = []
    for subcategoria in subcategorias:
        if subcategoria in df.columns:  # Solo si la subcategoría existe en el dataframe
            sub_df = df[df[subcategoria] == 'SÍ']
            res = count_responses(sub_df, sub_df['Respuestas_Completas'])
            res['Subcategoria'] = subcategoria
            subtotals.append(res)
    
    # Agregar fila de total por subcategoría
    if subtotals:
        total_subcategoria = pd.concat(subtotals, axis=1).sum(axis=1)
        total_subcategoria['Subcategoria'] = 'Total subcategoría'
        subtotals.append(total_subcategoria)
    
    # Agregar fila de total por categoría
    if subtotals:
        categoria_total = pd.Series({
            'Respuestas general': sum([s['Respuestas general'] for s in subtotals]),
            'Respuestas completas': sum([s['Respuestas completas'] for s in subtotals]),
            'Respuestas incompletas': sum([s['Respuestas incompletas'] for s in subtotals]),
            'Subcategoria': 'Total categoría'
        })
        subtotals.append(categoria_total)

    # Añadir cada subcategoría y totales a la lista de resultados
    for row in subtotals:
        row['Nivel de desagregación'] = categoria
        results.append(row)

# Convertir la lista de resultados a un DataFrame
results_df = pd.DataFrame(results).set_index(['Nivel de desagregación', 'Subcategoria'])

# Reordenar las columnas para que sigan el formato especificado
results_df = results_df[['Respuestas general', 'Respuestas completas', 'Respuestas incompletas']]

# Guardar los resultados en un CSV
results_df.to_csv('outputs/20250109/cuadro_4.csv')

print("El CUADRO 4 ha sido generado y guardado en 'outputs/20250109/cuadro_4.csv'.")