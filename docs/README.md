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

## Ejecución
```bash
python scripts/NombreColumnas2.py