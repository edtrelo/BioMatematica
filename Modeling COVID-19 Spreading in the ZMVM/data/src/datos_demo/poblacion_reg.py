import pickle

with open('data/cleandata/ZMVM/cves_pob_miZMVM.pkl', 'rb') as file:
    cves_pob = pickle.load(file)

with open('data/rawdata/regiones.pkl', 'rb') as file:
    regiones = pickle.load(file)

for r in regiones:
    pob = sum([cves_pob[cve] for cve in regiones[r]])
    regiones[r] = pob

pobs = list(regiones.values())

with open('data/cleandata/ZMVM/pob_reg.pkl', 'wb') as handle:
    pickle.dump(pobs, handle, protocol=pickle.HIGHEST_PROTOCOL)