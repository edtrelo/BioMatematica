import pandas as pd
import pickle

def limpieza_matriz_movi(tipo_de_viaje):
    """Obtiene la matriz de movilidad entre distritos de la ZMVM a partir de uno de  dos artchivos csv: uno tiene la 
    información para los viajes entre semana y en sabado (esto último es el parámetro 'tipo de viaje'). 
    
    Args:
        tipo_de_viajes(str): 'entre_semana' o 'sabado'.
        
    Returns:
        pd.DataFrame: donde los nombres de las columnas y los registros de la columna 'origen' son los códigos de los
        distritos de la ZMVM."""
    # los nombres de ambos archivos inician de la misma forma
    nombre_archivo = "data/rawdata/tabulados_eod_2017_" + tipo_de_viaje + ".xlsx"
    try:
        hoja = ""
        if tipo_de_viaje == 'sabado':
            hoja = 'Matriz_OD_9.1'
        else: 
            hoja = 'Matriz_OD_8.1'
            # leemos el archivo excel correspondiente
        excel = pd.read_excel(nombre_archivo, sheet_name = hoja, keep_default_na = False)
    except:
        return
    # los datos en renglones empiezan desde el renglón 8 y terminan en el 194 (los distritos con nombre asignado.)
    excel = excel.iloc[8:194+8].reset_index(drop=True)
    # renombro la primer columna. Tiene un nombre feo --- que es el título
    nombre_feo = "INEGI. Encuesta Origen-Destino en Hogares de la Zona Metropolitana del Valle de México 2017 (EOD). Viajes "
    if tipo_de_viaje == 'sabado':
        nombre_feo += "en sábado" + ". Tabulados"
    else:
        nombre_feo += "entre semana" + ". Tabulados"
    excel.rename(columns = {nombre_feo:"origen"}, inplace = True)
    # obtenemos las claves de los distritos
    dist_names = {}
    for i, destino in enumerate(excel.iloc[:, 0]):
        # queremos solo el código
        dist_names["Unnamed: {}".format(i+2)] = int(destino[:3])
    # cambiamos el nombre del distrito por su clave 1-300
    excel.rename(columns = dist_names, inplace = True)
    # borramos la columna unnamed 1: que es los viajes del origen a la ZMVM y las dos últimas columnas que son depósitos
    excel.drop(columns = ["Unnamed: 1", "Unnamed: 196", "Unnamed: 197"], inplace = True)
    # en origen solo usamos los códigos de los distritos
    excel['origen'] = excel['origen'].apply(lambda x: int(x[0:3]))
    # regresamos la matriz de viajes con códigos de los distritos
    return excel

def distritos_a_mun(matrizMovilidadDistritos):
    """Mapea los códigos en la matriz de Movilidad por distritos a su código único de
     municipio eemmm y los agrupa por municipio.
    
    Args: 
        matrizMovilidadDistritos(pd.DataFrame): el resultado de la función limpiezaMatrizMovilidad."""
    # leemos el diccionario de distritos a cves únicas de municipio
    with open('data/cleandata/ZMVM/distritos_a_cve_umun.pkl', 'rb') as handle:
        distritos = pickle.load(handle)
    # cambiamos los códigos de los distritos por los pares de estado, municipio (en código)
    copy = matrizMovilidadDistritos.rename(columns = distritos)
    # agrupamos por columna, pues hay municipios que se repiten
    copy = copy.groupby(level = 0, axis = 1).sum()
    # cambiamos la columna origen
    copy['origen'] = copy['origen'].apply(lambda x: distritos[x])
    # agrupamos filas por los municipios
    copy = copy.groupby(by = 'origen').sum()
    # ordenamos por el código
    copy.sort_index(inplace = True)
    copy.sort_index(axis = 1, inplace = True)
    return copy

# obtenemos los viajes entre distritos.
matriz_entre_semana = limpieza_matriz_movi("entre_semana")
matriz_sabado = limpieza_matriz_movi("sabado")
# obtenemos los 
matriz_cves_entre_semana = distritos_a_mun(matriz_entre_semana)
matriz_cves_sabado = distritos_a_mun(matriz_sabado)
# guardamos los archivos
matriz_cves_entre_semana.to_csv('data/cleandata/viajes/viajes_entre_semana_por_cve_umun_2017.csv', 
                                sep = ',', encoding =  'utf-8')
matriz_cves_sabado.to_csv('data/cleandata/viajes/viajes_sabado_por_cve_umun_2017.csv', 
                                sep = ',', encoding =  'utf-8')

miZMVM = matriz_cves_entre_semana.index.to_list()
with open('data/cleandata/ZMVM/miZMVM_cves.pkl', 'wb') as handle:
    pickle.dump(miZMVM, handle, protocol=pickle.HIGHEST_PROTOCOL)
