using CSV
using DataFrames
using Plots
using Dates
using PyCall
# Cargamos los datos de casos confirmados en MX
fpMX = "data/rawdata/Casos_Diarios_Municipio_Confirmados_20230226.csv"
MX = CSV.read(fpMX, DataFrame);
# Cargamos los datos de casos confirmados en la ZMVM
fpZMVM = "data/cleandata/datos_epi/positivos_ZMVM_total.csv"
ZMVM = CSV.read(fpZMVM, DataFrame);
# obtenemos la población de MX
pobMx = sum(MX[:, :poblacion])
# Creamos una función que nos regresé el achivo pkl, en python
py"""
import pickle
 
def load_pickle(fpath):
    with open(fpath, "rb") as f:
        data = pickle.load(f)
    return data
"""
# crea la función en julia
load_pickle = py"load_pickle"
# cargamos el diccionarios con las claves y poblaciones
cves_pob = load_pickle("data/cleandata/ZMVM/cves_poblacion_total.pkl")
# obtenemos la suma de todos los values del diccionario
listpobZMVM = collect(values(cves_pob))
pobZMVM = sum(listpobZMVM)
# número de casos en todo el país
casosMX_t = MX[:, 4:ncol(MX)]
casosMX = sum.(eachcol(casosMX_t))
# número de casos en toda la ZMVM
casosZMVM_t = ZMVM[:, 2:ncol(ZMVM)]
casosZMVM = sum.(eachcol(casosZMVM_t))
# obtenemos los casos por habitante
casosxhab_ZMVM = casosZMVM/pobZMVM
casosxhab_MX = casosMX/pobMx;
# creamos el eje x de fechas
inicio = DateTime(2020,02,27)
x = range(0, 1095, step = 1)
tm = inicio + Day.(x);

myplot = plot(tm, casosxhab_ZMVM, label = "ZMVM",
    ylabel = "Casos por habitante",
    yformatter = :scientific,
    grid = false, size = (1000,400),
    xtickfontsize = 12,
    ytickfontsize = 9,
    yguidefontsize = 15,
    legendfontsize = 15,
    fg_legend = :false)
myplot = plot!(tm, casosxhab_MX, label = "México")

savefig(myplot,"data/images/casosmxvscasoszmvm.png")
display(myplot)

