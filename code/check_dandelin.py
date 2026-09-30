"""Numeric check of Dandelin's theorem as formalised in Dandelin/Basic.lean (`dandelin`).
Random cone (apex V, unit axis u, half-angle alpha), random 0<d1<d2, random unit n with
the plane through F1 = V+d1 u+d1 s n containing F2 = V+d2 u-d2 s n; sample points of
plane ∩ cone and check |XF1|+|XF2| = (d2-d1) cos(alpha)."""
import numpy as np
rng = np.random.default_rng(1)
def unit(v): return v / np.linalg.norm(v)
worst = 0.0; ok = 0
for trial in range(300):
    V = rng.normal(size=3); u = unit(rng.normal(size=3))
    al = rng.uniform(0.1, 1.4); k, s = np.cos(al), np.sin(al)
    d1 = rng.uniform(0.2, 3); d2 = d1 + rng.uniform(0.2, 3)
    # need <u,n> = m with (d2-d1) m = s (d1+d2) ... from <F2-F1,n>=0: (d2-d1)m - s(d1+d2) = 0
    m = s * (d1 + d2) / (d2 - d1)
    if m >= 1: continue
    w = unit(np.cross(u, rng.normal(size=3)))
    n = m * u + np.sqrt(1 - m * m) * w
    F1 = V + d1 * u + d1 * s * n; F2 = V + d2 * u - d2 * s * n
    assert abs((F2 - F1) @ n) < 1e-9
    # parametrise generators: X = V + t g, g unit with <g,u>=k; solve <X-F1,n>=0 for t>0
    e1 = w; e2 = np.cross(u, w)
    for phi in np.linspace(0, 2 * np.pi, 60, endpoint=False):
        g = k * u + s * (np.cos(phi) * e1 + np.sin(phi) * e2)
        gn = g @ n
        if abs(gn) < 1e-12: continue
        t = ((F1 - V) @ n) / gn
        if t <= 0: continue
        X = V + t * g
        lhs = np.linalg.norm(X - F1) + np.linalg.norm(X - F2)
        worst = max(worst, abs(lhs - (d2 - d1) * k)); ok += 1
        assert d1 * k - 1e-9 <= t <= d2 * k + 1e-9
print("points checked:", ok, "max error:", worst)
assert worst < 1e-8
