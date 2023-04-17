import geopandas as gpd
import pandas as pd
import pickle

fp  = "D:/Edgar Trejo/Universidad/BioMatematica/Modeling COVID-19 Spreading in the ZMVM/data/rawdata/Censo 2010 (Municipal)/inegi_refcenmuni_2010.shp"
mapaMX = gpd.read_file(fp, encoding = 'latin')

with open("data/cleandata/ZMVM/ZMVM_cves.pkl", "rb") as file:
    zmvm = pickle.load(file)
# flageamos a los municipios de la ZMVM
mapaMX['inZMVM'] = mapaMX['cve_umun'].apply(lambda x: 1 if x in zmvm else 0)
# filtramos
ZMVMtotal = mapaMX[mapaMX.inZMVM == 1]
# guardamos el archivo
ZMVMtotal.to_file("data/cleandata/ZMVMtotalmap/ZMVMtotal.shp")
# ahora vamos a obtener el mapa de mi ZMVM
with open("data/cleandata/ZMVM/miZMVM_cves.pkl", "rb") as file:
    mizmvm = pickle.load(file)
miZMVM = ZMVMtotal[ZMVMtotal.cve_umun.isin(mizmvm)]
# guardamos el archivo
miZMVM.to_file("data/cleandata/miZMVMmap/miZMVM.shp")

