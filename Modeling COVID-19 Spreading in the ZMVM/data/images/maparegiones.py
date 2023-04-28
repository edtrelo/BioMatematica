import geopandas as gpd
import matplotlib.pyplot as plt
from mycolorpy import colorlist as mcp
from matplotlib.transforms import Bbox
plt.rcParams["font.family"] = "Times New Roman"

filepath = 'D:/Edgar Trejo/Universidad/BioMatematica/Modeling COVID-19 Spreading in the ZMVM/data/cleandata/Regionesmap/regiones.shp'
regiones = gpd.read_file(filepath, encoding = 'latin ')

romanos = {1:'I', 2:'II', 3:'III', 4:'IV', 5:'V', 6:'VI', 7:'VII', 8:'VIII'}
fig, ax = plt.subplots()
regiones['p_total'] = [2008954, 3087543, 3956978, 3154056, 2523807, 905765, 2683885, 2419664]
# ploteamos el mapa
vmin = regiones['p_total'].min()
vmax = regiones['p_total'].max()
regiones.plot(column = 'p_total', cmap = 'Reds', ax = ax, norm=plt.Normalize(vmin = vmin, vmax = vmax))
regiones.apply(lambda x: ax.annotate(text=romanos[x['region']], 
                                     xy=x.geometry.centroid.coords[0], 
                                     ha='center',
                                     fontsize = 26), axis=1)
# removemos los spines
plt.axis('off')
fig.set_size_inches(16, 24)

sm = plt.cm.ScalarMappable(cmap='Reds', norm=plt.Normalize(vmin = vmin, vmax = vmax))
# fake up the array of the scalar mappable. Urgh...
sm._A = []
cb = fig.colorbar(sm, ax = ax, label = 'Casos Activos', fraction = 0.1)


plt.savefig('data/images/maparegionespob.jpg',
            bbox_inches="tight", dpi = 300)
