# %%
# Importar Paquetes

import fitz
import re
from collections import Counter
import pandas as pd
import spacy
import nltk
from nltk.corpus import stopwords
import os

nltk.download('stopwords')

# Cargar el modelo de spaCy para español
nlp = spacy.load("es_core_news_sm")

# Cargar la lista de stopwords en español desde nltk
stopwords = set(stopwords.words('spanish'))

# Cargar rutas
info_path = r'D:\OneDrive\01_Automatizaciones&Modelos\17_AnalystText\Info'

# Definir un patrón de regex para eliminar números, signos de puntuación y links
patron_limpieza = re.compile(r'[^\w\s]|[\d_]|https?://\S+|www\.\S+')

# Inicializar un DataFrame para almacenar todas las frecuencias
df_total_frecuencias = pd.DataFrame(
    columns=['Palabra', 'Frecuencia', 'Archivo'])

for archivo in os.listdir(info_path):
    if archivo.endswith('.pdf'):
        path_pdf = os.path.join(info_path, archivo)
        nombre_archivo = archivo[:-4]
        pdf_document = fitz.open(path_pdf)
        total_words = []

        # Iterar sobre todas las páginas del PDF
        for pagina_num in range(pdf_document.page_count):
            pagina = pdf_document[pagina_num]
            palabras_pagina = pagina.get_text("words")
            # Extraer solo las palabras y limpiar el texto
            for palabra in palabras_pagina:
                palabra_limpia = re.sub(
                    patron_limpieza, '', palabra[4]).lower()
                if palabra_limpia and palabra_limpia not in stopwords:
                    total_words.append(palabra_limpia)

        # Lematizar y filtrar palabras
        palabras_lemas = []
        for palabra in total_words:
            doc = nlp(palabra)
            lema = doc[0].lemma_
            if lema.isalpha() and lema not in stopwords:
                palabras_lemas.append(lema)

        # Contar la frecuencia de cada palabra
        frecuencia_palabras = Counter(palabras_lemas)

        # Convertir el contador a un DataFrame
        df_frecuencias = pd.DataFrame(frecuencia_palabras.items(), columns=[
                                      'Palabra', 'Frecuencia'])

        # Añadir la columna con el nombre del archivo
        df_frecuencias['Archivo'] = nombre_archivo

        # Concatenar los resultados al DataFrame total
        df_total_frecuencias = pd.concat(
            [df_total_frecuencias, df_frecuencias], ignore_index=True)

# Guardar el DataFrame total en un archivo CSV
df_total_frecuencias.to_csv('frecuencias_palabras_total.csv', index=False)

# Mostrar el DataFrame total
print(df_total_frecuencias)
# %%
