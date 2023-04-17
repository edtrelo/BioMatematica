import geopandas as gpd
import matplotlib.pyplot as plt

ZMVMtotal = gpd.read_file("data/cleandata/ZMVMtotalmap/ZMVMtotal.shp", encoding = 'latin')
miZMVM = gpd.read_file("data/cleandata/miZMVMmap/miZMVM.shp", encoding = 'latin')

fig, ax = plt.subplots()
ZMVMtotal.plot(ax = ax, color = '#BEE0B7')
miZMVM.plot(ax= ax, color = '#3DAC27')
ax.set_axis_off()
fig.set_size_inches(12, 12)
plt.show()