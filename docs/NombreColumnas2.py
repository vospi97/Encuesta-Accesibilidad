import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.exc import ProgrammingError
import re

# Configuración de conexión usando SQLAlchemy
engine = create_engine('postgresql://postgres:postgres@localhost/encuesta_accesibilidad')

# Leer datos desde un archivo CSV
data = pd.read_csv('data/20250109/ArchivoRespuestasFinal-4.csv')

# Ajusta los nombres de las columnas para que coincidan con los de la tabla en la base de datos
column_mapping = {
    'Cedula': 'Cedula',
    'Orden1': 'MayorDeEdadRespondida',
    'Respuesta1': 'RespuestaMayorDeEdad',
    'Orden2': 'AutorizacionMenorRespondida',
    'Respuesta2': 'AutorizacionMenor',
    'Orden3': 'ConsentimientoInformadoRespondida',
    'Respuesta3': 'RespuestaConsentimiento',
    'Orden4': 'DificultadesPermanentesRespondida',
    'Respuesta4.42': 'DificultadVerCercaLejos',
    'Respuesta4.44': 'DificultadOir',
    'Respuesta4.53': 'DificultadMovilidad',
    'Respuesta4.58': 'DificultadCognitiva',
    'Respuesta4.64': 'DificultadInteraccionSocial',
    # Aquí agregas el resto de mapeos
    'Orden5': 'CondicionDiscapacidadRespondida',
    'Respuesta6': 'RespuestaCondicionDiscapacidad',
    'Orden6': 'CategoriaDiscapacidadRespondida',
    'Respuesta6.43': 'DiscapacidadBajaVision',
    'Respuesta6.45': 'DiscapacidadMultiple',
    'Respuesta6.55': 'DiscapacidadPsicosocialMental',
    'Respuesta6.3': 'DiscapacidadMiembrosSuperioresInferiores',
    'Respuesta6.59': 'DiscapacidadHipoacusia',
    'Respuesta6.6': 'DiscapacidadMiembrosInferiores',
    'Respuesta6.62': 'DiscapacidadCeguera',
    'Respuesta6.67': 'DiscapacidadIntelectual',
    'Respuesta6.74': 'DiscapacidadMiembrosSuperiores',
    'Respuesta6.75': 'SinCorrespondenciaDiscapacidad',
    
    'Orden7': 'DispositivosMovilidadRespondida',
    'Respuesta7.46': 'DispositivoBastonApoyo',
    'Respuesta7.48': 'DispositivoEspecifico',
    'Respuesta7.48_Otro': 'OtroDispositivo',
    'Respuesta7.3': 'DispositivoOrtopedico',
    'Respuesta7.60': 'AyudasAuditivas',
    'Respuesta7.63': 'BastonOrientacionMovilidad',
    'Respuesta7.66': 'SillaRuedasMotorizada',
    'Respuesta7.73': 'Muletas',
    
    'Orden8': 'LugaresUniversidadRespondida',
    'Respuesta8.1': 'CampusMedellinCiudadUniversitaria',
    'Respuesta8.49': 'CampusApartado',
    'Respuesta8.50': 'CampusCaucasia',
    'Respuesta8.51': 'CampusElCarmenDeViboral',
    'Respuesta8.52': 'CampusTurbo',
    'Respuesta8.54': 'CampusMedellinSedePosgrados',
    'Respuesta8.65': 'CampusMedellinEdificioSanIgnacio',
    'Respuesta8.68': 'CampusMedellinAntiguaEscuelaDerecho',
    'Respuesta8.69': 'CampusMedellinFacultadMedicina',
    'Respuesta8.70': 'CampusMedellinSIU',
    'Respuesta8.71': 'CampusMedellinFacultadOdontologia',
    'Respuesta8.72': 'CampusAmalfi',
    'Respuesta8.76': 'CampusAndes',
    
    'Orden9': 'AccesoEspaciosUniversidadRespondida',
    'Respuesta9.10': 'AccesoSenderosPeatonales',
    'Respuesta9.10_Otro': 'AccesoSenderosPeatonalesNivel',
    'Respuesta9.11': 'AccesoSenaletica',
    'Respuesta9.11_Otro': 'AccesoSenaleticaNivel',
    'Respuesta9.2': 'AccesoAscensores',
    'Respuesta9.2_Otro': 'AccesoAscensoresNivel',
    'Respuesta9.3': 'AccesoBaldosasPodotactiles',
    'Respuesta9.3_Otro': 'AccesoBaldosasPodotactilesNivel',
    'Respuesta9.4': 'AccesoBanosAccesibles',
    'Respuesta9.4_Otro': 'AccesoBanosAccesiblesNivel',
    'Respuesta9.5': 'AccesoEscaleras',
    'Respuesta9.5_Otro': 'AccesoEscalerasNivel',
    'Respuesta9.6': 'AccesoEstacionamientosReservados',
    'Respuesta9.6_Otro': 'AccesoEstacionamientosReservadosNivel',
    'Respuesta9.7': 'AccesoMobiliarioAulasOficinas',
    'Respuesta9.7_Otro': 'AccesoMobiliarioAulasOficinasNivel',
    'Respuesta9.8': 'AccesoPuertasAulas',
    'Respuesta9.8_Otro': 'AccesoPuertasAulasNivel',
    'Respuesta9.9': 'AccesoRampas',
    'Respuesta9.9_Otro': 'AccesoRampasNivel',

    'Orden10': 'AccesibilidadLugaresUniversidadRespondida',
    'Respuesta10.12': 'AccesibilidadAulasOficinas',
    'Respuesta10.12_Otro': 'AccesibilidadAulasOficinasNivel',
    'Respuesta10.13': 'AccesibilidadBiblioteca',
    'Respuesta10.13_Otro': 'AccesibilidadBibliotecaNivel',
    'Respuesta10.14': 'AccesibilidadCafeterias',
    'Respuesta10.14_Otro': 'AccesibilidadCafeteriasNivel',
    'Respuesta10.15': 'AccesibilidadEnfermeria',
    'Respuesta10.15_Otro': 'AccesibilidadEnfermeriaNivel',
    'Respuesta10.16': 'AccesibilidadEscuchaderos',
    'Respuesta10.16_Otro': 'AccesibilidadEscuchaderosNivel',
    'Respuesta10.17': 'AccesibilidadEspaciosDeportivos',
    'Respuesta10.17_Otro': 'AccesibilidadEspaciosDeportivosNivel',
    'Respuesta10.18': 'AccesibilidadLaboratoriosTalleres',
    'Respuesta10.18_Otro': 'AccesibilidadLaboratoriosTalleresNivel',
    'Respuesta10.19': 'AccesibilidadZonasComunes',
    'Respuesta10.19_Otro': 'AccesibilidadZonasComunesNivel',
    'Respuesta10.20': 'AccesibilidadSalaLactancia',
    'Respuesta10.20_Otro': 'AccesibilidadSalaLactanciaNivel',
    'Respuesta10.21': 'AccesibilidadSalasComputo',
    'Respuesta10.21_Otro': 'AccesibilidadSalasComputoNivel',
    'Respuesta10.22': 'AccesibilidadTeatrosMuseos',
    'Respuesta10.22_Otro': 'AccesibilidadTeatrosMuseosNivel',

    'Orden11': 'AccesibilidadInformacionConocimientoRespondida',
    'Respuesta11.23': 'AccesibilidadComunicadosAlertas',
    'Respuesta11.23_Otro': 'AccesibilidadComunicadosAlertasNivel',
    'Respuesta11.24': 'AccesibilidadContenidosEducativos',
    'Respuesta11.24_Otro': 'AccesibilidadContenidosEducativosNivel',
    'Respuesta11.25': 'AccesibilidadInformacionDeportivaRecreativa',
    'Respuesta11.25_Otro': 'AccesibilidadInformacionDeportivaRecreativaNivel',
    'Respuesta11.26': 'AccesibilidadInformacionFeriaBazar',
    'Respuesta11.26_Otro': 'AccesibilidadInformacionFeriaBazarNivel',
    'Respuesta11.27': 'AccesibilidadInformacionCultural',
    'Respuesta11.27_Otro': 'AccesibilidadInformacionCulturalNivel',
    'Respuesta11.28': 'AccesibilidadMaterialAudiovisual',
    'Respuesta11.28_Otro': 'AccesibilidadMaterialAudiovisualNivel',
    'Respuesta11.29': 'AccesibilidadMaterialImpreso',
    'Respuesta11.29_Otro': 'AccesibilidadMaterialImpresoNivel',
    'Respuesta11.30': 'AccesibilidadPortalWebUdeA',
    'Respuesta11.30_Otro': 'AccesibilidadPortalWebUdeANivel',
    'Respuesta11.31': 'AccesibilidadRecursosDigitales',
    'Respuesta11.31_Otro': 'AccesibilidadRecursosDigitalesNivel',
    'Respuesta11.32': 'AccesibilidadRepositorioInstitucional',
    'Respuesta11.32_Otro': 'AccesibilidadRepositorioInstitucionalNivel',
    'Respuesta11.33': 'AccesibilidadRevistasDigitales',
    'Respuesta11.33_Otro': 'AccesibilidadRevistasDigitalesNivel',

    'Orden12': 'AspectosOrganizacionalesRespondida',
    'Respuesta12.34': 'EducacionInclusivaConocimiento',
    'Respuesta12.34_Otro': 'EducacionInclusivaConocimientoNivel',
    'Respuesta12.35': 'DirectricesAdaptacionesCurriculares',
    'Respuesta12.35_Otro': 'DirectricesAdaptacionesCurricularesNivel',
    'Respuesta12.36': 'FormacionAccesibilidadComunidad',
    'Respuesta12.36_Otro': 'FormacionAccesibilidadComunidadNivel',
    'Respuesta12.37': 'ParticipacionDiscapacidadInvestigacion',
    'Respuesta12.37_Otro': 'ParticipacionDiscapacidadInvestigacionNivel',
    'Respuesta12.38': 'NormatividadAccesibilidad',
    'Respuesta12.38_Otro': 'NormatividadAccesibilidadNivel',
    'Respuesta12.39': 'OfertaProgramasDiscapacidad',
    'Respuesta12.39_Otro': 'OfertaProgramasDiscapacidadNivel',
    'Respuesta12.40': 'RecursosProduccionMaterialesAccesibles',
    'Respuesta12.40_Otro': 'RecursosProduccionMaterialesAccesiblesNivel',
    'Respuesta12.41': 'SensibilizacionPersonalAtencion',
    'Respuesta12.41_Otro': 'SensibilizacionPersonalAtencionNivel',

    'Orden13': 'BarrerasActitudinalesRespondida',
    'Respuesta13': 'BarrerasActitudinales',

    'Orden14': 'AmpliacionRespuestaRespondida',
    'Respuesta14': 'AmpliacionRespuesta',

    'Orden15': 'ModoAmpliacionRespondida',
    'Respuesta15.47': 'AmpliacionPorTexto',
    'Orden16': 'ComentariosFinalesRespondida',
    'Respuesta16': 'ComentariosFinales',

    'Orden19': 'ComentariosFinalesRespondida2',
    'Respuesta19': 'ComentariosFinales2',
    
    'Orden20' : 'ComentariosFinalesRespondida3',
    'Respuesta20': 'ComentariosFinales3'

}

def to_title_case(s):
    # Función para convertir a Title Case, ignorando palabras que son completamente en mayúsculas o abreviaturas
    return ' '.join(word.capitalize() if word.islower() else word 
                    for word in re.findall(r'\b\w+\b', s.replace('.', '_').replace('_', ' '))).replace(' ', '')

# Aplicamos el mapeo y convertimos a Title Case
data.columns = [to_title_case(column_mapping.get(col, col)) for col in data.columns]

# Cambia los valores en las columnas de Orden
for col in data.columns:
    if re.match(r'^Orden\d+$', col):  # Comprueba si la columna es 'Orden' seguido por un número
        data[col] = data[col].apply(lambda x: 1 if pd.notna(x) and x != '' else 0)

# Insertar datos en la nueva tabla
try:
    data.to_sql('tabla_20250109', engine, if_exists='replace', index=False)
    print("Datos cargados y tabla creada o actualizada en 'tabla_20250109' en la base de datos.")
except Exception as e:
    print(f"Error al cargar datos en la tabla: {e}")

# Verificar las columnas existentes antes de renombrar
with engine.connect() as connection:
    result = connection.execute(text("SELECT column_name FROM information_schema.columns WHERE table_name = 'tabla_20250109';"))
    existing_columns = [row[0] for row in result]

    try:
        for old_name, new_name in column_mapping.items():
            old_name_lower = old_name.lower().replace('.', '_')  # Ajustamos por si hay puntos en lugar de guiones bajos
            if old_name_lower in existing_columns:
                new_name_title = to_title_case(new_name)
                operation = text(f"ALTER TABLE tabla_20250109 RENAME COLUMN {old_name_lower} TO {new_name_title};")
                try:
                    connection.execute(operation)
                    print(f"Columna '{old_name}' renombrada a '{new_name_title}'.")
                except ProgrammingError as e:
                    if 'does not exist' in str(e):
                        print(f"La columna '{old_name}' no existe, no se pudo renombrar.")
                    else:
                        raise
            else:
                print(f"No se encontró la columna '{old_name}' para renombrar.")
    except Exception as e:
        print(f"Error en el proceso de renombramiento: {e}")

def verify_columns(connection):
    result = connection.execute(text("""
        SELECT column_name 
        FROM information_schema.columns 
        WHERE table_name = 'tabla_20250109'
    """))
    existing_columns = [row[0] for row in result]
    expected_columns = [to_title_case(col) for col in column_mapping.values()]
    missing_columns = set(expected_columns) - set(existing_columns)
    extra_columns = set(existing_columns) - set(expected_columns)

    if missing_columns:
        print(f"Columnas esperadas pero no encontradas: {', '.join(missing_columns)}")
    if extra_columns:
        print(f"Columnas adicionales no esperadas: {', '.join(extra_columns)}")

with engine.connect() as connection:
    verify_columns(connection)

print("Proceso de renombramiento y verificación completado.")