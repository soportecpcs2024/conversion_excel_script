# Conversión de CSV a JSON

Este script Python convierte un archivo CSV a un archivo JSON. Detecta automáticamente la codificación del archivo CSV, maneja la codificación BOM si está presente, reemplaza los valores `NaN` con cadenas vacías, y convierte números flotantes enteros a enteros en el archivo JSON resultante.

## Requisitos

Asegúrate de tener instaladas las siguientes dependencias:

- `pandas`
- `json` (incluido en la biblioteca estándar de Python)
- `os` (incluido en la biblioteca estándar de Python)
- `chardet`

Puedes instalar las dependencias necesarias usando pip:

```bash
# pip install pandas chardet



#Variables
- csv_file_path: Ruta al archivo CSV de entrada.
- json_file_path: Ruta al archivo JSON de salida.
Funciones
detectar_codificacion(file_path)
Detecta la codificación de un archivo utilizando la biblioteca chardet.

#Parámetros:

file_path (str): Ruta del archivo del cual se desea detectar la codificación.
Retorno: (str) Codificación detectada del archivo.

convertir_csv_a_json(csv_file_path, json_file_path)
Convierte el archivo CSV especificado a un archivo JSON, reemplaza NaN con cadenas vacías y convierte números flotantes enteros a enteros.

#Parámetros:

csv_file_path (str): Ruta del archivo CSV de entrada.
json_file_path (str): Ruta del archivo JSON de salida.
Excepciones:

Captura y muestra cualquier excepción que ocurra durante el proceso de lectura del archivo CSV o escritura del archivo JSON.
Uso
Clona o descarga este repositorio.
Asegúrate de que el archivo CSV de entrada esté disponible en la ruta especificada en la variable csv_file_path.
Ejecuta el script utilizando Python.
