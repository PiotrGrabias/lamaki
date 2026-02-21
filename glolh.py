from math import gcd

def classical_period(a, N):
    r = 1
    while pow(a, r, N) != 1:
        r += 1
    return r

def factorize_15(N=15):
    for a in range(2, N):
        if gcd(a, N) != 1:
            continue
        r = classical_period(a, N)
        if r % 2 != 0:
            continue
        x = pow(a, r//2, N)
        f1 = gcd(x-1, N)
        f2 = gcd(x+1, N)
        if f1 not in [1, N]:
            return f1, N//f1
        if f2 not in [1, N]:
            return f2, N//f2
    return None

print(factorize_15())
