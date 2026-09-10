"""India calibration on top of the Korinek et al. (2026) framework.
Only *measured* structural inputs change; the AI scenario objects (2030 diffusion, gain,
automation share, reinstatement, search discount, posting speed, wage rigidity, capital
elasticity) are kept at the paper's values. The 2030 affected mass is rescaled so the same
FRACTION of cognitive work is affected as in the US (0.2/0.3/0.5 of 0.624)."""
import numpy as np, pandas as pd, json, sys
from model import Econ, Scenario, US_SCEN, run, table

COG_IN = 0.2304          # PLFS 2025 via ILOSTAT: ISCO 1-4 (13.6%) + 52 sales (9.4%)
US_CEIL = 0.624

def india_econ(**kw):
    e = Econ(
        sigma=0.5,
        sL0=0.53,            # PWT 11 labsh, India
        cog=COG_IN,
        eps=3.0,
        rbar=0.47/3.0,       # K/Y = 3.0 -> gross 15.7%, net 10.7%
        delta=0.05,
        g=0.050, n=0.015,    # 6.5% no-AI GDP growth; measured TFP = 0.53*5.0 = 2.65%
        lam=1.0, phi_fish=3.1,
        Ubar=0.043,          # PLFS CWS unemployment rate, all-India 15+
        qbar_yr=0.08,        # implied by f=0.15/month and the pool
        qT_share=0.55,
        rel_qC=1.216, rel_qN=0.935,   # cognitive-origin pool ~6%, other ~3.8%
        mubar=0.17, iota=1.27, fill_mean=0.65,
        m_anchor=0.22*COG_IN,         # same within-cognitive exposure (0.22) as the US
        d_anchor=0.05,
        xi=0.5,
    )
    for k,v in kw.items(): setattr(e,k,v)
    return e

def india_scen(e, dlag=1.0):
    out = {}
    for k, s in US_SCEN.items():
        frac = s.m2030/US_CEIL
        out[k] = Scenario(k, frac*e.cog, s.d2030*dlag, s.a_anchor, s.g_a, s.psi, s.rho, s.mu, s.thetaH)
    return out

if __name__ == '__main__':
    e = india_econ()
    sc = india_scen(e)
    res, paths = [], {}
    for k in sc:
        df = run(e, sc[k], months=73, verbose=(k=='modest'))
        res.append(table(e, df, k)); paths[k] = df
    T = pd.concat(res, axis=1)
    print("\n=== INDIA base ===\n", T.round(1).to_string())
    # US for comparison
    eu = Econ(); U = pd.concat([table(eu, run(eu, s, months=73), k) for k,s in US_SCEN.items()], axis=1)
    # sensitivities (substantial & extreme)
    sens = {}
    variants = {
        'wage-bill weighted cognitive share (0.35)': dict(cog=0.35, m_anchor=0.22*0.35),
        'inelastic capital (eps=1)': dict(eps=1.0),
        'perfectly elastic capital (eps=inf)': dict(eps=np.inf),
        'rigid formal wages (xi=0.9)': dict(xi=0.9),
        'flexible wages (xi=0)': dict(xi=0.0),
        'slower absorption (f=0.10/month)': dict(qbar_yr=0.055),
    }
    for name, kw in variants.items():
        ev = india_econ(**kw); sv = india_scen(ev)
        for k in ['substantial','extreme']:
            sens[(name,k)] = table(ev, run(ev, sv[k], months=73), k)
    ev = india_econ(); sv = india_scen(ev, dlag=0.5)
    for k in ['substantial','extreme']:
        sens[('adoption lag: 2030 diffusion halved',k)] = table(ev, run(ev, sv[k], months=73), k)
    S = pd.DataFrame(sens)
    print("\n=== sensitivities ===\n", S.round(1).to_string())
    # save
    out = {'india': T.round(2).to_dict(), 'us': U.round(2).to_dict(),
           'sens': {f"{a}|{b}": v.round(2).to_dict() for (a,b),v in sens.items()},
           'paths': {k: df[['t','Y','w','wC','wN','r','sL','lC','uC','u','K']].round(5).to_dict('list') for k,df in paths.items()},
           'params': {k: vars(v) for k,v in sc.items()}, 'econ': {k:(None if v==np.inf else v) for k,v in vars(e).items()}}
    json.dump(out, open('india_results.json','w'), indent=1, default=float)
    # headline arithmetic
    gdp26 = 346.36  # lakh crore FY26 nominal (used only for rupee illustration)
    print("\nCognitive workforce (PLFS 2025 total employed 476.6m x 23.0pct) =", round(476.557*COG_IN,1), "million")
