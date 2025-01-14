import pandas as pd
from sqlalchemy import create_engine
import seaborn as sns
import matplotlib
matplotlib.use('TkAgg')  # Backend interactivo (para mostrar el gráfico)
import matplotlib.pyplot as plt


# Configuración de conexión usando SQLAlchemy
engine = create_engine('postgresql://postgres:postgres@localhost/encuesta_accesibilidad')

# Leer datos desde PostgreSQL
query = "SELECT * FROM respuestas_accesibilidad;"
data = pd.read_sql_query(query, engine)

# Mostrar las primeras filas
# print(data.head())

# Contar las respuestas en una columna específica
conteo_respuestas = data['respuesta5_2'].value_counts()

# Gráfico de barras para respuesta5_2
plt.figure(figsize=(10, 6))
sns.barplot(x=conteo_respuestas.index, y=conteo_respuestas.values)
plt.title("Distribución de Respuestas en respuesta5_2")
plt.xlabel("Tipo de Respuesta")
plt.ylabel("Número de Respuestas")
plt.xticks(rotation=45)

plt.savefig("grafico_ejemplo.png")
print("Gráfico guardado como 'grafico_ejemplo.png'")

plt.show() # Debe quedar después de guardar el gráfico

