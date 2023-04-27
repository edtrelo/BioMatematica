import pandas as pd
import pickle as pkl

# casos de defunciones a los que vamos a ajustar las soluciones 
fp_viajes = ["data/cleandata/viajes/viajes_entre_semana_por_cve_umun_2020.csv",
             "data/cleandata/viajes/viajes_sabado_por_cve_umun_2017.csv",
             "data/cleandata/viajes/viajes_domingo_por_cve_umun_2017.csv"]

with open("data/rawdata/regiones.pkl", "rb") as file:
    regiones = pkl.load(file)

with open("data/cleandata/ZMVM/miZMVM_cves.pkl", "rb") as file:
    miZMVM = pkl.load(file)

# definimos una función para asignar su región a un municipio dado
def asignar_region(x):
    for k, v in regiones.items():
        if x in v:
            return str(k)
        
# definimos las funciones para obtener nuestros datos por región
def viajes_regiones(fp):
    """Obtiene el número de viajes que se realizan entre regiones."""
    # leemos y cambiamos los nombre de las columnas para trabajar más cómodo
    viajes = pd.read_csv(fp, sep = ',', encoding = 'utf-8', 
                         dtype={'origen': str})
    viajes['region'] = viajes.origen.apply(asignar_region)
    print(viajes)
    # agrupamos por región y sumamos
    viajes = viajes.groupby("region").sum(numeric_only=True)
    # obtenemos un diccionarios con nombre:región
    ncols = {}
    for c in viajes.columns:
        ncols[c] = asignar_region(c)
    # agrupamos por columnas y sumamos
    viajes.rename(columns = ncols, inplace = True)
    viajes = viajes.groupby(level = 0, axis = 1).sum()
    return viajes

viajes_es_reg = viajes_regiones(fp_viajes[0])
viajes_s_reg = viajes_regiones(fp_viajes[1])
viajes_d_reg = viajes_regiones(fp_viajes[2])

viajes_es_reg.to_csv('data/cleandata/viajes/viajes_es_reg.csv')
viajes_s_reg.to_csv('data/cleandata/viajes/viajes_s_reg.csv')
viajes_d_reg.to_csv('data/cleandata/viajes/viajes_d_reg.csv')