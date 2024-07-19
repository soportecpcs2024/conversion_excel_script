import pandas as pd
import json
import os
import chardet

# Define la ruta al archivo CSV y al archivo JSON de salida
csv_file_path = os.path.join(os.path.dirname(__file__), '../EstudiantesGlobales.csv')
json_file_path = os.path.join(os.path.dirname(__file__), 'estudiantesGlobales.json')

# Función para detectar la codificación del archivo
def detectar_codificacion(file_path):
    with open(file_path, 'rb') as f:
        result = chardet.detect(f.read())
    return result['encoding']

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

        # Convertir números a enteros si es posible
        for col in df.columns:
            df[col] = df[col].apply(lambda x: int(x) if isinstance(x, float) and x.is_integer() else x)

        # Convertir a JSON
        resultados = df.to_dict(orient='records')

        # Guardar en un archivo JSON
        with open(json_file_path, 'w', encoding='utf-8') as json_file:
            json.dump(resultados, json_file, ensure_ascii=False, indent=2)
        
        print(f"Los datos del CSV se han convertido a JSON y se han guardado en {json_file_path}")
    
    except Exception as e:
        print(f"Error al leer el archivo CSV: {e}")

# Ejecuta la función de conversión
convertir_csv_a_json(csv_file_path, json_file_path)
