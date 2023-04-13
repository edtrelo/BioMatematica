import pandas as pd
import pickle as pkl

# casos de defunciones a los que vamos a ajustar las soluciones 
url_casos = "https://raw.githubusercontent.com/edtrelo/BioMatematica/main/Modeling%20COVID-19%20Spreading%20in%20the%20ZMVM/data/cleandata/Casos_Diarios_ZMVM_Defunciones.csv"
url_viajes = "https://raw.githubusercontent.com/edtrelo/BioMatematica/main/Modeling%20COVID-19%20Spreading%20in%20the%20ZMVM/data/cleandata/viajes_ZMVM.csv"

with open("D:/Edgar Trejo/Universidad/BioMatematica/Modeling COVID-19 Spreading in the ZMVM/data/rawdata/regiones.pkl", "rb") as file:
    regiones = pkl.load(file)
# obtenemos los municipios de las regiones
mun_ZMVM = []
for value in regiones.values():
    mun_ZMVM.extend(value)
# definimos una función para asignar su región a un municipio dado
def asignar_region(x):
    for k, v in regiones.items():
        if x in v:
            return k
# definimos las funciones para obtener nuestros datos por región
def viajes_regiones():
    """Obtiene el número de viajes que se realizan entre regiones."""
    global regiones
    # leemos y cambiamos los nombre de las columnas para trabajar más cómodo
    viajes = pd.read_csv(url_viajes, sep = ',', encoding = 'utf-8')
    viajes.rename(columns = {'Unnamed: 0':'nombre'}, inplace = True)
    # obtenemos la cve única del municipio
    with open("D:/Edgar Trejo/Universidad/BioMatematica/Modeling COVID-19 Spreading in the ZMVM/data/rawdata/municipios.pkl", "rb") as f:
        data = pkl.load(f)
    data["cve_umun"] = data.apply(lambda x: "0"*(2-len(str(x.estado))) +  str(x.estado) + "0"*(3-len(str(x.municipio))) +  str(x.municipio), axis = 1)
    data = data[data.cve_umun.isin(mun_ZMVM)]
    # definimos una función para cambiar de un nombre a su clave
    def nombre_to_cve(x):
        return data[data.nombre == x]['cve_umun'].values[0]
    # hacmeos los cambios: nombre->cve->región  
    viajes['cve_umun'] = viajes.nombre.apply(nombre_to_cve)
    viajes['region'] = viajes.cve_umun.apply(asignar_region)
    # agrupamos por región y sumamos
    viajes = viajes.groupby("region").sum()
    # obtenemos un diccionarios con nombre:región
    def nombrecol_to_rgn():
        ncols = {}
        for c in viajes.columns:
            if c[-1] == "1":
                ncols[c] = str(asignar_region(nombre_to_cve(c[:-2]))) + "_sab"
            elif c[-1] == "2":
                ncols[c] = str(asignar_region(nombre_to_cve(c[:-2]))) + "_dom"
            else:
                ncols[c] = asignar_region(nombre_to_cve(c))
        return ncols
    # agrupamos por columnas y sumamos
    viajes.rename(columns = nombrecol_to_rgn(), inplace = True)
    viajes = viajes.groupby(level = 0, axis = 1).sum()
    return viajes

def casos_regiones():
    """Obtiene el número de casos por región"""
    casos = pd.read_csv(url_casos, sep = ',', encoding = 'utf-8')
    with open("D:/Edgar Trejo/Universidad/BioMatematica/Modeling COVID-19 Spreading in the ZMVM/data/rawdata/municipios.pkl", "rb") as f:
        data = pkl.load(f)
    data["cve_umun"] = data.apply(lambda x: "0"*(2-len(str(x.estado))) +  str(x.estado) + "0"*(3-len(str(x.municipio))) +  str(x.municipio), axis = 1)
    data = data[data.cve_umun.isin(mun_ZMVM)]
    def nombre_to_cve(x):
        return data[data.nombre == x]['cve_umun'].values[0]
    casos['cve_umun'] = casos.nombre.apply(nombre_to_cve)
    casos['region'] = casos.cve_umun.apply(asignar_region)
    casos = casos.groupby("region").sum()
    return casos