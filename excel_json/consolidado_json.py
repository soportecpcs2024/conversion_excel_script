import pandas as pd
import json
import os
import chardet

# Define la ruta al archivo CSV y al archivo JSON de salida
csv_file_path = os.path.join(os.path.dirname(__file__), '../consolidadoNotas.csv')  # Cambia el nombre del archivo aquí
json_file_path = os.path.join(os.path.dirname(__file__), 'consolidadoNotas.json')

# Función para detectar la codificación del archivo
def detectar_codificacion(file_path):
    with open(file_path, 'rb') as f:
        result = chardet.detect(f.read())
    return result['encoding']

# Función para convertir valores numéricos
def convertir_valores(df):
    # Convertir números a enteros si es posible
    for col in df.columns:
        if df[col].dtype == float:
            df[col] = df[col].apply(lambda x: int(x) if pd.notnull(x) and x.is_integer() else x)

    return df

# Función para convertir CSV a JSON
def convertir_csv_a_json(csv_file_path, json_file_path):
    try:
        # Detectar la codificación del archivo CSV
        encoding = detectar_codificacion(csv_file_path)
        print(f"Codificación detectada: {encoding}")

        # Leer el archivo CSV con la codificación detectada y el delimitador ';'
        df = pd.read_csv(csv_file_path, sep=';', encoding=encoding, quotechar='"', quoting=2, on_bad_lines='skip')

        # Reemplazar NaN con cadenas vacías
        df = df.fillna('')

        # Normalizar los nombres de las columnas para que coincidan con el modelo Mongoose
        df.columns = [col.replace(' ', '_').lower() for col in df.columns]

        # Convertir valores numéricos
        df = convertir_valores(df)

        # Convertir el DataFrame a una lista de diccionarios
        resultados = df.to_dict(orient='records')

        # Guardar en un archivo JSON
        with open(json_file_path, 'w', encoding='utf-8') as json_file:
            json.dump(resultados, json_file, ensure_ascii=False, indent=2)
        
        print(f"Los datos del CSV se han convertido a JSON y se han guardado en {json_file_path}")
    
    except FileNotFoundError:
        print(f"Archivo no encontrado: {csv_file_path}")
    except pd.errors.EmptyDataError:
        print(f"El archivo CSV está vacío: {csv_file_path}")
    except pd.errors.ParserError:
        print(f"Error al analizar el archivo CSV: {csv_file_path}")
    except Exception as e:
        print(f"Error al leer el archivo CSV: {e}")

# Ejecuta la función de conversión
convertir_csv_a_json(csv_file_path, json_file_path)
