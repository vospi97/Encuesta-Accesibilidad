# Proyecto de Accesibilidad - Universidad de Antioquia

## Objetivo
Analizar las respuestas de la encuesta Data Accesibilidad UdeA.

## Estructura del Proyecto
- **data**: Datos de la encuesta organizados por fecha.
- **docs**: Documentación del proyecto.
- **outputs**: Resultados y visualizaciones.
- **scripts**: Scripts de procesamiento de datos.
- **venv**: Entorno virtual de Python.
- **requirements.txt**: Dependencias del proyecto.

## Scripts Principales
- `NombreColumnas2.py`: Maneja la carga, transformación, y almacenamiento de datos en PostgreSQL.

## Proceso
- Carga de datos desde CSV.
- Renombramiento de columnas para mayor claridad.
- Transformación de valores.

## Documentación Adicional
- Ver `docs/decisions.txt` para decisiones y detalles de implementación.

## Datos y Estructura

- **Encuestas de Accesibilidad:** Almacenadas en `data/20250109/ArchivoRespuestasFinal-4.csv` y procesadas en la tabla `tabla_20250109` en PostgreSQL.
- **Datos de Vinculación:** 
  - `data/20250109/empleados_encuestados.csv`
  - `data/20250109/estudiantes_encuestados.csv`
  - Estos datos se han unido con la encuesta en la tabla `encuesta_con_vinculo` en PostgreSQL.

  ## Scripts Usados

- `scripts/procesamiento_encuesta_accesibilidad.py` - Procesa y carga datos de encuestas en PostgreSQL.
- `scripts/carga_integracion_vinculo.py` - Integra datos de empleados y estudiantes con la encuesta, luego carga el resultado en PostgreSQL.

