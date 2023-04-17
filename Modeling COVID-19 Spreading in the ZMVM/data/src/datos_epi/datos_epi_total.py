import pandas as pd
import pickle

with open('data/cleandata/ZMVM/cves_nombre_total.pkl', 'rb') as file:
    cves_nombre = pickle.load(file)
# claves de la ZMVM
cves = cves_nombre.keys()
# ------------------------- CASOS CONFIRMADOS -------------------------------------------------------------- #
# leemos los casos confirmados a nivel nacional
casosdiarios = pd.read_csv("data/rawdata/Casos_Diarios_Municipio_Confirmados_20230226.csv", encoding = 'utf-8', 
                          dtype = {'cve_ent':str, 'poblacion': str, 'nombre':str})
# filtramos para los municipios en la ZMVM
casosdiarios = casosdiarios[casosdiarios.cve_ent.isin(cves)]
# vamos a estar usando el estado y el municipio
casosdiarios.drop(columns = ['poblacion', 'nombre'], inplace = True)
casosdiarios.sort_values(by = 'cve_ent', inplace=True)
casosdiarios.to_csv('data/cleandata/datosepi/positivos_ZMVM_total.csv', sep = ',', 
                    encoding = 'utf-8', index = False)
# ------------------------- DEFUNCIONES  -------------------------------------------------------------- #
# leemos las nuevas defunciones a nivel nacional
casosdiarios = pd.read_csv("data/rawdata/Casos_Diarios_Municipio_Defunciones_20230226.csv", encoding = 'utf-8', 
                          dtype = {'cve_ent':str, 'poblacion': str, 'nombre':str})
# filtramos para los municipios en la ZMVM
casosdiarios = casosdiarios[casosdiarios.cve_ent.isin(cves)]
# vamos a estar usando el estado y el municipio
casosdiarios.drop(columns = ['poblacion', 'nombre'], inplace = True)
casosdiarios.sort_values(by = 'cve_ent', inplace=True)
casosdiarios.to_csv('data/cleandata/datosepi/defunciones_ZMVM_total.csv', sep = ',', 
                    encoding = 'utf-8', index = False)