# ordenamos los datos para que los municipios se presenten en orden alfabético
import pandas as pd
url_viajes = "https://raw.githubusercontent.com/edtrelo/BioMatematica/main/Modeling%20COVID-19%20Spreading%20in%20the%20ZMVM/data/cleandata/viajes_ZMVM.csv"
viajes  = pd.read_csv(url_viajes)
# ordenamos por nombres
viajes = viajes.reindex(sorted(viajes.columns), axis = 1)
viajes.rename(columns = {'Unnamed: 0':'nombre'}, inplace = True)
viajes.set_index('nombre', inplace=True)
viajes.sort_index(inplace=True)
viajes.to_csv('D:\\Edgar Trejo\\Universidad\\BioMatematica\\Modeling COVID-19 Spreading in the ZMVM\\data\\cleandata\\viajes_ZMVM.csv', 
             sep = ',', encoding = 'utf-8', index = True)

url_casos = "https://raw.githubusercontent.com/edtrelo/BioMatematica/main/Modeling%20COVID-19%20Spreading%20in%20the%20ZMVM/data/cleandata/Casos_Diarios_ZMVM_Confirmados.csv"
casos = pd.read_csv(url_casos)
casos.sort_values(by = 'nombre', inplace = True)
casos.to_csv('D:\\Edgar Trejo\\Universidad\\BioMatematica\\Modeling COVID-19 Spreading in the ZMVM\\data\\cleandata\\Casos_Diarios_ZMVM_Confirmados.csv', 
             sep = ',', encoding = 'utf-8', index = False)
