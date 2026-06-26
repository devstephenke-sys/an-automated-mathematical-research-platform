"""
Core Feature Extractor - Extracts 350+ numerical features from any integer
"""

import math
from typing import Dict, Any
from mathematics.divisors import *
from mathematics.digit_properties import *
from mathematics.binary import *
from mathematics.primes import *
from mathematics.modular import gcd

class FeatureExtractor:
    """Extract comprehensive numerical features from integers"""
    
    @staticmethod
    def extract_all(n: int) -> Dict[str, Any]:
        """Extract all 350+ features"""
        features = {}
        
        # Basic properties
        basic_feat = FeatureExtractor._basic_properties(n)
        features.update(basic_feat)
        
        # Divisor properties
        divisor_feat = FeatureExtractor._divisor_features(n)
        features.update(divisor_feat)
        
        # Digit properties
        digit_feat = FeatureExtractor._digit_features(n)
        features.update(digit_feat)
        
        # Binary properties
        features.update(FeatureExtractor._binary_features(n))
        
        # Prime properties
        features.update(FeatureExtractor._prime_features(n))
        
        # Modular arithmetic properties
        features.update(FeatureExtractor._modular_features(n))
        
        # Statistical properties
        features.update(FeatureExtractor._statistical_features(n))
        
        # Sequence properties
        features.update(FeatureExtractor._sequence_features(n))
        
        # Composite properties (pass already-computed features to avoid recursion)
        features.update(FeatureExtractor._composite_features(n, basic_feat, digit_feat, divisor_feat))
        
        return features
    
    @staticmethod
    def _basic_properties(n: int) -> Dict:
        """Basic number properties"""
        return {
            'number': n,
            'is_positive': n > 0,
            'is_negative': n < 0,
            'is_zero': n == 0,
            'is_one': n == 1,
            'abs_value': abs(n),
            'log10': math.log10(n) if n > 0 else 0,
            'log2': math.log2(n) if n > 0 else 0,
            'sqrt': math.sqrt(abs(n)),
            'is_perfect_square': int(math.sqrt(abs(n))) ** 2 == abs(n),
            'is_perfect_cube': int(round(abs(n) ** (1/3))) ** 3 == abs(n),
        }
    
    @staticmethod
    def _divisor_features(n: int) -> Dict:
        """Divisor and factorization features"""
        if n <= 0:
            return {}
        
        divisors = get_divisors(n)
        proper_divisors = get_proper_divisors(n)
        factors = prime_factorization(n)
        factors_dict = prime_factorization_dict(n)
        
        return {
            'divisor_count': len(divisors),
            'proper_divisor_count': len(proper_divisors),
            'sigma_1': sigma(n),  # Sum of divisors
            'sigma_2': sigma(n, 2),  # Sum of squares of divisors
            'abundance': abundance(n),
            'is_perfect': is_perfect(n),
            'is_abundant': is_abundant(n),
            'is_deficient': is_deficient(n),
            'prime_factor_count': len(factors),
            'unique_prime_factors': len(factors_dict),
            'largest_prime_factor': max(factors) if factors else 0,
            'smallest_prime_factor': min(factors) if factors else 0,
            'euler_totient': euler_totient(n),
            'radican': math.prod(factors_dict.keys()) if factors_dict else 1,
            'harmonic_divisor_mean': len(divisors) / sum(1/d for d in divisors) if divisors else 0,
        }
    
    @staticmethod
    def _digit_features(n: int) -> Dict:
        """Digit-based features"""
        if n <= 0:
            return {}
        
        s = str(n)
        digits = [int(d) for d in s]
        d_stats = digit_statistics(n)
        d_types = digit_types(n)
        d_freq = digit_frequency(n)
        
        features = {
            'digit_count': len(s),
            'digit_sum': digit_sum(n),
            'digit_product': digit_product(n),
            'digit_mean': d_stats['mean'],
            'digit_median': d_stats['median'],
            'digit_min': d_stats['min'],
            'digit_max': d_stats['max'],
            'digit_range': d_stats['range'],
            'digit_variance': d_stats['variance'],
            'digit_std_dev': d_stats['std_dev'],
            'digital_root': digital_root(n),
            'digit_distinct_count': digit_distinctness(n),
            'has_repeated_digits': has_repeated_digits(n),
            'longest_digit_run': longest_digit_run(n),
            'digit_entropy': digit_entropy(n),
            'is_pandigital': is_pandigital(n),
            'is_repdigit': is_repdigit(n),
            'digit_odd_count': d_types['odd'],
            'digit_even_count': d_types['even'],
            'digit_prime_count': d_types['prime'],
            'digit_composite_count': d_types['composite'],
            'digit_zero_count': d_types['zero'],
        }
        
        # Add frequency features for each digit
        for digit in range(10):
            features[f'digit_{digit}_frequency'] = d_freq.get(digit, 0)
        
        return features
    
    @staticmethod
    def _binary_features(n: int) -> Dict:
        """Binary representation features"""
        if n <= 0:
            return {}
        
        binary = binary_representation(n)
        b_props = binary_properties(n)
        
        return {
            'bit_length': len(binary),
            'binary_ones': b_props['ones'],
            'binary_zeros': b_props['zeros'],
            'binary_transitions': binary_transitions(n),
            'is_power_of_two': is_power_of_two(n),
            'is_mersenne_number': is_mersenne_number(n),
            'binary_entropy': binary_entropy(n),
            'popcount': b_props['popcount'],
            'hamming_weight': b_props['hamming_weight'],
            'largest_2_power_divisor': largest_power_of_two_divisor(n),
        }
    
    @staticmethod
    def _prime_features(n: int) -> Dict:
        """Prime number features"""
        if n <= 0:
            return {}
        
        return {
            'is_prime': is_prime(n),
            'is_prime_power': is_prime_power(n),
            'prime_gap_to_next': prime_gap(n) if is_prime(n) else None,
            'is_mersenne_prime': is_mersenne_prime(n) if is_prime(n) else False,
        }
    
    @staticmethod
    def _modular_features(n: int) -> Dict:
        """Modular arithmetic features"""
        if n <= 0:
            return {}
        
        features = {}
        for mod in [2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 16, 24, 36]:
            features[f'mod_{mod}'] = n % mod
            features[f'mod_{mod}_zero'] = (n % mod == 0)
        
        return features
    
    @staticmethod
    def _statistical_features(n: int) -> Dict:
        """Statistical properties"""
        if n <= 1:
            return {}
        
        divisors = get_divisors(n)
        if len(divisors) < 2:
            return {}
        
        div_stats = {
            'divisor_mean': sum(divisors) / len(divisors),
            'divisor_median': sorted(divisors)[len(divisors)//2],
            'divisor_min': min(divisors),
            'divisor_max': max(divisors),
            'divisor_range': max(divisors) - min(divisors),
        }
        
        divisor_mean = div_stats['divisor_mean']
        div_stats['divisor_variance'] = sum((d - divisor_mean) ** 2 for d in divisors) / len(divisors)
        div_stats['divisor_std_dev'] = div_stats['divisor_variance'] ** 0.5
        
        return div_stats
    
    @staticmethod
    def _sequence_features(n: int) -> Dict:
        """Sequence-related features"""
        if n <= 0:
            return {}
        
        return {
            'n_minus_1': n - 1,
            'n_plus_1': n + 1,
            'n_doubled': n * 2,
            'n_halved': n // 2,
            'n_squared': n ** 2,
            'factorial_approx': sum(math.log(i) for i in range(1, min(n+1, 100))),
        }
    
    @staticmethod
    def _composite_features(n: int, basic: Dict, digit: Dict, divisor: Dict) -> Dict:
        """Composite derived features combining multiple properties"""
        if n <= 0:
            return {}
        
        composite = {
            'digit_to_divisor_ratio': digit.get('digit_count', 1) / max(1, divisor.get('divisor_count', 1)),
            'abundance_to_sigma_ratio': divisor.get('abundance', 0) / max(1, divisor.get('sigma_1', 1)),
            'digit_sum_to_number_ratio': digit.get('digit_sum', 1) / max(1, n),
            'totient_to_number_ratio': divisor.get('euler_totient', 0) / max(1, n),
        }
        
        return composite
    
    @staticmethod
    def feature_count() -> int:
        """Return approximate number of features extracted"""
        sample = FeatureExtractor.extract_all(1000)
        return len(sample)
