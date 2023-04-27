import pandas as pd
import numpy as np
import pickle
import matplotlib.pyplot as plt

np.random.seed(123)

fp = "data/cleandata/viajes/viajes_sabado_por_cve_umun_2017.csv"
matriz_sab = pd.read_csv(fp, index_col=0, encoding='utf-8', sep = ',', dtype = {'origen':str})
# creamos la matriz para los domingos
matriz_dom = matriz_sab.copy()
# leemos el ajuste que hicimos para datos de sábado-domingo
fp = "D:/Edgar Trejo/Universidad/BioMatematica/Modeling COVID-19 Spreading in the ZMVM/results/ajuste_sabdom.pkl"
with open(fp, "rb") as file:
    df, loc, scale = pickle.load(file)
n = len(matriz_dom)
print(df, loc, scale)
# multiplicamos las entradas de la matriz de sábado por el parámetro de proporcionalidad
beta = np.exp(scale*(np.random.standard_t(df, size = (n, n))) + loc)
for i in range(n):
    for j in range(n):
        matriz_dom.iloc[i, j] *= beta[i, j] 
# aplicamos la función piso
myfloor = lambda x: np.floor(x).astype(int) # hay unas entradas que son negativas, pero cerca del cero.
matriz_dom = matriz_dom.apply(myfloor)
matriz_dom.to_csv('data/cleandata/viajes/viajes_domingo_por_cve_umun_2017.csv', 
                                 sep = ',', encoding =  'utf-8')