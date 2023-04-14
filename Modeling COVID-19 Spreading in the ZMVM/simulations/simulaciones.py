import pandas as pd
import geopandas as gpd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as cs
import sys
sys.path.insert(1, "D:/Edgar Trejo/Universidad/BioMatematica/Modeling COVID-19 Spreading in the ZMVM/mathematics")
import datosporregion as dpr
import model


def dfSimulacion(Modelo, compartimiento = 'Infectados', norm = False, **kwargs):
    """Ejecute la función 'simular' de Modelo y regresa un data frame con la evolución
    del compartimiento por semana y por región."""

    compartimientos = {'Suceptibles':0, 'Expuestos':1, 'Infectados':2,
                       'Recuperados':3, 'Removidos':3, 'Muertos':4}
    
    compartimiento = compartimientos[compartimiento]

    dias = Modelo.diasModelados
    n = Modelo.ncompartimientos
    y = Modelo.simular(**kwargs)

    compSol = y[[5*i + compartimiento for i in range(n)]]

    # creamos el diccionario con los datos que vamos a poner en el df
    df = {}
    semanas = int(dias/7)
    # obtenemos el número de casos por región por semana
    for i in range(semanas):
        week = 'semana_{}'.format(i+1)
        df[week] = compSol[:, i*7]
        if norm:
            df[week] = df[week]/Modelo.poblaciones
    # obtenemos las regiones
    df['region'] = [i+1 for i in range(n)]
    # regresamos el dataframe
    return pd.DataFrame(df)

def gdfSimulacion(Modelo, compartimiento = 'Infectados', norm = False, 
                  **kwparams):
    df = dfSimulacion(Modelo, compartimiento, norm)
    fr = 'D:/Edgar Trejo/Universidad/BioMatematica/Modeling COVID-19 Spreading in the ZMVM/data/cleandata/regiones/regiones.shp'
    map_rgn = gpd.read_file(fr, encoding = 'latin')
    # hacemos el merge de los dos dataframes
    return map_rgn.set_index('region').join(df.set_index('region'))

def animarMapa(gdf, ax, fig, norm = False):
    vmax = __getglobalmax(gdf)
    vmin = 0
    #"#3F9B0B" "#560319""#6CC417"
    colors = ["#3F9B0B","#7FE817","#DAEE01",
              "#DAEE01","#F9DB24", "#F9E30D", "#FFAE42", "#EB5406", "#FF0000", "#8B0000", "#560319"]
    nodes = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
    my_cmap = cs.LinearSegmentedColormap.from_list("mycmap", list(zip(nodes, colors)))

    def animate(t):
        plt.cla()
        if not norm:
            gdf.plot('semana_{}'.format(t+1), ax = ax, cmap = my_cmap, norm=cs.LogNorm(vmin=vmin+1.1, vmax=vmax))
        else: 
            gdf.plot('semana_{}'.format(t+1), ax = ax, cmap = my_cmap, norm=cs.Normalize(vmin=vmin, vmax=vmax))
        
        ax.set_title('Infectados en Semana Epidemiológica: {}'.format(t+1), fontsize = 10)
        plt.axis('off')
    # creamos la colorbar con la escala global
    if not norm:
        sm = plt.cm.ScalarMappable(cmap=my_cmap, norm=cs.LogNorm(vmin=vmin+1.1, vmax=vmax))
    else:
        sm = plt.cm.ScalarMappable(cmap=my_cmap, norm=cs.Normalize(vmin=vmin, vmax=vmax))
    cbar = fig.colorbar(sm, location = 'left', fraction = 0.1)
    plt.cla()
    
    
    return animate
    
def __getglobalmax(gdf):
    # obtenemos las semanas del gdf
    maxg = 0
    for i in range(14):
        maxg = gdf[['semana_{}'.format(i+1) for i in range(14)]].max()

    return maxg.max()

def plotMaps(gdf, ax, fig):
    pass

def generateMaps(gdf, ax, fig):
    pass

def reducirTrafico(red = 0, semana_inicio = 0):
    """
    Args:
    red(float): fracción a reducir, entre 0 y 1."""
    global viajes
    dias = modelobase.diasModelados
    semanas = int(dias/7)
    viajesreducidos = viajes.copy(deep = True)
    viajesreducidos = viajesreducidos.multiply(1-red)
    return viajesreducidos

def simularReduccionTrafico(red = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9],
                            sem_ini = 0):
    global casos
    df = {}
    for r in red:
        modelored = model.SEIRDmodel(viajes, casos)
        dfred = dfSimulacion(modelored, redTraf = r, semana_inicio_red = sem_ini)
        reduccionesMedias = reduccionMedia(dfred)
        df['{}'.format(r)] = reduccionesMedias
    
    return pd.DataFrame(df)
        

def reduccionMedia(caso):
    global dfbase
    casobase = dfbase
    reducciones = np.zeros(8)
    for i in range(8):
        ri_base = casobase.iloc[i]
        ri_caso = caso.iloc[i]
        red = (ri_base - ri_caso)/ri_base
        red_m = red.mean()
        reducciones[i] = red_m
    return reducciones


# ----------------------- CASO BASE --------------------------- #
# como las simulaciones las vamos a hacer para compararlas contra el caso base
viajes = dpr.viajes_regiones()
casos = dpr.casos_regiones()
modelobase = model.SEIRDmodel(viajes, casos)
dfbase = dfSimulacion(modelobase)