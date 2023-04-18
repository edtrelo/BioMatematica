using DifferentialEquations
using CSV
using DataFrames
using PyCall
using Optim
using Plots
using Flux, DiffEqFlux

# ---------------------- parámetros fijos --------------------------- #
ν = 5/12
γ = 1/21
η = 1/7
f = 0.1
n = 47
# ----------------------- datos -------------------------------------- #
viajes = CSV.read("data/cleandata/viajes/viajes_entre_semana_por_cve_umun_2017.csv", DataFrame)
muertes = CSV.read("data/cleandata/datos_epi/defunciones_miZMVM.csv", DataFrame)

wi = zeros(100)
for i in 20:100
    wi[i] = muertes[1, 1 + (i-20)]
end

py"""
import pickle
 
def load_pickle(fpath):
    with open(fpath, "rb") as f:
        data = pickle.load(f)
    return data
"""
# crea la función en julia
load_pickle = py"load_pickle"
cves_pob = load_pickle("data/cleandata/ZMVM/cves_pob_miZMVM.pkl")
listpobmiZMVM = collect(values(cves_pob))
# -------------------- funciones auxiliares ---------------------------- #
function Q(i, j)
    return viajes[i, j + 1]
end
# suma de viajes de salida
Ngorro = sum.(eachcol(viajes[:, 2:n+1]))
function M(i)
    return Ngorro[i]
end

function N(i)
    return listpobmiZMVM[i]
end
# modelo
function F(du, u, p, t)
    # parámetros
    μ = p[1]
    Br = p[2:length(p)]

    function S(i)
        u[1 + (i-1)*5]
    end

    function E(i)
        u[2 + (i-1)*5]
    end

    function I(i)
        u[3 + (i-1)*5]
    end

    function R(i)
        u[4 + (i-1)*5]
    end

    function D(i)
        u[5 + (i-1)*5]
    end
    
    function Σ(k)
        return sum([Q(m, k) * (E(m) + f * I(m))/(N(m) * M(k)) for m in 1:n])
    end

    for i in 1:n
        du[1 + (i-1)*5] = - ν * S(i)/N(i) * sum([Q(i, k) * Br[k] * Σ(k) for k in 1:n]) - Br[i]*(1-ν)*S(i)*(E(i) + f*I(i))/N(i)
         
        du[2 + (i-1)*5] = ν * S(i)/N(i) * sum([Q(i, k) * Br[k] * Σ(k) for k in 1:n]) + Br[i]*(1-ν)*S(i)*(E(i) + f*I(i))/N(i)
        du[2 + (i-1)*5] += -(η+γ)*E(i)

        du[3 + (i-1)*5] = η*E(i) - γ*I(i) - μ*I(i)

        du[4 + (i-1)*5] = γ*I(i) + γ*E(i)

        du[5 + (i-1)*5] = μ*I(i)
    end

end

# condiciones iniciales
u0 = zeros(47*5)
for i in 1:47
    u0[1 + (i-1)*5] = N(i) - 1.0
    u0[3 + (i-1)*5] = 1.0
end
tspan = (0.0, 99.0)
# parámetros iniciales
p = zeros(48)
for i in 1:48
    p[i] = 0.1
end
params = Flux.params(p)

prob = ODEProblem(F, u0, tspan, p)

function predict_rd()
    solve(prob, Tsit5(), p=p, saveat=0.1)[5,:]
end

loss_rd() = sum(abs2, predict_rd()[i] - wi[i] for i in 1:100)


data = Iterators.repeated((), 100)

opt = ADAM(0.1)

#Flux.train!(loss_rdm params, data, opt)
