# Phase 2 numeric checks: bounded-section inequality, the two sphere parameters, converse.
import numpy as np
rng=np.random.default_rng(1)
def unit(v): return v/np.linalg.norm(v)
bad=0; ntests=0; maxerr=0; agree=0; conv_err=0
for trial in range(2000):
    V=rng.normal(size=3); u=unit(rng.normal(size=3)); n=unit(rng.normal(size=3))
    al=rng.uniform(0.05,np.pi/2-0.05); k,s=np.cos(al),np.sin(al)
    p0=rng.normal(size=3)*3; m=u@n; c=(p0-V)@n
    # sample generators, see if the plane meets every generator of the nappe at tau>0
    e1=unit(np.cross(u,rng.normal(size=3))); e2=np.cross(u,e1)
    th=np.linspace(0,2*np.pi,721)
    W=k*u[None,:]+s*(np.cos(th)[:,None]*e1+np.sin(th)[:,None]*e2)
    wn=W@n
    with np.errstate(divide='ignore'): tau=c/wn
    bounded_closed_curve = np.all(tau>0)   # every generator hits plane on the nappe
    pred = (abs(m)>s) and (m*c>0)
    agree += (bounded_closed_curve==pred); ntests+=1
    if abs(m)>s and m*c>0:
        d1=c/(m+s); d2=c/(m-s)
        if m<0: d1,d2=d2,d1
        # tangency |<V+d u - p0, n>| = d s
        for d in (d1,d2):
            C=V+d*u; maxerr=max(maxerr,abs(abs((C-p0)@n)-d*s))
        assert 0<d1<d2
        # orient n so that m>0 for the dandelin formulas
        nn = n if m>0 else -n
        F1=V+d1*u+d1*s*nn; F2=V+d2*u-d2*s*nn
        # projections of centres onto plane
        for d,F in ((d1,F1),(d2,F2)):
            C=V+d*u; P=C-((C-p0)@n)*n; maxerr=max(maxerr,np.linalg.norm(P-F))
        # section sum
        X=V+tau[:,None]*W
        S=np.linalg.norm(X-F1,axis=1)+np.linalg.norm(X-F2,axis=1)
        maxerr=max(maxerr,np.max(abs(S-(d2-d1)*k)))
        # converse: random point of the ellipse in the plane -> on cone
        a=rng.normal(size=3); a=unit(a-(a@n)*n)
        # point X=F1+r a with |X-F1|+|X-F2|=D, solve for r>0 by bisection
        D=(d2-d1)*k; f=lambda r: r+np.linalg.norm(F1+r*a-F2)-D
        lo,hi=0,D
        for _ in range(200):
            mid=(lo+hi)/2
            lo,hi=(mid,hi) if f(mid)<0 else (lo,mid)
        X=F1+lo*a; conv_err=max(conv_err,abs((X-V)@u-k*np.linalg.norm(X-V)))
print("inequality prediction agreement",agree,"/",ntests)
print("max tangency/sum error",maxerr,"converse cone error",conv_err)
