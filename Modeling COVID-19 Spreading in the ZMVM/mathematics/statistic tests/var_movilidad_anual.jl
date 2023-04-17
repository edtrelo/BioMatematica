using CSV
using DataFrames
using Dates
using HypothesisTests
using Plots
using Statistics
using StatsPlots
using CurveFit
fp = "D:/Edgar Trejo/Universidad/BioMatematica/Modeling COVID-19 Spreading in the ZMVM/data/rawdata/afluenciastc_simple_02_2023.csv"
# Vamos a usar los datos de afluencia del STC Metro para analizar la variabilidad de la movilidad de la ZMVM en el tiempo.
metrodata = CSV.read(fp, DataFrame);
# Agrupamos los datos de afluencia por fecha y los sumamos (cada fecha tiene la suma de la afluencia de cada estación).
porfecha = groupby(metrodata, :fecha)
porfecha = combine(porfecha, :afluencia => sum); # este es el equivalente a  groupby(column).sum() 
# La primer hipótesis que queremos probar es si no hay variabiliad entre la afluencia a fines de 2019 y a principios de 2020.
inicios2020 = porfecha[DateTime("2020-01-01") .<= porfecha.fecha .<= DateTime("2020-02-27"), 2];
data2019 = porfecha[DateTime("2019-01-01") .<= porfecha.fecha .<= DateTime("2019-12-31"), 2];
# test: E[X] == E[Y], donde inicios2020 ∼ X y data2019 ∼ Y.
@show MannWhitneyUTest(inicios2020, data2019) #p-value = 0.7439
# No hay evidencia que nos haga rechazar la hipótesis.
# Ahora queremos probar si el número esperado de usuarios en el metro en 2017 es el mismo que en el año 2020. 
# Obtenemos los datos de afluencia de cada año.
data2017 = porfecha[DateTime("2017-01-01") .<= porfecha.fecha .<= DateTime("2017-12-31"), 2];
# test: E[X] == E[Y], donde data2019 ∼ X y data2017 ∼ Y.
@show MannWhitneyUTest(data2019, data2017) # p-value = 0.0001
# Debemos rechazar la hipótesis de que la distribución de los datos no ha cambiado a lo largo del tiempo. 
# Veamos el siguiente gráfico de dispesión:
myplot = boxplot(["2017" "2019"], [data2019, data2019], legend = false, ylabel = "Afluencia diaria",
        xtickfontsize = 14, ytickfontsize = 10, yguidefontsize = 15);
#savefig(myplot,"D:/Edgar Trejo/Universidad/BioMatematica/Modeling COVID-19 Spreading in the ZMVM/data/graficaldata/distrmetro.png")
display(myplot)
# Podemos notar la gran cantidad de outliers, por ello queremos realizar la misma prueba pero a los datos sin estos outliers.
# definimos una función para obtener el rango intercuantil.
function iqrrange(x::Vector) 
    q1 = quantile!(x, 0.25)
    q3 = quantile!(x, 0.75)
    iqr = q3 - q1
    (q1 - 1.5*iqr, q3 + 1.5*iqr)
end
# Obtenemos el rango inter cuantil de cada año
rango2017 = iqrrange(data2017)
rango2019 = iqrrange(data2019)
# Creamos un dataframe donde cada renglón se la misma fecha del año.
datos = DataFrame(año2017=data2017, año2019=data2019);
# Filtramos los datos que se encuentren dentro de sus respectivos rangos intercuantiles.
temp = datos[( datos.año2017 .>= rango2017[1]) .& (datos.año2017 .<= rango2017[2]), :]
datosfiltro = temp[( temp.año2019 .>= rango2019[1]) .& (temp.año2019 .<= rango2019[2]), :];
# Realizamos la prueba de variabiliad de las esperanzas
@show MannWhitneyUTest(datosfiltro.año2017, datosfiltro.año2019) #p-value <1e-06
# Debemos rechazar la hipótesis de que la distribución de los datos no ha cambiado a lo largo del tiempo. 
# Veamos el siguiente gráfico de dispesión:
myplot = scatter(datosfiltro.año2017, datosfiltro.año2019, 
    xlabel = "Afluencia en 2017", ylabel = "Afluencia en 2019", legend = false,
    xtickfontsize = 10, ytickfontsize = 10, yguidefontsize = 15, xguidefontsize = 15);
#savefig(myplot,"D:/Edgar Trejo/Universidad/BioMatematica/Modeling COVID-19 Spreading in the ZMVM/data/graficaldata/2017vs2019metro.png")
display(myplot)
# Podemos probar una relación lineal entre las afluencias de los años.
@show cor(datosfiltro.año2017, datosfiltro.año2019)
# El coeficiente de correlación de las afluencias por año suguiere una relación lineal fuerte. 
# Suponiendo esto, los parámetros de la recta que mejor se ajustan son.
@show linear_fit(datosfiltro.año2017, datosfiltro.año2019) #a, b; donde y = a + bx
