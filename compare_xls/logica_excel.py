import pandas as pd
import os

def procesar_coincidencias(ruta1, ruta2, ruta_guardado_base):
    """
    Lee dos archivos de Excel, compara TODAS las columnas para buscar 
    filas exactamente iguales y guarda los resultados separados.
    """
    # 1. Cargar los archivos de Excel
    df1 = pd.read_excel(ruta1)
    df2 = pd.read_excel(ruta2)
    
    # Validar que los archivos tengan columnas en común
    columnas_comunes = df1.columns.intersection(df2.columns)
    if len(columnas_comunes) == 0:
        raise ValueError("Los archivos no tienen ninguna columna con el mismo nombre para poder compararlos.")

    # 2. Buscar coincidencias en TODAS las columnas comunes
    # Al no poner "on=", Pandas compara automáticamente usando todas las columnas que comparten
    cruce_total = pd.merge(df1, df2, how='outer', indicator=True)
    
    # 3. Filtrar
    # 'both': La fila exacta está en ambos archivos
    coincidencias = cruce_total[cruce_total['_merge'] == 'both'].drop(columns=['_merge'])
    
    # Diferencias: La fila está solo en el archivo 1 o solo en el archivo 2
    diferencias = cruce_total[cruce_total['_merge'] != 'both'].drop(columns=['_merge'])
    
    # 4. Generar los nombres de los dos archivos de salida
    nombre_base, extension = os.path.splitext(ruta_guardado_base)
    if not extension:
        extension = ".xlsx"
        
    ruta_coincidencias = f"{nombre_base}_coincidencias{extension}"
    ruta_diferencias = f"{nombre_base}_diferencias{extension}"
    
    # 5. Exportar los resultados
    coincidencias.to_excel(ruta_coincidencias, index=False)
    diferencias.to_excel(ruta_diferencias, index=False)
    
    return ruta_coincidencias, ruta_diferencias