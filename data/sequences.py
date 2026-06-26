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
