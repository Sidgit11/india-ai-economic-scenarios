"""Replication of Korinek, Jones, Sacher, Cotter & McCrory (2026), 'Economic Scenarios
for Transformative AI', Anthropic Institute WP 2026-02 -- monthly task-based model with
search/matching and sticky cognitive wage. Written from Appendix A / Table A.1."""
import numpy as np
from scipy.optimize import fsolve, brentq
from dataclasses import dataclass, field

@dataclass
class Econ:
    # structure
    sigma: float = 0.5
    sL0: float = 0.60
    cog: float = 0.624          # s_C/s_L
    eps: float = 3.0
    rbar: float = 0.115
    delta: float = 0.05
    g: float = 0.0167           # ideas / output per worker growth
    n: float = 0.0033           # labor force growth
    lam: float = 1.0
    phi_fish: float = 3.1       # 1-phi in TFP units
    # labor market normal times
    Ubar: float = 0.038
    qbar_yr: float = 0.11
    qT_share: float = 0.55
    rel_qC: float = 0.69
    rel_qN: float = 1.52
    mubar: float = 0.17
    iota: float = 1.27
    fill_mean: float = 0.65
    # AI anchors (mid-2026)
    m_anchor: float = 0.14
    d_anchor: float = 0.10
    t0: float = 2024.0
    t_anchor: float = 2026.5
    t_end: float = 2030.0
    xi: float = 0.5

@dataclass
class Scenario:
    name: str
    m2030: float; d2030: float; a_anchor: float; g_a: float
    psi: float; rho: float; mu: float; thetaH: float

US_SCEN = {
 'modest':      Scenario('modest',      0.2, 0.2, 0.30, 0.0,   0.50, 0.50, 0.17, 0.10),
 'substantial': Scenario('substantial', 0.3, 0.4, 0.35, 0.028, 0.75, 0.25, 0.08, 0.25),
 'extreme':     Scenario('extreme',     0.5, 0.6, 0.45, 0.10,  0.90, 0.00, 0.04, 0.50),
}

def logistic_path(anchor, v2030, ceil, t_anchor, t_end):
    span = t_end - t_anchor
    kappa = (1/span) * np.log(((ceil-anchor)/anchor) * (v2030/(ceil-v2030)))
    tmid = t_anchor + np.log(ceil/anchor - 1)/kappa
    return lambda t: ceil/(1+np.exp(-kappa*(t-tmid)))

def solve_actual(e, LamC, Bcap, dA, lC0, lN0, lC=None, wC=None, x0=None):
    """System (39). Either lC given (returns clearing wC) or wC given (returns lC demand).
    Unknowns: x=dln wC, y=dln wN, r=dln r, Y=dln Y  (or lC replaces x)."""
    s, sN0, sL0, sK0 = e.sigma, e.sL0*(1-e.cog), e.sL0, 1-e.sL0
    sC0 = e.sL0*e.cog
    def F(v):
        if lC is not None:
            x, y, r, Y = v; lc = lC
        else:
            lc, y, r, Y = v; x = wC
        f1 = sL0*LamC*np.exp((1-s)*(x-dA)) + sN0*np.exp((1-s)*(y-dA)) + Bcap*np.exp((1-s)*r) - 1
        f2 = np.log(lc/lC0) - (np.log(LamC/e.cog) + Y - s*x - (1-s)*dA)
        f3 = np.log(lN0*np.exp(0)/lN0) - 0  # placeholder replaced below
        f3 = lnN - (Y - s*y - (1-s)*dA)
        sK = Bcap*np.exp((1-s)*r)
        f4 = (r if not np.isfinite(e.eps) else e.eps*r - (np.log(sK/sK0) + Y - r))
        return [f1, f2, f3, f4]
    lnN = np.log(solve_actual._lN/lN0)
    if x0 is None:
        x0 = [0.0, 0.0, 0.0, 0.0] if lC is not None else [lC0, 0.0, 0.0, 0.0]
    sol, info, ier, msg = fsolve(F, x0, full_output=True, xtol=1e-11)
    if ier != 1:
        sol, info, ier, msg = fsolve(F, [0,0,0,0] if lC is not None else [lC0,0,0,0], full_output=True)
    return sol

def run(e: Econ, sc: Scenario, months=None, verbose=False):
    s = e.sigma; sL0 = e.sL0; sK0 = 1-sL0
    sC0 = sL0*e.cog; sN0 = sL0*(1-e.cog)
    h = 1/12
    # ---- paths
    mbar = e.cog
    m_of = logistic_path(e.m_anchor, sc.m2030, mbar, e.t_anchor, e.t_end)
    d_of = logistic_path(e.d_anchor, sc.d2030, 1.0, e.t_anchor, e.t_end)
    a_of = lambda t: sc.a_anchor + sc.g_a*(t-e.t_anchor)
    # ---- ideas
    phiR = sL0*e.phi_fish + e.lam      # 1-phi_R
    # ---- steady state of labor market
    Lbar = 1 - e.Ubar
    lC0 = e.cog*Lbar; lN0 = (1-e.cog)*Lbar
    qbar_m = 1-(1-e.qbar_yr)**(1/12)   # monthly fraction
    # split by relative separation rates, employment-weighted to qbar
    wC = e.cog; wN = 1-e.cog
    scale = qbar_m/(wC*e.rel_qC + wN*e.rel_qN)
    qC_hat, qN_hat = e.rel_qC*scale, e.rel_qN*scale
    qC = -np.log(1-qC_hat); qN = -np.log(1-qN_hat)
    HC, HN = qC*lC0, qN*lN0
    mub = e.mubar
    def pool_eq(UC):
        UN = e.Ubar-UC
        SC = UC+mub*UN; SN = mub*UC+UN
        fC = HC/SC + mub*HN/SN
        return fC*UC - HC
    UC = brentq(pool_eq, 1e-6, e.Ubar-1e-6); UN = e.Ubar-UC
    SC = UC+mub*UN; SN = mub*UC+UN
    fCbar = HC/SC + mub*HN/SN; fNbar = mub*HC/SC + HN/SN
    io = e.iota
    def fill(chi, H, S):
        return chi*(1-(H/(chi*S))**io)**(1/io)
    def chi_eq(chi):
        return (lC0*fill(chi,HC,SC)+lN0*fill(chi,HN,SN))/Lbar - e.fill_mean
    chi = brentq(chi_eq, max(HC/SC,HN/SN)*1.0001, 5.0)
    piC, piN = fill(chi,HC,SC), fill(chi,HN,SN)
    if verbose:
        print(f"SS: UC={UC*100:.2f} UN={UN*100:.2f} uC={UC/(UC+lC0)*100:.2f}% uN={UN/(UN+lN0)*100:.2f}% "
              f"piC={piC:.3f} piN={piN:.3f} chi={chi:.3f} f={ (fCbar*UC+fNbar*UN)/e.Ubar:.3f} qC={qC*100:.2f} qN={qN*100:.2f}")
    qCX, qCT = qC*(1-e.qT_share), qC*e.qT_share
    qNX, qNT = qN*(1-e.qT_share), qN*e.qT_share
    xim = e.xi**(1/12)
    # ---- state
    dA = 0.0
    lC, lN, UCt, UNt = lC0, lN0, UC, UN
    fC_prev, fN_prev = fCbar, fNbar
    wCrel_prev = 0.0
    T = int(round((e.t_end-e.t0)/h))+1 if months is None else months   # last row is the start of 2030
    rows = []
    guessA = None; guessB = None
    def prims(t):
        m, d, a = m_of(t), d_of(t), a_of(t)
        md = m*d
        LamC = e.cog - md*(1 - sc.rho*sc.psi - (1-sc.psi)*np.exp(-(1-s)*a))
        B = sc.psi*md*(np.exp(-(1-s)*a) - sc.rho)
        Bcap = sK0 + sL0*B
        lN_tilde = -np.log(1 - md*(1 - sc.rho*sc.psi - (1-sc.psi)*np.exp(-(1-s)*a)))
        return m, d, a, LamC, Bcap, lN_tilde
    def full_emp(t, dA):
        m, d, a, LamC, Bcap, lNt = prims(t)
        def cap_gap(r):
            sL = 1 - Bcap*np.exp((1-s)*r)
            dsL = np.log(sL/sL0)
            w = (dsL + lNt)/(1-s) + dA
            Y = w - dsL
            K = np.log((1-sL)/sK0) + Y - r
            return e.eps*r - K
        rmax = np.log(1/Bcap)/(1-s) - 1e-9   # keep labor share positive
        r = brentq(cap_gap, -0.5, min(rmax, 2.0)) if e.eps < np.inf else 0.0
        sL = 1 - Bcap*np.exp((1-s)*r); dsL = np.log(sL/sL0)
        w = (dsL+lNt)/(1-s) + dA; Y = w - dsL
        lNstar = lN0*np.exp(lNt); lCstar = lC0 + lN0 - lNstar
        return dict(m=m,d=d,a=a,LamC=LamC,Bcap=Bcap,lNt=lNt,r=r,sL=sL,w=w,Y=Y,lNstar=lNstar,lCstar=lCstar)
    for k in range(T):
        t = e.t0 + k*h
        fe = full_emp(t, dA); fe1 = full_emp(t+h, dA)
        LamC, Bcap = fe['LamC'], fe['Bcap']
        # gaps
        BN = max(0.0, np.log(fe1['lNstar']) - np.log(lN))
        # attached cognitive force and clearing wage
        NC = lC + max(0.0, UCt-UC)
        solve_actual._lN = lN
        solA = solve_actual(e, LamC, Bcap, dA, lC0, lN0, lC=NC, x0=guessA); guessA = solA
        wCc = solA[0]
        wcommon = fe['w']
        wCrel = xim*wCrel_prev + (1-xim)*(wCc - wcommon)
        wC = wcommon + wCrel
        solB = solve_actual(e, LamC, Bcap, dA, lC0, lN0, wC=wC, x0=guessB); guessB = solB
        lCd = solB[0]
        E = max(0.0, lC-lCd); Z = max(0.0, lCd-lC)
        # separations & openings
        qCt = qCX + qCT*fC_prev/fCbar; qNt = qNX + qNT*fN_prev/fNbar
        DC = max(0.0, E - qCt*lC)
        vC = (max(0.0, qCt*lC - E) + sc.thetaH*Z)/piC
        vN = (qNt + sc.thetaH*BN)*lN/piN
        # matching
        SCt = UCt + sc.mu*UNt; SNt = sc.mu*UCt + UNt
        HCt = chi*SCt*vC/(SCt**io + vC**io)**(1/io)
        HNt = chi*SNt*vN/(SNt**io + vN**io)**(1/io)
        fCt = HCt/SCt + sc.mu*HNt/SNt; fNt = sc.mu*HCt/SCt + HNt/SNt
        # reporting at realized employment
        solR = solve_actual(e, LamC, Bcap, dA, lC0, lN0, lC=lC, x0=guessA)
        mplC, wN, r, Y = solR
        sK = Bcap*np.exp((1-s)*r); sLr = 1-sK
        # income shares with sticky wage paid (profit small)
        labinc = np.exp(wC)*lC + np.exp(wN)*lN            # relative to w0*1
        labinc0 = lC0+lN0
        avgw = labinc/(lC+lN)
        K = np.log(sK/sK0) + Y - r
        capinc = np.log(np.exp(r)*np.exp(K))
        tfp = -(1/(1-s))*np.log(sK0 + sL0*(1 - fe['m']*fe['d']*(1-np.exp(-(1-s)*fe['a'])))*np.exp(-(1-s)*dA))
        rows.append(dict(t=t, m=fe['m'], d=fe['d'], a=fe['a'], Y=Y, w=np.log(avgw/(labinc0/(lC0+lN0))),
                         wC=wC, wN=wN, r=r, K=K, sL=sLr, lC=lC, lN=lN, UC=UCt, UN=UNt,
                         uC=UCt/(UCt+lC), u=(UCt+UNt), labinc=np.log(labinc/labinc0),
                         wbillC=np.log(np.exp(wC)*lC/lC0), capinc=capinc, tfp=tfp, dA=dA,
                         lCstar=fe['lCstar'], DC=DC, HN=HNt, fC=fCt))
        # stocks
        lC_new = (1-qCt)*lC - DC + HCt
        lN_new = (1-qNt)*lN + HNt
        UC_new = UCt + qCt*lC + DC - fCt*UCt
        UN_new = UNt + qNt*lN - fNt*UNt
        lC, lN, UCt, UNt = lC_new, lN_new, UC_new, UN_new
        fC_prev, fN_prev, wCrel_prev = fCt, fNt, wCrel
        # ideas
        dg = e.g*(np.exp(e.lam*Y - phiR*dA) - 1)
        dA = dA + h*dg
    import pandas as pd
    return pd.DataFrame(rows)

def table(e, df, label):
    end = df.iloc[-1]; prev = df.iloc[-13]
    k = df[df.t>=e.t_anchor].index[0]; anch = df.loc[k]
    noai_g = e.g+e.n
    out = {
      'GDP % above no-AI': 100*(np.exp(end.Y)-1),
      'GDP growth %/yr': 100*(noai_g + end.Y-prev.Y),
      'Avg wage %': 100*(np.exp(end.w)-1),
      'Cognitive wage %': 100*(np.exp(end.wC)-1),
      'Other wage %': 100*(np.exp(end.wN)-1),
      'Net return %': 100*(e.rbar*np.exp(end.r)-e.delta),
      'Capital stock %': 100*(np.exp(end.K)-1),
      'Labor share %': 100*end.sL,
      'Labor income %': 100*(np.exp(end.labinc)-1),
      'Cog wage bill %': 100*(np.exp(end.wbillC)-1),
      'Capital income %': 100*(np.exp(end.capinc)-1),
      'Cog employment % since mid-2026': 100*(end.lC/anch.lC-1),
      'Unemp cognitive %': 100*end.uC,
      'Unemp all %': 100*end.u,
      'TFP % above': 100*(np.exp(end.tfp)-1),
      'TFP growth %/yr': 100*(e.sL0*e.g + end.tfp-prev.tfp),
      'Ideas stock %': 100*end.dA,
    }
    return pd.Series(out, name=label)

import pandas as pd
if __name__ == '__main__':
    e = Econ()
    res = []
    for k, sc in US_SCEN.items():
        df = run(e, sc, verbose=(k=='modest'))
        res.append(table(e, df, k))
    print(pd.concat(res, axis=1).round(1).to_string())
