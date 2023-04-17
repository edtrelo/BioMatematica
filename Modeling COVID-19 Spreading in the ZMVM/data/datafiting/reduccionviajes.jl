using CSV
using DataFrames
using Dates
using Printf

metrodata = CSV.read("D:/Edgar Trejo/Universidad/BioMatematica/Modeling COVID-19 Spreading in the ZMVM/data/rawdata/afluenciastc_simple_02_2023.csv", DataFrame)
porfecha = groupby(metrodata, :fecha)
porfecha = combine(porfecha, :afluencia => sum)
inicios2020 = porfecha[DateTime("2020-01-01") .<= porfecha.fecha .<= DateTime("2020-02-27"), 2];
primerbrote = porfecha[DateTime("2020-02-27") .< porfecha.fecha .<= DateTime("2020-02-27") + Day(100), 2]

mediainicios2020 = mean(inicios2020)
mediaprimerbrote = mean(primerbrote)
reduccion = mediaprimerbrote/mediainicios2020

@printf("La media de la afluencia a inicio de 2020 era %d usuarios al día.\n", mediainicios2020)
@printf("La media de la afluencia los primeros 100 días de la pandemia era %d usuarios al día.\n", mediaprimerbrote)
@printf("La reducción de las medias de afluencia fue %f.", reduccion)
