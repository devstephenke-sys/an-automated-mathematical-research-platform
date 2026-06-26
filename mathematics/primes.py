"""
Prime Number Analysis
"""

from functools import lru_cache
from typing import List

@lru_cache(maxsize=10000)
def is_prime(n: int) -> bool:
    """Check if n is prime"""
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(n ** 0.5) + 1, 2):
        if n % i == 0:
            return False
    return True

def sieve_of_eratosthenes(limit: int) -> List[int]:
    """Get all primes up to limit"""
    if limit < 2:
        return []
    
    sieve = [True] * (limit + 1)
    sieve[0] = sieve[1] = False
    
    for i in range(2, int(limit ** 0.5) + 1):
        if sieve[i]:
            for j in range(i * i, limit + 1, i):
                sieve[j] = False
    
    return [i for i, is_p in enumerate(sieve) if is_p]

@lru_cache(maxsize=10000)
def next_prime(n: int) -> int:
    """Find the next prime after n"""
    candidate = n + 1
    while not is_prime(candidate):
        candidate += 1
    return candidate

@lru_cache(maxsize=10000)
def prev_prime(n: int) -> int:
    """Find the previous prime before n"""
    candidate = n - 1
    while candidate >= 2 and not is_prime(candidate):
        candidate -= 1
    return candidate if candidate >= 2 else None

def prime_gap(n: int) -> int:
    """Distance to the next prime"""
    if not is_prime(n):
        return None
    return next_prime(n) - n

@lru_cache(maxsize=10000)
def is_mersenne_prime(p: int) -> bool:
    """Check if 2^p - 1 is prime (assuming p is prime)"""
    if not is_prime(p):
        return False
    mersenne_primes_exponents = [
        2, 3, 5, 7, 13, 19, 31, 61, 89, 107, 127, 521, 607, 1279, 2203, 2281, 3217, 
        4253, 4423, 9689, 9941, 11213, 19937, 21701, 23209, 44497, 86243, 110503, 132049
    ]
    return p in mersenne_primes_exponents

@lru_cache(maxsize=10000)
def largest_prime_factor(n: int) -> int:
    """Get the largest prime factor"""
    if n < 2:
        return None
    factor = None
    while n % 2 == 0:
        factor = 2
        n //= 2
    i = 3
    while i * i <= n:
        while n % i == 0:
            factor = i
            n //= i
        i += 2
    if n > 2:
        factor = n
    return factor

@lru_cache(maxsize=10000)
def smallest_prime_factor(n: int) -> int:
    """Get the smallest prime factor"""
    if n < 2:
        return None
    if n % 2 == 0:
        return 2
    i = 3
    while i * i <= n:
        if n % i == 0:
            return i
        i += 2
    return n

def is_prime_power(n: int) -> bool:
    """Check if n = p^k for some prime p and k >= 1"""
    if n < 2:
        return False
    p = smallest_prime_factor(n)
    temp = n
    while temp % p == 0:
        temp //= p
    return temp == 1
