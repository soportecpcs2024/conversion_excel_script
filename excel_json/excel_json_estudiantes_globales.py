import pandas as pd
import json
import os
import chardet
from datetime import datetime

# Define la ruta al archivo CSV y al archivo JSON de salida
csv_file_path = os.path.join(os.path.dirname(__file__), '../EstudiantesGlobales.csv')
json_file_path = os.path.join(os.path.dirname(__file__), 'estudiantesGlobales.json')

# Función para detectar la codificación del archivo
def detectar_codificacion(file_path):
    with open(file_path, 'rb') as f:
        result = chardet.detect(f.read())
    return result['encoding']

# Función para convertir fechas del formato "DD/MM/YYYY" a ISO 8601
def convertir_fecha(fecha_str):
    try:
        # Convertir fechas del formato "DD/MM/YYYY" a ISO 8601
        return datetime.strptime(fecha_str, "%d/%m/%Y").isoformat() if fecha_str else None
    except ValueError:
        # Devolver None si no se puede convertir
        return None

# Función para convertir valores booleanos
def convertir_booleano(valor):
    if isinstance(valor, str):
        return valor.lower() in ['true', '1', 'sí', 'si']
    return bool(valor)

# Función para convertir CSV a JSON
def convertir_csv_a_json(csv_file_path, json_file_path):
    try:
        # Detectar la codificación del archivo CSV
        encoding = detectar_codificacion(csv_file_path)
        print(f"Codificación detectada: {encoding}")

        # Leer el archivo CSV con la codificación detectada
        df = pd.read_csv(csv_file_path, sep=';', encoding=encoding)

        # Reemplazar NaN con cadenas vacías
        df = df.fillna('')

        # Normalizar los nombres de las columnas para que coincidan con el modelo Mongoose
        df.columns = [col.replace(' ', '_').lower() for col in df.columns]

        # Convertir fechas a formato ISO 8601
        for fecha_col in ['fecha_nacimiento', 'fecha_matricula', 'ultima_fecha_de_actualizacion']:
            if fecha_col in df.columns:
                df[fecha_col] = df[fecha_col].apply(convertir_fecha)

        # Convertir valores booleanos
        boolean_columns = [
            'tiene_subsidio',
            'madre_cabeza_familia',
            'beneficiario_heroe_nacion',
            'beneficiario_madre_cabeza_familia',
            'beneficiario_veterano_fuerza_publica',
            'proviene_sector_privado',
            'proviene_otro_municipio',
            'poblacion_victima_conflicto',
            'formalizada',
            'pertenece_regimen_contributivo'
        ]
        for col in boolean_columns:
            if col in df.columns:
                df[col] = df[col].apply(convertir_booleano)

        # Convertir números a enteros si es posible
        for col in df.columns:
            if df[col].dtype == float:
                df[col] = df[col].apply(lambda x: int(x) if not pd.isnull(x) and x.is_integer() else x)

        # Validar que cada registro tenga el campo requerido 'codigo_matricula'
        df = df[df['codigo_matricula'] != '']

        # Convertir el DataFrame a una lista de diccionarios
        resultados = df.to_dict(orient='records')

        # Guardar en un archivo JSON
        with open(json_file_path, 'w', encoding='utf-8') as json_file:
            json.dump(resultados, json_file, ensure_ascii=False, indent=2)
        
        print(f"Los datos del CSV se han convertido a JSON y se han guardado en {json_file_path}")
    
    except Exception as e:
        print(f"Error al leer el archivo CSV: {e}")

# Ejecuta la función de conversión
convertir_csv_a_json(csv_file_path, json_file_path)
