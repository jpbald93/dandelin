# Phase 5 numeric check: generator construction, non-emptiness, regime characterisation in R^3.
import numpy as np
rng = np.random.default_rng(5)
def unit(v): return v/np.linalg.norm(v)
stats = dict(ell=0, hyp=0, par=0, err_plane=0.0, err_cone=0.0, ell_bad=0, hyp_bad=0, unb_bad=0, nappe_bad=0)
for trial in range(3000):
    V = rng.normal(size=3); u = unit(rng.normal(size=3)); n = unit(rng.normal(size=3))
    alpha = rng.uniform(0.1, 1.4); k, s = np.cos(alpha), np.sin(alpha)
    if trial % 10 == 0:   # parabola regime: force |<u,n>| = s
        q = unit(np.cross(u, rng.normal(size=3)))
        n = unit(k*q + (s if rng.random()<.5 else -s)*u)
    p0 = rng.normal(size=3); c = (p0-V)@n
    if abs(c) < 1e-3: continue
    m = u@n; q = n - m*u; r = np.linalg.norm(q)
    def gen_point(e):
        w = k*u + s*e; d = w@n; t = c/d; X = V + t*w
        stats['err_plane'] = max(stats['err_plane'], abs((X-p0)@n)/max(1.0, np.linalg.norm(X-V)))
        stats['err_cone'] = max(stats['err_cone'], abs(((X-V)@u)**2 - k**2*np.linalg.norm(X-V)**2)/max(1.0, np.linalg.norm(X-V)**2))
        return X, t
    if abs(abs(m)-s) < 1e-12:
        stats['par'] += 1
    if abs(m) < s - 1e-9:   # hyperbola: e = +- q/r
        stats['hyp'] += 1
        _, t1 = gen_point(q/r); _, t2 = gen_point(-q/r)
        if not (t1*t2 < 0): stats['hyp_bad'] += 1
    elif abs(m) > s + 1e-9:  # ellipse: any e ⟂ u gives the correct nappe (sign(t) = sign(m c))
        stats['ell'] += 1
        for _ in range(20):
            e = unit(np.cross(u, rng.normal(size=3)))
            X, t = gen_point(e)
            if not (t > 0) == (m*c > 0): stats['ell_bad'] += 1
    # unboundedness when |m| <= s: generator with <w,n> = eps small
    if abs(m) <= s + 1e-12:
        f = unit(np.cross(u, n)); R = 1e6
        eps = abs(c)/(R+1) * (1 if k*m >= 0 else -1) * 0.5   # same sign as k m, as in exists_small_eps
        a = (eps - k*m)/(s*r)
        a = float(np.clip(a, -1, 1)) if abs(a) <= 1 + 1e-12 else a
        if abs(a) <= 1:
            e = a*q/r + np.sqrt(1-a*a)*f
            X, t = gen_point(e)
            if not np.linalg.norm(X-V) > R: stats['unb_bad'] += 1
        else: stats['unb_bad'] += 1
    # one-nappe check (|m| >= s): sample section points and check nappe sign
    if abs(m) >= s - 1e-12 and abs(m) > 1e-9:
        for _ in range(20):
            e = unit(np.cross(u, rng.normal(size=3))); w = k*u+s*e
            for sg in (1, -1):
                w2 = k*sg*u + s*e; d = w2@n
                if abs(d) < 1e-12: continue
                t = c/d
                if t > 0:  # point on nappe sg
                    if (sg > 0) != (m*c > 0): stats['nappe_bad'] += 1
print(stats)
