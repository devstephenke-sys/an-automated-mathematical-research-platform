"""
Data Module - Perfect Numbers and Mersenne Sequences
"""

from config import KNOWN_PERFECT_NUMBERS, KNOWN_MERSENNE_EXPONENTS

class PerfectNumbers:
    """Manage perfect number data"""
    
    _cache = {}
    
    @staticmethod
    def get_all() -> list:
        """Get all known perfect numbers"""
        return KNOWN_PERFECT_NUMBERS.copy()
    
    @staticmethod
    def get_by_index(idx: int):
        """Get perfect number by index (0-based)"""
        if 0 <= idx < len(KNOWN_PERFECT_NUMBERS):
            return KNOWN_PERFECT_NUMBERS[idx]
        return None
    
    @staticmethod
    def count() -> int:
        """Get count of known perfect numbers"""
        return len(KNOWN_PERFECT_NUMBERS)
    
    @staticmethod
    def generate_next_mersenne_based(max_exponent: int = 4423) -> list:
        """Generate perfect numbers based on Mersenne exponents"""
        results = []
        for p in KNOWN_MERSENNE_EXPONENTS:
            if p <= max_exponent:
                pn = (2 ** (p - 1)) * ((2 ** p) - 1)
                results.append({'pn': pn, 'exponent': p})
        return results

class MersenneNumbers:
    """Manage Mersenne number data"""
    
    _cache = {}
    
    @staticmethod
    def get_exponents() -> list:
        """Get all known Mersenne prime exponents"""
        return KNOWN_MERSENNE_EXPONENTS.copy()
    
    @staticmethod
    def count() -> int:
        """Get count of known Mersenne primes"""
        return len(KNOWN_MERSENNE_EXPONENTS)
    
    @staticmethod
    def get_by_index(idx: int):
        """Get Mersenne exponent by index"""
        if 0 <= idx < len(KNOWN_MERSENNE_EXPONENTS):
            return KNOWN_MERSENNE_EXPONENTS[idx]
        return None
    
    @staticmethod
    def compute_mersenne_number(exponent: int):
        """Compute 2^p - 1"""
        return (2 ** exponent) - 1
    
    @staticmethod
    def corresponding_perfect_number(exponent: int):
        """Compute corresponding perfect number for Mersenne exponent"""
        return (2 ** (exponent - 1)) * ((2 ** exponent) - 1)

class PrimeNumbers:
    """Manage prime number data"""

    @staticmethod
    def get_first(count: int = 50) -> list:
        """Return the first `count` prime numbers"""
        primes = []
        candidate = 2
        while len(primes) < count:
            is_prime = True
            for p in range(2, int(candidate ** 0.5) + 1):
                if candidate % p == 0:
                    is_prime = False
                    break
            if is_prime:
                primes.append(candidate)
            candidate += 1
        return primes

class FibonacciNumbers:
    """Manage Fibonacci sequence data"""

    @staticmethod
    def get_sequence(count: int = 20) -> list:
        """Return the first `count` Fibonacci numbers"""
        if count <= 0:
            return []
        sequence = [1, 1]
        while len(sequence) < count:
            sequence.append(sequence[-1] + sequence[-2])
        return sequence[:count]

class TriangularNumbers:
    """Manage triangular number data"""

    @staticmethod
    def get_sequence(count: int = 20) -> list:
        """Return the first `count` triangular numbers"""
        return [n * (n + 1) // 2 for n in range(1, count + 1)]

class AmicableNumbers:
    """Manage known amicable number pairs"""

    KNOWN_PAIRS = [
        (220, 284),
        (1184, 1210),
        (2620, 2924),
        (5020, 5564),
        (6232, 6368),
    ]

    @staticmethod
    def get_numbers(limit: int = 10) -> list:
        """Return a flattened list of amicable numbers"""
        numbers = []
        for a, b in AmicableNumbers.KNOWN_PAIRS[:limit]:
            numbers.extend([a, b])
        return numbers

class HighlyCompositeNumbers:
    """Manage highly composite numbers"""

    KNOWN_NUMBERS = [
        1, 2, 4, 6, 12, 24, 36, 48, 60, 120, 180, 240, 360, 720, 840, 1260, 1680, 2520, 5040,
        7560, 10080, 15120, 20160, 25200, 27720, 45360, 50400, 55440, 83160,
    ]

    @staticmethod
    def get_all(limit: int = 20) -> list:
        """Return a list of highly composite numbers"""
        return HighlyCompositeNumbers.KNOWN_NUMBERS[:limit]
