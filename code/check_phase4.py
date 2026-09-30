# Phase 4 numeric check: hyperbola case of Dandelin (two-nappe cone).
import numpy as np
rng = np.random.default_rng(4)
def unit(v): return v/np.linalg.norm(v)
maxerr = dict(tan=0, diff=0, const=0, conv=0, dirx=0)
regime_ok = 0; N = 2000; npts = 0
for trial in range(N):
    a = rng.uniform(0.05, np.pi/2-0.05); k, s = np.cos(a), np.sin(a)
    V = rng.normal(size=3); u = unit(rng.normal(size=3)); n = unit(rng.normal(size=3))
    p0 = V + rng.normal(size=3)*2
    m = u@n; c = (p0-V)@n
    # regime test by sampling generators: does plane hit both nappes?
    e1 = unit(np.cross(u, rng.normal(size=3))); e2 = np.cross(u, e1)
    th = rng.uniform(0, 2*np.pi, 400)
    g = k*u[None,:] + s*(np.cos(th)[:,None]*e1 + np.sin(th)[:,None]*e2)
    tau = c/(g@n)   # V + tau g in plane; tau>0 upper nappe, tau<0 lower
    both = (tau > 0).any() and (tau < 0).any()
    pred = abs(m) < s
    regime_ok += (both == pred)
    if not pred:
        continue
    if c < 0: n, m, c = -n, -m, -c
    d1, d2 = c/(m+s), c/(m-s)
    assert d1 > 0 > d2
    C1, C2 = V+d1*u, V+d2*u
    F1, F2 = C1-((C1-p0)@n)*n, C2-((C2-p0)@n)*n
    for C, d in ((C1, d1), (C2, d2)):
        maxerr['tan'] = max(maxerr['tan'], abs(abs((C-p0)@n) - abs(d)*s))
    D = (d1-d2)*k
    maxerr['const'] = max(maxerr['const'], abs(D - 2*c*s*k/(s*s-m*m)))
    e = np.sqrt(1-m*m)/k
    w = unit(u - m*n)
    for tt, X in zip(tau, V+tau[:,None]*g):
        if abs(tt) > 50: continue
        A, B = np.linalg.norm(X-F1), np.linalg.norm(X-F2)
        sgn = np.sign((X-V)@u)
        # upper: B - A = D ; lower: A - B = D
        maxerr['diff'] = max(maxerr['diff'], abs(sgn*(B-A) - D)/max(1,D))
        for F, d in ((F1, d1), (F2, d2)):
            dist_l = abs((X-V)@u - d*k*k)/np.sqrt(1-m*m)
            maxerr['dirx'] = max(maxerr['dirx'], abs(np.linalg.norm(X-F) - e*dist_l)/max(1,np.linalg.norm(X-F)))
        npts += 1
    # converse: random plane points with |A-B| = D: check cone equation (p^2 = k^2 t^2)
    b = unit(np.cross(n, w))
    for _ in range(20):
        # parametrise plane by (x,y) around F1: find points with |A-B|=D by bisection along ray
        phi = rng.uniform(0, 2*np.pi); dirv = np.cos(phi)*w + np.sin(phi)*b
        f = lambda r: abs(np.linalg.norm(F1+r*dirv-F1) - np.linalg.norm(F1+r*dirv-F2)) - D
        lo, hi = 0.0, 1e-3
        # |A-B| - D at r=0 is |F1F2| - D ... find sign change
        rs = np.linspace(0, 100, 2001); vals = [f(r) for r in rs]
        for i in range(2000):
            if vals[i]*vals[i+1] < 0:
                lo, hi = rs[i], rs[i+1]
                for _ in range(80):
                    mid = (lo+hi)/2
                    if f(lo)*f(mid) <= 0: hi = mid
                    else: lo = mid
                X = F1 + lo*dirv; p = (X-V)@u; t = np.linalg.norm(X-V)
                maxerr['conv'] = max(maxerr['conv'], abs(p*p - k*k*t*t)/max(1, t*t))
                break
print("regime prediction |m|<s <=> plane meets both nappes:", regime_ok, "/", N)
print("points tested:", npts)
print({k_: float(v) for k_, v in maxerr.items()})
