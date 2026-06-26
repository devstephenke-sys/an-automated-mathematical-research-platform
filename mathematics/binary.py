"""
Binary Representation Analysis
"""

from typing import Dict

def binary_representation(n: int) -> str:
    """Get binary representation (without '0b' prefix)"""
    return bin(n)[2:]

def binary_properties(n: int) -> Dict:
    """Extract binary properties"""
    binary = binary_representation(n)
    return {
        'binary': binary,
        'bit_length': len(binary),
        'ones': binary.count('1'),
        'zeros': binary.count('0'),
        'is_mersenne_form': binary == '1' * len(binary),
        'leading_zeros_in_byte': 8 - len(binary),
        'hamming_weight': binary.count('1'),
        'popcount': binary.count('1'),
    }

def gray_code(n: int) -> str:
    """Convert n to Gray code"""
    gray = n ^ (n >> 1)
    return bin(gray)[2:]

def binary_entropy(n: int) -> float:
    """Shannon entropy of binary representation"""
    binary = binary_representation(n)
    length = len(binary)
    if length == 0:
        return 0
    ones = binary.count('1')
    zeros = binary.count('0')
    
    entropy = 0
    if ones > 0:
        p_ones = ones / length
        entropy -= p_ones * (p_ones ** 0.5)
    if zeros > 0:
        p_zeros = zeros / length
        entropy -= p_zeros * (p_zeros ** 0.5)
    
    return entropy

def binary_transitions(n: int) -> int:
    """Count number of bit transitions (0->1 or 1->0)"""
    binary = binary_representation(n)
    transitions = 0
    for i in range(len(binary) - 1):
        if binary[i] != binary[i + 1]:
            transitions += 1
    return transitions

def is_power_of_two(n: int) -> bool:
    """Check if n is a power of 2"""
    return n > 0 and (n & (n - 1)) == 0

def is_mersenne_number(n: int) -> bool:
    """Check if n = 2^k - 1 for some k"""
    binary = binary_representation(n)
    return binary == '1' * len(binary)

def largest_power_of_two_divisor(n: int) -> int:
    """Return the largest power of 2 that divides n"""
    if n == 0:
        return 0
    return n & -n
