import requests
import pandas as pd
import pickle

url = 'https://es.wikipedia.org/wiki/Zona_metropolitana_del_valle_de_M%C3%A9xico'
html = requests.get(url).content
df_list = pd.read_html(html)
# primer tabla de la página
df = df_list[1]

cves_nombre = {}
cves_poblacion = {}
# comenzamos en 1 porque el primer renglón son los nombres de las columnas
for i in range(1, len(df)):
    # la primer columna tiene las claves de los municipios
    # la segunda columna contiene los nombres
    cves_nombre[df.iloc[i, 0]] = df.iloc[i, 1]
    # la séptima columna tiene la población de 2020
    cves_poblacion[df.iloc[i,0]] = int(df.iloc[i, 6].replace('\xa0', ''))

with open('data/cleandata/ZMVM/cves_nombre_total.pkl', 'wb') as handle:
    pickle.dump(cves_nombre, handle, protocol=pickle.HIGHEST_PROTOCOL)

with open('data/cleandata/ZMVM/cves_poblacion_total.pkl', 'wb') as handle:
    pickle.dump(cves_poblacion, handle, protocol=pickle.HIGHEST_PROTOCOL)

cves = list(cves_poblacion.keys())
with open('data/cleandata/ZMVM/ZMVM_cves.pkl', 'wb') as handle:
    pickle.dump(cves, handle, protocol=pickle.HIGHEST_PROTOCOL)