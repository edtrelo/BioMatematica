import geopandas as gpd
import pickle as pkl

filepath = "D:/Edgar Trejo/Universidad/BioMatematica/Modeling COVID-19 Spreading in the ZMVM/data/rawdata/Censo 2010 (Municipal)/inegi_refcenmuni_2010.shp"
# leemos el mapa de todos los municipios de MX
map_MX = gpd.read_file(filepath, encoding = 'latin')
# leemos los municipios con lo que estamos trabajando
with open("D:/Edgar Trejo/Universidad/BioMatematica/Modeling COVID-19 Spreading in the ZMVM/data/rawdata/paresZMVM.pkl", "rb") as f:
    data = pkl.load(f)
def get_cve_mun(tupla):
    """Obtiene la clave única de municipio a partir del código de estado y del 
    código de municipio."""
    est = tupla[0]
    mun = tupla[1]
    est = "0"*(2-len(str(est))) + str(est)
    mun = "0"*(3-len(str(mun))) + str(mun)
    return est + mun
# obtenemos las claves de los municipios con los que estamos trabajando
cves = list(map(get_cve_mun, data))
# obtenemos el geoDataFrame de los municipios de la ZMVM
map_ZMVM = map_MX[map_MX.cve_umun.isin(cves)]
# leemos las regiones
with open("D:/Edgar Trejo/Universidad/BioMatematica/Modeling COVID-19 Spreading in the ZMVM/data/rawdata/regiones.pkl", "rb") as file:
    regiones = pkl.load(file)
def asignar_region(x):
    """Toma un código de municipio y le asigna su región."""
    for k, v in regiones.items():
        if x in v:
            return k
# establecemos la región para cada municipio en el geoDF de la ZMVM 
map_ZMVM["region"] = map_ZMVM["cve_umun"].apply(lambda x: asignar_region(x))
# creamos el geoDF con las regiones.
regiones = map_ZMVM.dissolve(by="region")
# guardamos el archivo
regiones.to_file('D:/Edgar Trejo/Universidad/BioMatematica/Modeling COVID-19 Spreading in the ZMVM/data/cleandata/regiones/regiones.shp')
