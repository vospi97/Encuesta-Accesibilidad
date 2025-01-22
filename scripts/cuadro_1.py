import pandas as pd
from sqlalchemy import create_engine, text

# Configuración de la conexión
engine = create_engine('postgresql://postgres:postgres@localhost/encuesta_accesibilidad')

def cargar_datos():
    query = text("SELECT * FROM encuesta_con_vinculo")
    df = pd.read_sql_query(query, engine)
    return df

# Cargar datos
df = cargar_datos()

def cuadro_1(df):
    # Población total es la cantidad total de respondientes
    poblacion_total = len(df['Cedula'].unique())
    
    # Respuestas completas son las respuestas que aceptaron la política de tratamiento de datos
    respuestas_completas = sum(df['RespuestaConsentimiento'] == 'SÍ')
    
    # Respuestas incompletas es el complemento de respuestas completas
    respuestas_incompletas = len(df) - respuestas_completas
    
    # Aquí también verificamos si se respondió la pregunta 4 (DificultadesPermanentesRespondida)
    respuestas_completas_con_preg4 = sum((df['RespuestaConsentimiento'] == 'SÍ') & (df['DificultadesPermanentesRespondida'] == 1))
    
    # Respuestas generales son todas las respuestas recibidas
    respuestas_generales = len(df)
    
    # No respuestas es el complemento de respuestas generales sobre la población total
    no_respuestas = poblacion_total - respuestas_generales
    
    # Tasa de respuesta es cantidad de respuesta general sobre población total
    tasa_respuesta = (respuestas_generales / poblacion_total) * 100 if poblacion_total > 0 else 0
    
    # Tasa de no respuesta es el complemento de respuesta general sobre población total
    tasa_no_respuesta = 100 - tasa_respuesta if tasa_respuesta != 0 else 0
    
    # Tasa de respuesta completa es el total de respuesta completa sobre población total
    tasa_respuesta_completa = (respuestas_completas_con_preg4 / poblacion_total) * 100 if poblacion_total > 0 else 0

    return {
        'Población total': poblacion_total,
        'Respuestas General': respuestas_generales,
        'Respuestas Completas': respuestas_completas_con_preg4,
        'Respuestas Incompletas': respuestas_incompletas,
        'No Respuestas': no_respuestas,
        'Tasa de respuesta': f"{tasa_respuesta:.2f}%",
        'Tasa de no respuesta': f"{tasa_no_respuesta:.2f}%",
        'Tasa de respuesta completa': f"{tasa_respuesta_completa:.2f}%"
    }

# Ejecución de la función
datos_cuadro_1 = cuadro_1(df)

# Guardar resultados en CSV o mostrarlos
pd.DataFrame([datos_cuadro_1]).to_csv('outputs/20250109/cuadro_1.csv', index=False)

print("Datos para CUADRO 1 generados y guardados.")