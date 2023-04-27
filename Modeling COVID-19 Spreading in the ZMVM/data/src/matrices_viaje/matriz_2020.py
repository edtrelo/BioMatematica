import pandas as pd
import numpy as np
import pickle

np.random.seed(123)

with open("D:/Edgar Trejo/Universidad/BioMatematica/Modeling COVID-19 Spreading in the ZMVM/results/ajuste_anualEntreSemana.pkl", "rb") as file:
    df, loc, scale = pickle.load(file)
# usamos los ajustes de la recta afluencia2017 vs afluencia2019
es2017 = pd.read_csv("data/cleandata/viajes/viajes_entre_semana_por_cve_umun_2017.csv",
                     encoding='utf-8', index_col=0, dtype = {'origen':str})
# para sábado y domingo 2020 y 2017 suponemos que son iguales.
# hacemos el ajuste
es2020 = es2017.copy()
n = len(es2020)
beta = np.exp(scale*(np.random.standard_t(df, size = (n, n))) + loc)
for i in range(n):
    for j in range(n):
        es2020.iloc[i, j] *= beta[i, j] 
# función piso
myfloor = lambda x: np.floor(x).astype(int)
es2020 = es2020.apply(myfloor)
# guardamos los archivos
es2020.to_csv("data/cleandata/viajes/viajes_entre_semana_por_cve_umun_2020.csv",
              encoding='utf-8',)