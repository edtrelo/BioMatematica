import pandas as pd
import numpy as np
# usamos los ajustes de la recta afluencia2017 vs afluencia2019
a, b = 264.58643833925595, 0.9675041007145377
es2017 = pd.read_csv("data/cleandata/viajes/viajes_entre_semana_por_cve_umun_2017.csv",
                     encoding='utf-8', index_col=0)
sab2017 = pd.read_csv("data/cleandata/viajes/viajes_sabado_por_cve_umun_2017.csv",
                     encoding='utf-8', index_col=0)
dom2017 = pd.read_csv("data/cleandata/viajes/viajes_domingo_por_cve_umun_2017.csv",
                     encoding='utf-8', index_col=0)
# hacemos el ajuste
es2020 = es2017.multiply(b).add(a)
sab2020 = sab2017.multiply(b).add(a)
dom2020 = dom2017.multiply(b).add(a)
myfloor = lambda x: np.floor(x).astype(int)
es2020 = es2020.apply(myfloor)
sab2020 = sab2020.apply(myfloor)
dom2020 = dom2020.apply(myfloor)
# guardamos los archivos
es2020.to_csv("data/cleandata/viajes/viajes_entre_semana_por_cve_umun_2020.csv",
              encoding='utf-8',)
sab2020.to_csv("data/cleandata/viajes/viajes_sabado_por_cve_umun_2020.csv",
              encoding='utf-8',)
dom2020.to_csv("data/cleandata/viajes/viajes_domingo_por_cve_umun_2020.csv",
              encoding='utf-8',)