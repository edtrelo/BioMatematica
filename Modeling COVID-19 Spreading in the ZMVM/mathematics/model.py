# Descripación: Implementación del modelo con la que se describe la dinámica
# de la propagación de una enfermedad tipo COVID-19

# Paqueterías que se usan
import numpy as np
import pandas as pd
from scipy.integrate import solve_ivp
from scipy.optimize import least_squares
import pickle as pkl

class SEIRDmodel:

    def __init__(self, matriz_viajes, matriz_defunciones, 
                 indices_primeroscasos = [1, 3, 5], total_dias = 100,
                 propInfAislamientoTotal = 0.9,
                 tasaIncubacion = 1/7,
                 tasaRecuperacion = 1/21,
                 tiempoTrabajo = 5/12,
                 mortalidad = None,
                 tasasInfeccion = None):
        
        self.viajes = matriz_viajes
        self.size = matriz_viajes.shape[0] 
        self.casos = matriz_defunciones
        self.poblacion = self.casos['poblacion'].to_numpy()
        #self.viajesfuera = self.viajes.sum().to_numpy()
        # los parámetros que describen al modelo
        self.f = 1 - propInfAislamientoTotal
        self.η = tasaIncubacion
        self.γ = tasaRecuperacion
        self.ν = tiempoTrabajo
        self.μ = mortalidad
        self.Br = tasasInfeccion
        # parámetros para las simulaciones
        self.fecha_inicio = pd.to_datetime("27-february-2020")
        self.dias = total_dias
        self.tmax = self.dias - 1
        self.indices = indices_primeroscasos
        self.redtraf = 0
        self.inicio_red = 0
     
    def __Q(self, i, j, d):
        wd = (self.fecha_inicio.weekday() + d) % 7
        if wd == 5:  #sábado
            q = self.viajes.iloc[i, j + self.size]
        elif wd == 6: #domingo
            q = self.viajes.iloc[i, j + 2*self.size]
        else:
            q = self.viajes.iloc[i, j]

        if d>=self.inicio_red:
                q *= (1-self.redtraf)
        return q
    
    def __Ngorro(self, k, d):
        wd = (self.fecha_inicio.weekday() + d) % 7
        if wd == 5:
            n = self.viajes.iloc[:, k + self.size].sum()
        elif wd == 6:
            n = self.viajes.iloc[:, k + self.size*2].sum()
        else:
            n = self.viajes.iloc[:, k].sum()
        if d>self.inicio_red:
            n *= (1-self.redtraf)
        return n
        
    def __F(self, t, X, μ, *Br):
        """Modelo metapoblacional de la dinámica del covid-19 por Calvetti, et. al. Establece el sistema de edo para los parámetros
        mu en R y Br en R^n."""
        
        dXdt = np.zeros(self.size * 5) # aquí vamos a guardar las expresiones de las derivadas. Cada 5 entradas cambiamos de patch.
        
        def num(i, j, t):
            """Cantidades de viajes de la ciudad i a la ciudad j."""
            return self.__Q(i, j, t)
        
        def S(i):
            """Suceptibles de la ciudad i."""
            return X[5*i]
            
        def E(i):
            """Expuestos de la ciudad i."""
            return X[5*i + 1]
        
        def I(i):
            """Infectados (confirmados) de la ciudad i."""
            return X[5*i + 2]
        
        def R(i):
            """Recuperados de la ciudad i."""
            return X[5*i + 3]
        
        def D(i):
            """Dinfunntos de la ciudad i."""
            return X[5*i + 4]
        
        def βr(k):
            """Tasa de contacto en la ciudad k."""
            return Br[k]
        
        for i in range(self.size):
            # ponemos alias más fáciles de seguir
            f = self.f
            N = self.poblacion
            M = self.__Ngorro
            ν = self.ν
            γ = self.γ
            η = self.η
            # X_i; los componentes de cada ciudad
            def Σ(k):
                return sum([num(m, k, t) * (E(m) + f * I(m))/(N[m] * M(k, t)) for m in range(self.size)])
            
            # ecuación de los suceptibles para la ciudad i
            dXdt[5*i + 0] = - ν * S(i)/N[i] * sum([num(i, k, t) * βr(k) * Σ(k) for k in range(self.size)]) - βr(i)*(1-ν)*S(i)*(E(i) + f*I(i))/N[i]
            # ecuación de los expuestos para la ciudad i
            dXdt[5*i + 1] = ν * S(i)/N[i] * sum([num(i, k, t) * βr(k) * Σ(k) for k in range(self.size)]) + βr(i)*(1-ν)*S(i)*(E(i) + f*I(i))/N[i]
            dXdt[5*i + 1] += -(η+γ)*E(i)
            # ecuación de los infectados para la ciudad i
            dXdt[5*i + 2] = η*E(i) - γ*I(i) - μ*I(i)
            # ecuación de los recuperados para la ciudad i
            dXdt[5*i + 3] = γ*I(i) + γ*E(i)
            # ecuación para los fallecidos para la ciudad i
            dXdt[5*i + 4] = μ*I(i)
            
        return dXdt
    
    def __x0(self):
        """Condiciones iniciales del problema"""
        # inicialización de las condiciones iniciales
        x0 = []
        for k in range(self.size):
            # S0, E0, I0, R0, D0
            if k in self.indices: # si uno de los patches fue de los que registró un caso inicial
                x0.extend([self.poblacion[k] - 1, 0, 1, 0, 0])
            else:
                x0.extend([self.poblacion[k], 0, 0, 0, 0])
        return x0

    def __g(self, Θ):
        """Función que ocupamos para obtener la solución del sistema y que va 
        a ajustarse a los datos."""

        tdata = np.linspace(0, self.tmax, self.dias)
    
        sol = solve_ivp(self.__F, (0, self.tmax), self.__x0(), args = (Θ), t_eval = tdata)
    
        return sol.y    
    
    def ajustar(self, estimados = None):

        def getdata(tn):
            """Obtiene una matriz con los muertos de cada ciudad, donde cada columna es una ciudad distinta y tn es 
            el número de días a analizar."""
            data = np.zeros((self.size, tn-20))
            for k in range(self.size):
                # queremos los primeros tn casos de la ciudad k
                # suma acumulada de las defunciones, queremos los tn - 20 primeros días
                data[k] = self.casos.iloc[:, 1:-2].cumsum(axis = 1).iloc[k, 1:tn - 19]
            return data

        # obtenemos los datos
        data = getdata(self.dias)

        def residual(Θ):
            """Función a optimizar."""
            # obtenemos los valores iniciales 
            x0 = self.__x0()
            model = self.__g(Θ)
            # obtenemos las soluciones de los I_k
            modelI = np.zeros( (self.size, self.dias))
            # extraemos estos valores
            for k in range(self.size):
                # obtenemos las soluciones correspondientes a los Dinfuntos
                modelI[k] = model[5*k + 4]
            # las defunciones empezaron a registrarse a partir del vigésimo día de registrarse la primer infección
            return (modelI[:, 20:] - data).ravel()

        # creamos un vector con los valores estimados iniciales
        g0 = estimados
        if not estimados:
            g0 = [0.001]
            g0.extend([0.5]*self.size)
        # ajustamos
        ajuste = least_squares(residual, g0, bounds = ([0]*(self.size+1), [1]*(self.size+1))) 
        return ajuste.x # mu, Br
    
    def simular(self, redTraf = 0, semana_inicio_red = 0):
        self.inicio_red = semana_inicio_red*7
        self.redtraf = redTraf
        
        with open("D:/Edgar Trejo/Universidad/BioMatematica/Modeling COVID-19 Spreading in the ZMVM/results/ajuste8regiones.pkl", "rb") as file:
            ajuste = pkl.load(file)

        sol = self.__g(ajuste)

        return sol

    @property
    def params(self):
        p = {
            'Tasa de Incubación': self.η,
            'Tasa de Recuperación': self.γ,
            'Media de Tiempo fuera de Casa': self.ν,
            'Proporción de Infectados en Aislamiento Total': 1 - self.f,
            'Mortalidad': self.μ,
            'Tasas de Infección': self.Br
        }

        return p
    
    @property
    def diasModelados(self):
        return self.dias
    
    @property
    def poblaciones(self):
        return self.poblacion

    @property
    def ncompartimientos(self):
        return self.size