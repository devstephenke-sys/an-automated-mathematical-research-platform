"""
Divisor Analysis Module
All operations related to divisors and factorization
"""

from functools import lru_cache
from typing import List, Tuple, Set, Dict

@lru_cache(maxsize=10000)
def get_divisors(n: int) -> List[int]:
    """Get all divisors of n (including 1 and n itself)"""
    if n < 1:
        return []
    divisors = [1]
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            divisors.append(i)
            if i != n // i:
                divisors.append(n // i)
    divisors.append(n)
    return sorted(set(divisors))

@lru_cache(maxsize=10000)
def get_proper_divisors(n: int) -> List[int]:
    """Get proper divisors (all divisors except n itself)"""
    return sorted([d for d in get_divisors(n) if d != n])

@lru_cache(maxsize=10000)
def sigma(n: int, k: int = 1) -> int:
    """Sum of k-th powers of divisors"""
    divisors = get_divisors(n)
    return sum(d ** k for d in divisors)

@lru_cache(maxsize=10000)
def tau(n: int) -> int:
    """Number of divisors"""
    return len(get_divisors(n))

@lru_cache(maxsize=10000)
def prime_factorization(n: int) -> List[int]:
    """Get prime factorization as a list of prime factors (with repetition)"""
    if n < 2:
        return []
    factors = []
    d = 2
    while d * d <= n:
        while n % d == 0:
            factors.append(d)
            n //= d
        d += 1
    if n > 1:
        factors.append(n)
    return factors

@lru_cache(maxsize=10000)
def prime_factorization_dict(n: int) -> Dict[int, int]:
    """Get prime factorization as a dictionary {prime: exponent}"""
    factors = prime_factorization(n)
    result = {}
    for p in factors:
        result[p] = result.get(p, 0) + 1
    return result

def abundance(n: int) -> int:
    """Abundance = σ(n) - 2n"""
    return sigma(n) - 2 * n

def is_perfect(n: int) -> bool:
    """Check if n is a perfect number"""
    return sigma(n) == 2 * n

def is_abundant(n: int) -> bool:
    """Check if n is abundant (σ(n) > 2n)"""
    return sigma(n) > 2 * n

def is_deficient(n: int) -> bool:
    """Check if n is deficient (σ(n) < 2n)"""
    return sigma(n) < 2 * n

@lru_cache(maxsize=10000)
def gcd(a: int, b: int) -> int:
    """Greatest common divisor using Euclidean algorithm"""
    while b:
        a, b = b, a % b
    return a

@lru_cache(maxsize=10000)
def lcm(a: int, b: int) -> int:
    """Least common multiple"""
    return abs(a * b) // gcd(a, b) if a and b else 0

def is_coprime(a: int, b: int) -> bool:
    """Check if a and b are coprime"""
    return gcd(a, b) == 1

@lru_cache(maxsize=10000)
def euler_totient(n: int) -> int:
    """Euler's totient function φ(n)"""
    result = n
    p = 2
    while p * p <= n:
        if n % p == 0:
            while n % p == 0:
                n //= p
            result -= result // p
        p += 1
    if n > 1:
        result -= result // n
    return result

@lru_cache(maxsize=10000)
def divisor_sum_property(n: int) -> Tuple[int, int, float]:
    """Returns (sum_of_proper_divisors, 2n, ratio)"""
    s = sigma(n) - n
    return s, 2 * n, s / (2 * n) if n > 0 else 0
