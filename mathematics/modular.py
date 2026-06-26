"""
Modular Arithmetic Module
"""

from functools import lru_cache

@lru_cache(maxsize=10000)
def modular_power(base: int, exp: int, mod: int) -> int:
    """Compute (base^exp) mod mod efficiently"""
    result = 1
    base = base % mod
    while exp > 0:
        if exp % 2 == 1:
            result = (result * base) % mod
        exp = exp >> 1
        base = (base * base) % mod
    return result

@lru_cache(maxsize=10000)
def modular_inverse(a: int, m: int) -> int:
    """Find modular multiplicative inverse of a mod m using extended Euclidean algorithm"""
    if gcd(a, m) != 1:
        return None
    
    def extended_gcd(a, b):
        if a == 0:
            return b, 0, 1
        gcd_val, x1, y1 = extended_gcd(b % a, a)
        x = y1 - (b // a) * x1
        y = x1
        return gcd_val, x, y
    
    _, x, _ = extended_gcd(a % m, m)
    return (x % m + m) % m

@lru_cache(maxsize=10000)
def gcd(a: int, b: int) -> int:
    """Greatest common divisor"""
    while b:
        a, b = b, a % b
    return a

def legendre_symbol(a: int, p: int) -> int:
    """Legendre symbol (a/p) for odd prime p"""
    return modular_power(a, (p - 1) // 2, p)

def jacobi_symbol(a: int, n: int) -> int:
    """Jacobi symbol"""
    if n <= 0:
        raise ValueError("n must be positive")
    
    a = a % n
    result = 1
    
    while a != 0:
        while a % 2 == 0:
            a //= 2
            if n % 8 in [3, 5]:
                result = -result
        a, n = n, a
        if a % 4 == 3 and n % 4 == 3:
            result = -result
        a = a % n
    
    if n == 1:
        return result
    else:
        return 0

def congruent_mod(a: int, b: int, mod: int) -> bool:
    """Check if a ≡ b (mod m)"""
    return a % mod == b % mod

def quadratic_residue(a: int, p: int) -> bool:
    """Check if a is a quadratic residue mod p"""
    return legendre_symbol(a, p) == 1

def solve_linear_congruence(a: int, b: int, m: int) -> int:
    """Solve ax ≡ b (mod m) for x"""
    g = gcd(a, m)
    if b % g != 0:
        return None
    
    a //= g
    b //= g
    m //= g
    
    a_inv = modular_inverse(a, m)
    if a_inv is None:
        return None
    
    return (a_inv * b) % m
