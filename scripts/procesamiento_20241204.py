# Análisis de datos
import pandas as pd
import psycopg2
import matplotlib.pyplot as plt
import seaborn as sns

# Configuración de conexión
conn = psycopg2.connect(
    host= "localhost",
    database= "encuesta_accesibilidad",
    user= "postgres",
    password= "postgres"

)

# Leer datos desde PostgreSQL
query = "SELECT * FROM respuestas_accesibilidad;"
data = pd.read_sql_query(query, conn)

conn.close()

# Mostrar las primeras filas para verificar
# print(data.head())


# Contar las respuestas en una columna específica
conteo_respuestas = data['respuesta5_2'].value_counts()

# Mostrar el conteo
# print("Conteo de respuestas en respuesta5_2:")
# print(conteo_respuestas)

# Gráfico de barras para respuesta5_2
plt.figure(figsize=(10, 6))
sns.barplot(x=conteo_respuestas.index, y=conteo_respuestas.values)
plt.title("Distribución de Respuestas en respuesta5_2")
plt.xlabel("Tipo de Respuesta")
plt.ylabel("Número de Respuestas")
plt.xticks(rotation=45)
plt.show()