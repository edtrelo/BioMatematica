import pandas as pd
import numpy as np
import pickle

fp = "data/cleandata/viajes/viajes_sabado_por_cve_umun_2017.csv"
matriz_sab = pd.read_csv(fp, index_col=0, encoding='utf-8', sep = ',')
# creamos la matriz para los domingos
matriz_dom = matriz_sab.copy()
# leemos el ajuste que hicimos para datos de sábado-domingo
fp = "D:/Edgar Trejo/Universidad/BioMatematica/Modeling COVID-19 Spreading in the ZMVM/results/ajuste_sabdom.pkl"
with open(fp, "rb") as file:
    beta, mu, sigma = pickle.load(file)
# multiplicamos las entradas de la matriz de sábado por el parámetro de proporcionalidad
matriz_dom = matriz_dom.multiply(beta)
# sumamos un número de la distribución normal
n = len(matriz_dom)
# creamos un array con los errores
errores = np.random.normal(mu, sigma, size = (n, n))
for i in range(n):
    for j in range(n):
        matriz_dom.iloc[i, j] += matriz_dom.iloc[i, j]*errores[i, j]
# aplicamos la función piso
myfloor = lambda x: np.floor(x).astype(int) # hay unas entradas que son negativas, pero cerca del cero.
matriz_dom = matriz_dom.apply(myfloor)
matriz_dom.to_csv('data/cleandata/viajes/viajes_domingo_por_cve_umun_2017.csv', 
                                sep = ',', encoding =  'utf-8')