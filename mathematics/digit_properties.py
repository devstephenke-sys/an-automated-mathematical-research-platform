"""
Digit Analysis Module
All operations on decimal digits
"""

from collections import Counter
from typing import Dict, List

def digits_of(n: int) -> List[int]:
    """Get list of digits"""
    return [int(d) for d in str(abs(n))]

def digit_sum(n: int) -> int:
    """Sum of all digits"""
    return sum(digits_of(n))

def digital_root(n: int) -> int:
    """Iteratively sum digits until single digit"""
    while n >= 10:
        n = digit_sum(n)
    return n

def digit_product(n: int) -> int:
    """Product of all digits"""
    result = 1
    for d in digits_of(n):
        result *= d
    return result

def digit_count(n: int) -> int:
    """Number of digits"""
    return len(str(abs(n)))

def digit_statistics(n: int) -> Dict:
    """Extract comprehensive digit statistics"""
    digits = digits_of(n)
    s = str(abs(n))
    
    return {
        'count': len(digits),
        'sum': sum(digits),
        'product': digit_product(n),
        'mean': sum(digits) / len(digits) if digits else 0,
        'median': sorted(digits)[len(digits)//2] if digits else 0,
        'min': min(digits) if digits else 0,
        'max': max(digits) if digits else 0,
        'range': (max(digits) - min(digits)) if digits else 0,
        'variance': sum((d - sum(digits)/len(digits))**2 for d in digits) / len(digits) if digits else 0,
        'std_dev': (sum((d - sum(digits)/len(digits))**2 for d in digits) / len(digits)) ** 0.5 if digits else 0,
    }

def digit_frequency(n: int) -> Dict[int, int]:
    """Count frequency of each digit"""
    digits = digits_of(n)
    return dict(Counter(digits))

def digit_types(n: int) -> Dict[str, int]:
    """Count digit types: odd, even, prime, composite, zero"""
    s = str(abs(n))
    return {
        'odd': sum(1 for d in s if int(d) % 2 == 1),
        'even': sum(1 for d in s if int(d) % 2 == 0),
        'prime': sum(1 for d in s if int(d) in {2, 3, 5, 7}),
        'composite': sum(1 for d in s if int(d) in {4, 6, 8, 9}),
        'zero': s.count('0'),
        'one': s.count('1'),
    }

def digit_distinctness(n: int) -> int:
    """Number of distinct digits"""
    return len(set(str(abs(n))))

def has_repeated_digits(n: int) -> bool:
    """Check if n has any repeated digits"""
    s = str(abs(n))
    return len(s) != len(set(s))

def longest_digit_run(n: int) -> int:
    """Length of longest run of identical consecutive digits"""
    s = str(abs(n))
    if not s:
        return 0
    max_run = 1
    current_run = 1
    for i in range(1, len(s)):
        if s[i] == s[i-1]:
            current_run += 1
            max_run = max(max_run, current_run)
        else:
            current_run = 1
    return max_run

def digit_entropy(n: int) -> float:
    """Shannon entropy of digit distribution"""
    s = str(abs(n))
    length = len(s)
    if length == 0:
        return 0
    
    freq = Counter(s)
    entropy = 0
    for count in freq.values():
        p = count / length
        if p > 0:
            entropy -= p * (p ** 0.5)
    
    return entropy

def is_pandigital(n: int) -> bool:
    """Check if n contains all digits 0-9"""
    return len(set(str(abs(n)))) == 10

def is_repdigit(n: int) -> bool:
    """Check if all digits are the same"""
    s = str(abs(n))
    return len(set(s)) == 1

def digit_position_value(n: int) -> Dict:
    """Analyze position values of digits"""
    s = str(abs(n))
    positions = {}
    for i, digit in enumerate(reversed(s)):
        pos = 10 ** i
        positions[i] = {'digit': int(digit), 'position_value': int(digit) * pos}
    return positions
