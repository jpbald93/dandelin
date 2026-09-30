"""Phase 6 numeric check: directrix converse (all regimes) and apex sections (R^3)."""
import numpy as np
rng = np.random.default_rng(6)
def unit(v): return v / np.linalg.norm(v)
def rand_unit(): return unit(rng.normal(size=3))
fails = {k: 0 for k in ["conv_iff", "nappe_ell_par", "hyp_other_nappe", "apex_point",
                        "apex_line", "apex_lines_on", "apex_lines_cover"]}
counts = {k: 0 for k in fails}
maxres = 0.0
def infdist_directrix(X, V, u, n, b):
    m = u @ n
    return abs((X - V) @ u - b) / np.sqrt(1 - m * m)
def cone2(X, V, u, k): return ((X - V) @ u) ** 2 - k * k * np.linalg.norm(X - V) ** 2
for trial in range(3000):
    V = rng.normal(size=3); u = rand_unit(); n = rand_unit()
    al = rng.uniform(0.1, 1.4); k, s = np.cos(al), np.sin(al)
    if trial % 10 == 0:  # force parabola
        # n with |<u,n>| = s: n = ±(s u + k w), w ⟂ u unit
        w = unit(np.cross(u, rand_unit())); n = (s * u + k * w) * rng.choice([-1, 1])
    m = u @ n
    p0 = V + rng.normal() * 2 * n + np.cross(n, rng.normal(size=3))
    c = (p0 - V) @ n
    # --- converse: tangent axis spheres d with |d m - c| = |d| s
    ds = []
    for sg in (1, -1):
        den = m - sg * s
        if abs(den) > 1e-9: ds.append(c / den)
    ds = [d for d in ds if abs(abs(d * m - c) - abs(d) * s) < 1e-9 * (1 + abs(d))]
    # random points of plane
    e1 = unit(np.cross(n, rand_unit())); e2 = np.cross(n, e1)
    for d in ds:
        C = V + d * u; F = C - ((C - p0) @ n) * n
        b = d * k * k
        for _ in range(20):
            X = p0 + rng.normal() * 3 * e1 + rng.normal() * 3 * e2
            lhs = np.linalg.norm(X - F); rhs = np.sqrt(1 - m * m) / k * infdist_directrix(X, V, u, n, b)
            # iff: relation <=> cone2; equivalent polynomial: (k|XF|)^2 - (<X-V,u>-b)^2 = -(cone2)
            poly = (k * lhs) ** 2 - ((X - V) @ u - b) ** 2
            res = abs(poly + cone2(X, V, u, k))
            maxres = max(maxres, res / (1 + np.linalg.norm(X - V) ** 2))
            counts["conv_iff"] += 1
            if res > 1e-8 * (1 + np.linalg.norm(X - V) ** 2): fails["conv_iff"] += 1
        # construct points satisfying the relation: points on cone2 ∩ plane via generators
        for _ in range(20):
            e = unit(np.cross(u, rand_unit())); w = k * u + s * e
            if abs(w @ n) < 1e-6: continue
            for wdir in (w, -w):
                t = c / (wdir @ n); X = V + t * wdir
                lhs = np.linalg.norm(X - F); rhs = np.sqrt(1 - m * m) / k * infdist_directrix(X, V, u, n, b)
                if abs(lhs - rhs) > 1e-7 * (1 + lhs): continue
                on_up = abs((X - V) @ u - k * np.linalg.norm(X - V)) < 1e-7 * (1 + np.linalg.norm(X - V))
                if abs(m) >= s - 1e-12 and m * c > 0:
                    counts["nappe_ell_par"] += 1
                    if not on_up: fails["nappe_ell_par"] += 1
                if abs(m) < s and (X - V) @ u < -1e-6:
                    counts["hyp_other_nappe"] += 1  # relation holds, lower nappe, not on upper
                    if on_up: fails["hyp_other_nappe"] += 1
    # --- apex: plane through V
    q = V + np.cross(n, rng.normal(size=3))
    a = u - m * n
    if abs(m) > s + 1e-9:
        for _ in range(20):
            X = V + rng.normal() * e1 + rng.normal() * e2
            counts["apex_point"] += 1
            if abs(cone2(X, V, u, k)) < 1e-9 and np.linalg.norm(X - V) > 1e-6: fails["apex_point"] += 1
    # parabola apex
    if trial % 10 == 0:
        for _ in range(20):
            t = rng.normal() * 3
            counts["apex_line"] += 1
            X = V + t * a
            if abs(cone2(X, V, u, k)) > 1e-9 * (1 + t * t) or abs((X - V) @ n) > 1e-9: fails["apex_line"] += 1
            # a point off the line in the plane is not on the cone
            Y = X + (0.5 + rng.random()) * unit(np.cross(n, a))
            if abs(cone2(Y, V, u, k)) < 1e-9: fails["apex_line"] += 1
    if abs(m) < s - 1e-9:
        f = unit(np.cross(u, n)); rho = np.sqrt((1 - m * m) * (s * s - m * m)) / k
        for sg in (1, -1):
            for _ in range(10):
                t = rng.normal() * 3; X = V + t * (a + sg * rho * f)
                counts["apex_lines_on"] += 1
                if abs(cone2(X, V, u, k)) > 1e-9 * (1 + t * t) or abs((X - V) @ n) > 1e-9:
                    fails["apex_lines_on"] += 1
        # cover: solve cone2 on circle of directions in plane; roots must match ±rho
        th = np.linspace(0, np.pi, 20001)
        dirs = np.outer(np.cos(th), unit(a)) + np.outer(np.sin(th), f)
        vals = (dirs @ u) ** 2 - k * k
        roots = np.sum(np.sign(vals[:-1]) != np.sign(vals[1:]))
        counts["apex_lines_cover"] += 1
        if roots != 2: fails["apex_lines_cover"] += 1
for key in fails: print(f"{key:18s} cases={counts[key]:6d} failures={fails[key]}")
print("max relative residual of converse identity:", maxres)
