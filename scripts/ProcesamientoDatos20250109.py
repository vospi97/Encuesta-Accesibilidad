import pandas as pd
from sqlalchemy import create_engine, text

# Configuración de conexión usando SQLAlchemy
engine = create_engine('postgresql://postgres:postgres@localhost/encuesta_accesibilidad')

# Leer datos desde un archivo CSV (asegúrate de que el archivo CSV tenga las columnas correctas)
data = pd.read_csv('ArchivoRespuestasFinal-4.csv')

# Ajusta los nombres de las columnas para que coincidan con los de la tabla en la base de datos
# Esto es solo un ejemplo, ajusta según tu CSV
data.columns = ['Cedula', 'Orden1', 'Respuesta1', 'Orden2', 'Respuesta2', 'Orden3', 'Respuesta3', 'Orden4', 'Respuesta4_42', 'Respuesta4_44', 'Respuesta4_53', 'Respuesta4_58', 'Respuesta4_64', 'Orden5', 'Respuesta5', 'Orden6', 'Respuesta6_43', 'Respuesta6_45', 'Respuesta6_55', 'Respuesta6_3', 'Respuesta6_59', 'Respuesta6_60', 'Respuesta6_62', 'Respuesta6_67', 'Respuesta6_74', 'Respuesta6_75', 'Orden7', 'Respuesta7_46', 'Respuesta7_48', 'Respuesta7_48_Otro', 'Respuesta7_3', 'Respuesta7_60', 'Respuesta7_63', 'Respuesta7_66', 'Respuesta7_73', 'Orden8', 'Respuesta8_1', 'Respuesta8_49', 'Respuesta8_50', 'Respuesta8_51', 'Respuesta8_52', 'Respuesta8_54', 'Respuesta8_65', 'Respuesta8_68', 'Respuesta8_69', 'Respuesta8_70', 'Respuesta8_71', 'Respuesta8_72', 'Respuesta8_76', 'Orden9', 'Respuesta9_10', 'Respuesta9_10_Otro', 'Respuesta9_11', 'Respuesta9_11_Otro', 'Respuesta9_2', 'Respuesta9_2_Otro', 'Respuesta9_3', 'Respuesta9_3_Otro', 'Respuesta9_4', 'Respuesta9_4_Otro', 'Respuesta9_5', 'Respuesta9_5_Otro', 'Respuesta9_6', 'Respuesta9_6_Otro', 'Respuesta9_7', 'Respuesta9_7_Otro', 'Respuesta9_8', 'Respuesta9_8_Otro', 'Respuesta9_9', 'Respuesta9_9_Otro', 'Orden10', 'Respuesta10_12', 'Respuesta10_12_Otro', 'Respuesta10_13', 'Respuesta10_13_Otro', 'Respuesta10_14', 'Respuesta10_14_Otro', 'Respuesta10_15', 'Respuesta10_15_Otro', 'Respuesta10_16', 'Respuesta10_16_Otro', 'Respuesta10_17', 'Respuesta10_17_Otro', 'Respuesta10_18', 'Respuesta10_18_Otro', 'Respuesta10_19', 'Respuesta10_19_Otro', 'Respuesta10_20', 'Respuesta10_20_Otro', 'Respuesta10_21', 'Respuesta10_21_Otro', 'Respuesta10_22', 'Respuesta10_22_Otro', 'Orden11', 'Respuesta11_23', 'Respuesta11_23_Otro', 'Respuesta11_24', 'Respuesta11_24_Otro', 'Respuesta11_25', 'Respuesta11_25_Otro', 'Respuesta11_26', 'Respuesta11_26_Otro', 'Respuesta11_27', 'Respuesta11_27_Otro', 'Respuesta11_28', 'Respuesta11_28_Otro', 'Respuesta11_29', 'Respuesta11_29_Otro', 'Respuesta11_30', 'Respuesta11_30_Otro', 'Respuesta11_31', 'Respuesta11_31_Otro', 'Respuesta11_32', 'Respuesta11_32_Otro', 'Respuesta11_33', 'Respuesta11_33_Otro', 'Orden12', 'Respuesta12_34', 'Respuesta12_34_Otro', 'Respuesta12_35', 'Respuesta12_35_Otro', 'Respuesta12_36', 'Respuesta12_36_Otro', 'Respuesta12_37', 'Respuesta12_37_Otro', 'Respuesta12_38', 'Respuesta12_38_Otro', 'Respuesta12_39', 'Respuesta12_39_Otro', 'Respuesta12_40', 'Respuesta12_40_Otro', 'Respuesta12_41', 'Respuesta12_41_Otro', 'Orden13', 'Respuesta13', 'Orden14', 'Respuesta14', 'Orden15', 'Respuesta15_47', 'Orden16', 'Respuesta16', 'Orden19', 'Respuesta19', 'Orden20', 'Respuesta20']

# Insertar datos en la nueva tabla
data.to_sql('tabla_20250109', engine, if_exists='replace', index=False)

print("Datos cargados en 'tabla_20250109' en la base de datos.")

# Insertar datos en la nueva tabla
data.to_sql('tabla_20250109', engine, if_exists='replace', index=False)

print("Datos cargados en 'tabla_20250109' en la base de datos.")

# Renombrar columnas OrdenX a PreguntaXRespondida, solo si existen
with engine.connect() as connection:
    for i in range(1, 21):
        if i not in [17, 18]:  # Excluir Orden17 y Orden18 ya que no existen
            try:
                operation = text(f"ALTER TABLE tabla_20250109 RENAME COLUMN Orden{i} TO Pregunta{i}Respondida;")
                connection.execute(operation)
                print(f"Columna 'Orden{i}' renombrada a 'Pregunta{i}Respondida'.")
            except Exception as e:
                print(f"No se pudo renombrar 'Orden{i}': {str(e)}")

print("Proceso de renombramiento completado.")
print("Columnas 'OrdenX' renombradas a 'PreguntaXRespondida'.")