Bases de Datos consultadas

1. Casos Diarios de COVID-19 por Municipio: https://datos.covid-19.conacyt.mx/

En la sección de descargas se puede obtener el archivo csv. Existen cuatro categorías, que generan cada una un archivo diferente: Confirmados, Sospechosos, Negativos y Defunciones. Para cada categoría, cada archivo tienen una estructura similar. Los campos son:

- cve_ent: Los primeros dos dígitos son la clave del Estado, que va del 01 al 32 y se les adjudica tal par de dígitos según su orden alfabético, ej. Aguascalientes->"01". Los tres dígitos restantes tienen que ver con laclave del municipio/alcadía. 

- poblacion: Número de habitantes.

- nombre: Municipio/Alcadía. Hay que notar que, aunque debieran llevar, no se usan acentos. ej. "Coyoacan" estálistado, mientras que "Coyoacán" no existe como registro.

- El resto de columnas corresponden cada una a una fecha (desde el 26 de febrero de 2020). Para cada fecha y cadamunicipio se reporta el número de incidencias nuevas (según la cateogoría a la que haga referencia el archivo).

2. Encuesta Origen Destino en Hogares de la Zona Metropolitana del Valle de México (EOD) 2017: https://www.inegi.org.mx/programas/eod/2017/

En la sección "Tabulados" se puede descargar el archivo xlsx "tabulados_eod_2017_entre_semana" ("tabulados_eod_2017_sabado") que contienen una hoja "Matriz_OD_8.1" ("Matriz_OD_9.1") donde se organiza en forma de una matriz la información del número de viajes realizados entre semana (sábado) entre los distintos distritos. 

Para emparejar esta info con la de "Casos Diarios de COVID-18 por Municipio" se ocupó un el archivo "eod_2017_csv\tviaje_eod2017\conjunto_de_datos\tviaje.csv", descargable en la sección "Datos Abiertos", que contiene cada una de las respuestas de la encuesta OD. Con este archivo se hizo un match entre los distritos y su municipio/estado, con lo que se puedo crear la relación para sustituir los distritos de "tabulados_eod_2017_entre_semana" ("tabulados_eod_2017_sabado") con su respectiva pareja. 