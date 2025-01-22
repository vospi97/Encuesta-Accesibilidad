import pandas as pd
from sqlalchemy import create_engine, text

# Configuración de la conexión
engine = create_engine('postgresql://postgres:postgres@localhost/encuesta_accesibilidad')

def cuadro_3():
    # Consulta para obtener los datos necesarios
    query = text("""
    SELECT 
        encuesta_con_vinculo.Cedula AS Cedula,
        encuesta_con_vinculo."RespuestaConsentimiento" AS RespuestaConsentimiento,
        encuesta_con_vinculo."DificultadesPermanentesRespondida" AS DificultadesPermanentesRespondida,
        encuesta_con_vinculo."Campus Medellín - Ciudad universitaria" AS Campus_Medellin_Ciudad,
        encuesta_con_vinculo."Campus Apartadó" AS Campus_Apartado,
        encuesta_con_vinculo."Campus Turbo" AS Campus_Turbo,
        encuesta_con_vinculo."Campus Caucasia" AS Campus_Caucasia,
        encuesta_con_vinculo."Campus El Carmen de Viboral" AS Campus_Carmen_Viboral,
        encuesta_con_vinculo."Campus Santa Fe de Antioquia" AS Campus_Santa_Fe,
        encuesta_con_vinculo."Campus Yarumal" AS Campus_Yarumal,
        encuesta_con_vinculo."Campus Amalfi" AS Campus_Amalfi,
        encuesta_con_vinculo."Campus Segovia" AS Campus_Segovia,
        encuesta_con_vinculo."Campus Andes" AS Campus_Andes,
        encuesta_con_vinculo."Campus La Pintada" AS Campus_Pintada,
        encuesta_con_vinculo."Campus Sonsón" AS Campus_Sonson,
        encuesta_con_vinculo."Campus Puerto Berrío" AS Campus_Puerto_Berrio,
        encuesta_con_vinculo."Campus Medellín - Ciudadela Robledo" AS Campus_Robledo,
        encuesta_con_vinculo."Campus Medellín - Facultad de Medicina" AS Campus_Medicina,
        encuesta_con_vinculo."Campus Medellín - Edificio San Ignacio" AS Campus_San_Ignacio,
        encuesta_con_vinculo."Campus Medellín - SIU" AS Campus_SIU,
        encuesta_con_vinculo."Campus Medellín - Sede Posgrados" AS Campus_Posgrados
    FROM encuesta_con_vinculo
    """)

    # Cargar datos desde PostgreSQL
    df = pd.read_sql_query(query, engine)

    # Crear una columna 'Campus' combinando todas las columnas de campus
    campus_columns = [col for col in df.columns if col.startswith('Campus')]
    df['Campus'] = df[campus_columns].apply(lambda row: ', '.join([campus for campus in row if pd.notna(campus)]), axis=1)

    # Verificación de respuestas completas
    df['Respuestas_Completas'] = (df['RespuestaConsentimiento'] == 'SÍ') & (df['DificultadesPermanentesRespondida'] == 1)

    # Contar y agrupar por campus
    campus_counts = df.groupby('Campus').agg({
        'Cedula': 'count',  # Total de respuestas
        'Respuestas_Completas': 'sum'  # Respuestas completas
    }).reset_index()
    
    campus_counts['Respuestas incompletas'] = campus_counts['Cedula'] - campus_counts['Respuestas_Completas']
    campus_counts = campus_counts.rename(columns={
        'Cedula': 'Respuestas general',
        'Respuestas_Completas': 'Respuestas completas'
    })

    # Ordenar por nombre de campus
    campus_counts = campus_counts.sort_values('Campus')

    # Renombrar la columna 'Campus' a 'Nivel de desagregación'
    campus_counts = campus_counts.rename(columns={'Campus': 'Nivel de desagregación'})

    return campus_counts

# Generar el CUADRO 3
resultados_cuadro_3 = cuadro_3()

# Guardar los resultados en un CSV
resultados_cuadro_3.to_csv('outputs/20250109/cuadro_3.csv', index=False)

print("El CUADRO 3 ha sido generado y guardado en 'outputs/20250109/cuadro_3.csv'.")