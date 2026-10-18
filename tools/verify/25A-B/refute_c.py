import sympy as sp
from math import comb
from fractions import Fraction as Fr
p, q = sp.symbols('p q')
Q1 = p**2*(2*p**3-5*p**2+2*p+2)
claim1 = p*(2*p-p**2)**2+(1-p)*(2*p**2-p**4)
print("Q1 diff", sp.expand(Q1-claim1))
Q2 = 2*p**5*q**2-4*p**4*q**2-p**4*q+p**3*q**2+p**3*q+p**2*q**2+p**2*q
claim2 = q**2*p**2*(1+p-4*p**2+2*p**3)+q*p**2*(1+p-p**2)
print("Q2 diff", sp.expand(Q2-claim2), " alt form", sp.expand(Q2-(q**2*claim1+p**2*q*(1-q)*(1+p-p**2))))
# 4c four-term expansion
c4 = p*q*(2*p-p**2)**2*q+(1-p)*(1-q)*p**2*q+p*(1-q)*p*q*(2*p-p**2)+q*(1-p)*q*(2*p**2-p**4)
print("4c diff", sp.expand(c4-Q2))
# Q5d intermediate identity, exact with hypergeometric X ~ draws n-1 from N with D red
for N, D, n in [(12, 5, 4), (9, 4, 3), (10, 6, 5), (8, 3, 2)]:
    pk = {k: Fr(comb(D, k)*comb(N-D, n-1-k), comb(N, n-1)) for k in range(0, n)}
    EX = sum(k*v for k, v in pk.items()); EX2 = sum(k*k*v for k, v in pk.items())
    lhs = D*(D-1)-(2*D-1)*EX+EX2
    rhs = Fr(D*(D-1)*(N-n)*(N-n+1), N*(N-1))
    print(N, D, n, lhs == rhs, "VarX formula:", EX2-EX**2 == Fr((n-1)*D*(N-D)*(N-n+1), N*N*(N-1)))
