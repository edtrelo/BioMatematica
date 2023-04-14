import geopandas as gpd
import matplotlib.pyplot as plt
from mycolorpy import colorlist as mcp
from matplotlib.transforms import Bbox
plt.rcParams["font.family"] = "Times New Roman"

filepath = 'D:/Edgar Trejo/Universidad/BioMatematica/Modeling COVID-19 Spreading in the ZMVM/data/cleandata/regiones/regiones.shp'
regiones = gpd.read_file(filepath, encoding = 'latin ')

romanos = {1:'I', 2:'II', 3:'III', 4:'IV', 5:'V', 6:'VI', 7:'VII', 8:'VII'}
fig, ax = plt.subplots()
# obtenemos colores para distinguir entre regiones
colors = mcp.gen_color(cmap="summer", n=8)
# ploteamos el mapa
regiones.plot(color = colors, ax = ax)
regiones.apply(lambda x: ax.annotate(text=romanos[x['region']], 
                                     xy=x.geometry.centroid.coords[0], 
                                     ha='center',
                                     fontsize = 26), axis=1)
# removemos los spines
plt.axis('off')
fig.set_size_inches(16, 24)

plt.savefig('Modeling COVID-19 Spreading in the ZMVM/data/graficaldata/maparegiones.jpg',
            bbox_inches="tight", dpi = 300)
