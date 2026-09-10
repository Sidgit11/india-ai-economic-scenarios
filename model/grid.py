"""Precompute the India model over the explorer's answer grid (5 questions)."""
import numpy as np, json, itertools, sys, warnings
from multiprocessing import Pool
warnings.filterwarnings('ignore')
from model import Scenario, run
from india import india_econ, india_scen, COG_IN

CAP = [0.20, 0.32, 0.48, 0.80, 0.95]          # fraction of cognitive work AI can do by 2030
ADO = [0.10, 0.20, 0.40, 0.60, 0.80]          # diffusion 2030
AUT = [0.10, 0.30, 0.50, 0.75, 0.90]          # automation share psi
PRO = [0.10, 0.405, 0.693, 1.386, 2.303]      # log gain 2030: ~same, 1.5x, 2x, 4x, 10x
ADJ = [0.60, 0.35, 0.17, 0.10, 0.08, 0.04, 0.02]  # search discount mu: 1-2mo, 3mo, 6mo, 9mo, 1y, 2y, 3y+

def one(idx):
    i,j,k,l,m = idx
    e = india_econ()
    f, d, psi, a, mu = CAP[i], ADO[j], AUT[k], PRO[l], ADJ[m]
    a0 = min(0.35, a); ga = (a - a0)/3.5
    sc = Scenario('custom', f*e.cog, d, a0, ga, psi, 0.25, mu, 0.25)
    try:
        df = run(e, sc, months=73)
        end = df.iloc[-1]; prev = df.iloc[-13]; anch = df[df.t>=2026.5].iloc[0]
        vals = [100*(np.exp(end.Y)-1), 100*(e.g+e.n+end.Y-prev.Y), 100*(np.exp(end.w)-1),
                100*(np.exp(end.wC)-1), 100*(np.exp(end.wN)-1), 100*end.sL,
                100*(end.lC/anch.lC-1), 100*end.uC, 100*end.u]
        return idx, [round(v,1) for v in vals]
    except Exception as ex:
        return idx, None

if __name__ == '__main__':
    combos = list(itertools.product(range(5),range(5),range(5),range(5),range(7)))
    with Pool() as p:
        res = p.map(one, combos, chunksize=25)
    out = {}
    bad = 0
    for idx, v in res:
        if v is None: bad += 1; continue
        out[''.join(map(str,idx))] = v
    print('done', len(out), 'bad', bad)
    json.dump({'CAP':CAP,'ADO':ADO,'AUT':AUT,'PRO':PRO,'ADJ':ADJ,
               'keys':['gdp','growth','wage','wC','wN','sL','lC','uC','u'],'grid':out},
              open('grid.json','w'), separators=(',',':'))
