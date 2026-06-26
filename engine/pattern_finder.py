"""
Pattern Finder Engine - Discovers mathematical patterns across features
"""

from itertools import combinations
from typing import Dict, List, Tuple
import statistics

class PatternFinder:
    """Discovers relationships and patterns between features"""
    
    @staticmethod
    def find_linear_relationships(numbers: List[int], feature_values: Dict[str, List[float]], 
                                  threshold: float = 0.7) -> List[Dict]:
        """Find linear correlations between features"""
        patterns = []
        features = list(feature_values.keys())
        
        for feat1, feat2 in combinations(features, 2):
            values1 = feature_values[feat1]
            values2 = feature_values[feat2]
            
            # Skip if any have zero variance
            if len(set(values1)) < 2 or len(set(values2)) < 2:
                continue
            
            correlation = PatternFinder._pearson_correlation(values1, values2)
            
            if abs(correlation) >= threshold:
                patterns.append({
                    'type': 'linear_correlation',
                    'feature1': feat1,
                    'feature2': feat2,
                    'correlation': correlation,
                    'strength': 'strong' if abs(correlation) > 0.9 else 'moderate',
                })
        
        return sorted(patterns, key=lambda x: abs(x['correlation']), reverse=True)
    
    @staticmethod
    def find_modular_patterns(numbers: List[int]) -> List[Dict]:
        """Find modular arithmetic patterns"""
        patterns = []
        
        for modulus in [2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 16, 24, 36]:
            remainders = [n % modulus for n in numbers]
            
            # Check if all numbers have same remainder
            if len(set(remainders)) == 1:
                patterns.append({
                    'type': 'modular_uniformity',
                    'modulus': modulus,
                    'remainder': remainders[0],
                    'description': f'All numbers ≡ {remainders[0]} (mod {modulus})',
                    'evidence_count': len(numbers),
                })
            
            # Check for pattern in remainders
            if len(set(remainders)) <= len(set(numbers)) // 2:
                patterns.append({
                    'type': 'modular_constraint',
                    'modulus': modulus,
                    'possible_remainders': sorted(set(remainders)),
                    'evidence_count': len(numbers),
                })
        
        return patterns
    
    @staticmethod
    def find_digit_patterns(numbers: List[int]) -> List[Dict]:
        """Find patterns in digit properties"""
        patterns = []
        
        # Check last digits
        last_digits = [n % 10 for n in numbers]
        if len(set(last_digits)) == 1:
            patterns.append({
                'type': 'digit_ending',
                'digit': last_digits[0],
                'evidence_count': len(numbers),
                'description': f'All numbers end in {last_digits[0]}',
            })
        
        # Check digit count correlation with number
        digit_counts = [len(str(n)) for n in numbers]
        log_values = [n for n in numbers]
        
        if len(set(digit_counts)) > 1:
            corr = PatternFinder._pearson_correlation(digit_counts, log_values)
            if abs(corr) > 0.8:
                patterns.append({
                    'type': 'digit_count_correlation',
                    'correlation': corr,
                    'description': 'Strong correlation between digit count and number magnitude',
                })
        
        return patterns
    
    @staticmethod
    def find_divisor_patterns(numbers: List[int], divisor_counts: List[int]) -> List[Dict]:
        """Find patterns in divisor properties"""
        patterns = []
        
        if len(set(divisor_counts)) > 1:
            avg_divisors = statistics.mean(divisor_counts)
            patterns.append({
                'type': 'divisor_count_distribution',
                'mean': avg_divisors,
                'min': min(divisor_counts),
                'max': max(divisor_counts),
                'description': f'Divisor count ranges from {min(divisor_counts)} to {max(divisor_counts)}',
            })
        
        return patterns
    
    @staticmethod
    def find_binary_patterns(numbers: List[int]) -> List[Dict]:
        """Find patterns in binary representation"""
        patterns = []
        
        binaries = [bin(n)[2:] for n in numbers]
        bit_lengths = [len(b) for b in binaries]
        one_counts = [b.count('1') for b in binaries]
        
        # Check for pattern in ones/zeros ratio
        ratios = []
        for b in binaries:
            zeros = b.count('0')
            ones = b.count('1')
            if zeros > 0:
                ratios.append(ones / (ones + zeros))
        
        if len(set(ratios)) <= 3:
            patterns.append({
                'type': 'binary_ratio_pattern',
                'ratios': sorted(set(ratios)),
                'description': 'Binary representation has concentrated ones/zeros ratios',
            })
        
        return patterns
    
    @staticmethod
    def _pearson_correlation(x: List[float], y: List[float]) -> float:
        """Calculate Pearson correlation coefficient"""
        if len(x) != len(y) or len(x) < 2:
            return 0
        
        mean_x = statistics.mean(x)
        mean_y = statistics.mean(y)
        
        numerator = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(len(x)))
        
        denom_x = sum((xi - mean_x) ** 2 for xi in x) ** 0.5
        denom_y = sum((yi - mean_y) ** 2 for yi in y) ** 0.5
        
        if denom_x == 0 or denom_y == 0:
            return 0
        
        return numerator / (denom_x * denom_y)
    
    @staticmethod
    def find_all_patterns(numbers: List[int], features_dict: Dict[str, List[float]]) -> Dict:
        """Comprehensive pattern discovery"""
        return {
            'linear_relationships': PatternFinder.find_linear_relationships(numbers, features_dict),
            'modular_patterns': PatternFinder.find_modular_patterns(numbers),
            'digit_patterns': PatternFinder.find_digit_patterns(numbers),
            'binary_patterns': PatternFinder.find_binary_patterns(numbers),
        }
