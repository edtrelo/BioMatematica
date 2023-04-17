import geopandas as gpd
import matplotlib.pyplot as plt
import pickle

fp  = "D:/Edgar Trejo/Universidad/BioMatematica/Modeling COVID-19 Spreading in the ZMVM/data/rawdata/Censo 2010 (Municipal)/inegi_refcenmuni_2010.shp"
mapaMX = gpd.read_file(fp, encoding = 'latin')

with open("data/cleandata/ZMVM/ZMVM_cves.pkl", "rb") as file:
    zmvm = pickle.load(file)
# flageamos a los municipios de la ZMVM
mapaMX['inZMVM'] = mapaMX['cve_umun'].apply(lambda x: 1 if x in zmvm else 0)
fig, ax = plt.subplots()
mapaMX.plot('inZMVM', ax = ax, cmap = 'summer')
ax.set_axis_off()
fig.set_size_inches(18, 15)
plt.show()
