import pickle

with open("data/cleandata/ZMVM/cves_poblacion_total.pkl", "rb") as file:
    cves_pob_total = pickle.load(file)

with open("data/cleandata/ZMVM/miZMVM_cves.pkl", "rb") as file:
    miscves = pickle.load(file) 

mipob = {}

for k in cves_pob_total.keys():
    if k in miscves:
        mipob[k] = cves_pob_total[k]

with open('data/cleandata/ZMVM/cves_pob_miZMVM.pkl', 'wb') as handle:
    pickle.dump(mipob, handle, protocol=pickle.HIGHEST_PROTOCOL)
