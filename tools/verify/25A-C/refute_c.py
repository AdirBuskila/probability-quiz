import itertools
import sympy as sp
p, q = sp.symbols('p q')
units = {'A': ('L', 'T1'), 'B': ('L', 'B1'), 'E': ('T1', 'B1'), 'C': ('T1', 'T2'), 'D': ('B1', 'B2'),
         'F': ('T2', 'B2'), 'G': ('T2', 'O'), 'H': ('B2', 'O')}

def conn(up):
    adj = {}
    for k in up:
        u, v = units[k]; adj.setdefault(u, set()).add(v); adj.setdefault(v, set()).add(u)
    seen = {'L'}; st = ['L']
    while st:
        u = st.pop()
        for w in adj.get(u, ()):
            if w not in seen: seen.add(w); st.append(w)
    return 'O' in seen

def P(names, prob):
    tot = 0
    for bits in itertools.product([0, 1], repeat=len(names)):
        if conn([n for n, b in zip(names, bits) if b]):
            w = 1
            for n, b in zip(names, bits):
                w *= prob[n] if b else 1-prob[n]
            tot += w
    return sp.expand(tot)

pr = {n: p for n in 'ABCDEFG'}; pr['H'] = q
Q1 = P(list('ABCDEFG'), pr); Q2 = P(list('ABCDEFGH'), pr)
claimQ1 = p**3*(1+2*p-4*p**3+2*p**4)
claimH = p**2*(1+3*p-9*p**3+8*p**4-2*p**5)
claimQ2 = q*claimH+(1-q)*claimQ1
print("Q1 diff", sp.simplify(Q1-claimQ1), "| Q2 diff", sp.simplify(Q2-claimQ2))
print("Q2|q=p:", sp.expand(Q2.subs(q, p)), "claim", sp.expand(p**3*(2+4*p-2*p**2-13*p**3+14*p**4-4*p**5)))
print("Q2|H =", sp.factor(Q2.subs(q, 1)))
# the official's wrong (H with prob p) differs from correct unless q=p
print("official-style (q=p) equals correct Q2 only on q=p:", sp.simplify(Q2.subs(q, p)-Q2))
