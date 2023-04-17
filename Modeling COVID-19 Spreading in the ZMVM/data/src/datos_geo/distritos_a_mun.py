import pandas as pd
import pickle

# leemos el archivo con las respuestas a la encuesta Origen Destino
# este archivo es muy grande para github. No lo subí
encuesta = pd.read_csv("C:/Users/Edgar Trejo/Desktop/tviaje.csv")
# obtenemos las respuestas para viajes que son de la cdmx, del edomex y hgo
# la pregunta 'p5_7_7' tiene el código del estado de origen
encuesta = encuesta[encuesta["p5_7_7"].isin([9, 15, 13])]
# queremos los datos del municipio de origen: p5_7_6, estado de origen: p5_7_7, distrito de origen: dto_origen
# municipio de destino: p5_12_6, estado de destino: p5_12_7, distrito de destino: dto_dest
encuesta = encuesta[["p5_7_6", "p5_7_7", "dto_origen", "p5_12_6", "p5_12_7", "dto_dest"]]
# cambiamos los nombres para que esté más cool. Nos da más info que solo el código de la pregunta
encuesta = encuesta.rename(columns = {"p5_7_6":"mun_origen", "p5_7_7":"est_origen", "p5_12_6":"mun_dest",
                                                 "p5_12_7":"est_dest"})

# hacemos un multi index
encuesta.set_index(['dto_origen', 'est_origen', 'mun_origen'], inplace = True)
# con esto ya podemos mapear
distritos = {}
cve_est = lambda x: "0"*(2-len(str(x))) + str(x)
cve_mun = lambda x: "0"*(3-len(str(x))) + str(x)
for i in encuesta.index:
    # i es una tupla: la primer entrada es el distrito, la segunda el estado y el tercero el municipio
    if i[0] not in distritos and i[2] < 130: # números grandes en mun significan otra cosa
        distritos[i[0]] = cve_est(i[1]) + cve_mun(i[2])
# guardamos el diccionario en un archivo binario
with open('data/cleandata/ZMVM/distritos_a_cve_umun.pkl', 'wb') as handle:
    pickle.dump(distritos, handle, protocol=pickle.HIGHEST_PROTOCOL)