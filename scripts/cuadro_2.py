import pandas as pd
from sqlalchemy import create_engine, text

# Configuración de la conexión
engine = create_engine('postgresql://postgres:postgres@localhost/encuesta_accesibilidad')

def cargar_datos():
    query = text("SELECT * FROM encuesta_con_vinculo")
    df = pd.read_sql_query(query, engine)
    return df

def cuadro_2(df):
    unidades_academicas = df['NOMBRE_FACULTAD'].value_counts().to_dict()
    resultados = {}
    for unidad in unidades_academicas:
        subconjunto = df[df['NOMBRE_FACULTAD'] == unidad]
        # Suponiendo que 'RespuestaConsentimiento' es 'SÍ' para respuestas completas
        respuestas_completas = sum((subconjunto['RespuestaConsentimiento'] == 'SÍ') & (subconjunto['DificultadesPermanentesRespondida'] == 1))
        respuestas_incompletas = unidades_academicas[unidad] - respuestas_completas
        # No respondientes serían aquellos que no están en el dataframe pero deberían estar (datos hipotéticos o de otra fuente)
        no_respondientes = 0  # Esto debería ser calculado con más datos, por ahora lo ponemos en 0
        
        resultados[unidad] = {
            'Respuestas general': unidades_academicas[unidad],
            'Respuestas completas': respuestas_completas,
            'Respuestas incompletas': respuestas_incompletas,
            'No respondientes': no_respondientes
        }
    
    # Convertir el diccionario en DataFrame
    df_resultados = pd.DataFrame.from_dict(resultados, orient='index')
    df_resultados.reset_index(inplace=True)
    df_resultados = df_resultados.rename(columns={'index': 'Unidad Académica'})
    
    return df_resultados

# Ejecutar la función para obtener los datos del cuadro
df = cargar_datos()
resultados_cuadro_2 = cuadro_2(df)

# Guardar los resultados en un CSV
resultados_cuadro_2.to_csv('outputs/20250109/cuadro_2.csv', index=False)

print("El CUADRO 2 ha sido generado y guardado en 'outputs/20250109/cuadro_2.csv'.")