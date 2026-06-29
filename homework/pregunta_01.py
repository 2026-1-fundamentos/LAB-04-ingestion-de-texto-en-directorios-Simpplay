# pylint: disable=import-outside-toplevel
# pylint: disable=line-too-long
# flake8: noqa
"""
Escriba el codigo que ejecute la accion solicitada en cada pregunta.
"""

import os
import zipfile
import pandas as pd

def pregunta_01():
    """
    La información requerida para este laboratio esta almacenada en el
    archivo "files/input.zip" ubicado en la carpeta raíz.
    Descomprima este archivo.

    Como resultado se creara la carpeta "input" en la raiz del
    repositorio, la cual contiene la siguiente estructura de archivos:


    ```
    train/
        negative/
            0000.txt
            0001.txt
            ...
        positive/
            0000.txt
            0001.txt
            ...
        neutral/
            0000.txt
            0001.txt
            ...
    test/
        negative/
            0000.txt
            0001.txt
            ...
        positive/
            0000.txt
            0001.txt
            ...
        neutral/
            0000.txt
            0001.txt
            ...
    ```

    A partir de esta informacion escriba el código que permita generar
    dos archivos llamados "train_dataset.csv" y "test_dataset.csv". Estos
    archivos deben estar ubicados en la carpeta "output" ubicada en la raiz
    del repositorio.

    Estos archivos deben tener la siguiente estructura:

    * phrase: Texto de la frase. hay una frase por cada archivo de texto.
    * sentiment: Sentimiento de la frase. Puede ser "positive", "negative"
      o "neutral". Este corresponde al nombre del directorio donde se
      encuentra ubicado el archivo.

    Cada archivo tendria una estructura similar a la siguiente:

    ```
    |    | phrase                                                                                                                                                                 | target   |
    |---:|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------|:---------|
    |  0 | Cardona slowed her vehicle , turned around and returned to the intersection , where she called 911                                                                     | neutral  |
    |  1 | Market data and analytics are derived from primary and secondary research                                                                                              | neutral  |
    |  2 | Exel is headquartered in Mantyharju in Finland                                                                                                                         | neutral  |
    |  3 | Both operating profit and net sales for the three-month period increased , respectively from EUR16 .0 m and EUR139m , as compared to the corresponding quarter in 2006 | positive |
    |  4 | Tampere Science Parks is a Finnish company that owns , leases and builds office properties and it specialises in facilities for technology-oriented businesses         | neutral  |
    ```


    """
    
    # Definimos las rutas principales
    ruta_zip = "files/input.zip"
    ruta_extraccion = "files/input"
    ruta_salida = "files/output"

    # 1. Extraer el archivo .zip si no está extraído todavía
    if not os.path.exists(ruta_extraccion):
        with zipfile.ZipFile(ruta_zip, 'r') as zip_ref:
            zip_ref.extractall("files")

    # Crear la carpeta de salida si no existe
    if not os.path.exists(ruta_salida):
        os.makedirs(ruta_salida)

    # 2. Recorrer las carpetas principales (usualmente 'train' y 'test')
    # Usamos os.listdir para no asumir los nombres y leer lo que haya en la carpeta extraída
    carpetas_principales = os.listdir(ruta_extraccion)

    for carpeta in carpetas_principales:
        ruta_carpeta = os.path.join(ruta_extraccion, carpeta)
        
        # Saltamos si hay algún archivo suelto que no sea carpeta
        if not os.path.isdir(ruta_carpeta):
            continue
            
        datos = []
        
        # Recorrer las subcarpetas de sentimientos (ej. 'pos', 'neg')
        for sentimiento in os.listdir(ruta_carpeta):
            ruta_sentimiento = os.path.join(ruta_carpeta, sentimiento)
            
            if os.path.isdir(ruta_sentimiento):
                
                # Recorrer los archivos de texto de cada sentimiento
                for nombre_archivo in os.listdir(ruta_sentimiento):
                    ruta_archivo = os.path.join(ruta_sentimiento, nombre_archivo)
                    
                    # Leer el contenido del archivo
                    with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
                        texto = archivo.read()
                        
                        # Guardar la frase y su respectivo sentimiento (target)
                        datos.append({
                            "phrase": texto,
                            "target": sentimiento
                        })
        
        # 3. Convertir la lista de datos a un DataFrame de pandas
        df = pd.DataFrame(datos)
        
        # 4. Guardar el DataFrame como archivo CSV
        nombre_csv = f"{carpeta}_dataset.csv"
        ruta_csv = os.path.join(ruta_salida, nombre_csv)
        
        df.to_csv(ruta_csv, index=False)