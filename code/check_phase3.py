# Phase 3 numeric check: |XF| = e * dist(X, l), e = sqrt(1 - <u,n>^2) / cos(alpha)
import numpy as np
rng = np.random.default_rng(3)
def unit(v): return v/np.linalg.norm(v)
def dist_line(X, P, dvec):
    w = X-P; return np.linalg.norm(w - np.dot(w,dvec)*dvec)
maxerr = 0; cnt = 0; types = {'ellipse':0,'parabola':0,'hyperbola':0}
for trial in range(3000):
    V = rng.normal(size=3); u = unit(rng.normal(size=3))
    a = rng.uniform(0.05, np.pi/2-0.05); k, s = np.cos(a), np.sin(a)
    kind = trial % 3
    # plane normal n with prescribed m = <u,n>
    e1 = unit(np.cross(u, rng.normal(size=3)))
    if kind == 0: m = rng.uniform(s, 1.0)*0.999+0.001*s if s<0.998 else s+ (1-s)/2          # ellipse
    elif kind == 1: m = s                                  # parabola
    else: m = rng.uniform(0.0, s-1e-3)                      # hyperbola
    n = m*u + np.sqrt(1-m*m)*e1
    c = rng.uniform(0.3, 3.0)                              # <p0 - V, n>
    p0 = V + c*n
    # tangent axis spheres: |d m - c| = d s
    ds = [c/(m+s)] + ([c/(m-s)] if abs(m-s) > 1e-12 else [])
    ecc = np.sqrt(1-m*m)/k
    for d in ds:
        C = V + d*u; F = C - (np.dot(C-p0,n))*n
        assert abs(np.linalg.norm(C-F) - abs(d)*s) < 1e-9
        # directrix: plane p0,n  ∩  <Y-V,u> = d k^2 ; direction = n x u
        dl = unit(np.cross(n,u))
        # point on l: solve in span(n,u)
        A = np.array([[1, m],[m, 1]]); b = np.array([np.dot(p0-V,n), d*k*k])
        al, be = np.linalg.solve(A,b); P = V + al*n + be*u
        assert abs(np.dot(P-p0,n))<1e-9 and abs(np.dot(P-V,u)-d*k*k)<1e-9
        for _ in range(8):
            # random generator of the nappe hitting the plane at positive parameter
            g = unit(rng.normal(size=3)); g = unit(g - np.dot(g,u)*u); w = k*u + s*g
            wn = np.dot(w,n)
            if abs(wn) < 1e-9: continue
            t = c/wn
            if t <= 0: continue
            X = V + t*w
            lhs = np.linalg.norm(X-F); rhs = ecc*dist_line(X,P,dl)
            err = abs(lhs-rhs)/max(1,lhs); maxerr = max(maxerr, err); cnt += 1
            # also h / sqrt(1-m^2) formula
            h = np.dot(X-V,u) - d*k*k
            assert abs(dist_line(X,P,dl) - abs(h)/np.sqrt(1-m*m)) < 1e-7*max(1,abs(h))
    types[['ellipse','parabola','hyperbola'][kind]] += 1
    assert (ecc < 1) == (s < abs(m)) or kind == 1
print("points", cnt, "max rel err", maxerr, types)
