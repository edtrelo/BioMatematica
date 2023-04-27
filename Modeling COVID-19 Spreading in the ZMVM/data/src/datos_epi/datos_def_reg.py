import pandas as pd
import pickle as pkl

with open("data/rawdata/regiones.pkl", "rb") as file:
    regiones = pkl.load(file)

# definimos una función para asignar su región a un municipio dado
def asignar_region(x):
    for k, v in regiones.items():
        if x in v:
            return str(k)
        
fp = 'data/cleandata/datos_epi/defunciones_miZMVM.csv'
casos = pd.read_csv(fp, sep = ',', encoding = 'utf-8', dtype = {'cve_ent':str})
casos['region'] = casos.cve_ent.apply(asignar_region)
casos = casos.groupby("region").sum(numeric_only=True)
casos.to_csv('data/cleandata/datos_epi/defunciones_reg.csv')