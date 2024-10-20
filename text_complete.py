#%%
import fitz  # PyMuPDF
import re

# Definir la ruta del archivo PDF y el nombre del archivo TXT de salida
pdf_path = r'D:\OneDrive\01_Automatizaciones&Modelos\17_AnalystText\Info\CP21-3 UNFCC.pdf'
txt_output_path = r'D:\OneDrive\01_Automatizaciones&Modelos\17_AnalystText\Info\CP21-3 UNFCC.txt'

# Abrir el documento PDF
pdf_document = fitz.open(pdf_path)

# Inicializar una lista para almacenar los párrafos
parrafos = []

# Iterar sobre todas las páginas del PDF
for pagina_num in range(pdf_document.page_count):
    pagina = pdf_document[pagina_num]  # Obtener cada página
    texto_pagina = pagina.get_text()  # Obtener el texto de la página
    
    # Dividir el texto en líneas
    lineas = texto_pagina.split('\n')
    
    # Limpiar y procesar líneas
    parrafo_actual = ""
    for linea in lineas:
        linea_limpia = linea.strip()
        
        # Omitir líneas que probablemente sean encabezados o pies de página
        # Esto puede variar según el formato de tu PDF, así que ajusta según sea necesario
        if linea_limpia and not re.match(r'^\d{1,2}\s+.*', linea_limpia):  # Ejemplo de omisión de encabezados
            if linea_limpia:  # Si la línea no está vacía
                if parrafo_actual:  # Si ya hay un párrafo en construcción
                    parrafo_actual += " " + linea_limpia
                else:
                    parrafo_actual = linea_limpia
        else:
            # Si encontramos una línea en blanco, guardamos el párrafo actual
            if parrafo_actual:
                parrafos.append(parrafo_actual.strip())
                parrafo_actual = ""  # Reiniciar el párrafo actual

    # Al final de cada página, si hay un párrafo pendiente, añadirlo
    if parrafo_actual:
        parrafos.append(parrafo_actual.strip())

# Escribir los párrafos en el archivo TXT
with open(txt_output_path, 'w', encoding='utf-8') as f:
    for parrafo in parrafos:
        f.write(parrafo + '\n\n')  # Añadir dos saltos de línea para separar los párrafos

print(f"El texto ha sido extraído y guardado en {txt_output_path}.")
# %%
