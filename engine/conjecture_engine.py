"""
Conjecture Generator Engine - Generates mathematical conjectures from patterns
"""

from typing import List, Dict, Any
from datetime import datetime

class ConjectureEngine:
    """Generate candidate mathematical conjectures"""
    
    @staticmethod
    def generate_from_patterns(patterns: Dict[str, List[Dict]], 
                               number_set: List[int],
                               metadata: Dict = None) -> List[Dict]:
        """Generate conjectures from discovered patterns"""
        conjectures = []
        conjecture_id = 1
        
        # Linear relationship conjectures
        for pattern in patterns.get('linear_relationships', []):
            if pattern['correlation'] > 0.9:
                conj = {
                    'id': conjecture_id,
                    'type': 'linear_relationship',
                    'statement': f"{pattern['feature1']} and {pattern['feature2']} are strongly correlated",
                    'correlation': pattern['correlation'],
                    'confidence': min(100, abs(pattern['correlation']) * 100),
                    'evidence_count': len(number_set),
                    'complexity': 'low',
                    'novelty': 'medium',
                    'testable': True,
                }
                conjectures.append(conj)
                conjecture_id += 1
        
        # Modular arithmetic conjectures
        for pattern in patterns.get('modular_patterns', []):
            if pattern['type'] == 'modular_uniformity':
                conj = {
                    'id': conjecture_id,
                    'type': 'modular_constraint',
                    'statement': pattern['description'],
                    'modulus': pattern['modulus'],
                    'remainder': pattern['remainder'],
                    'confidence': 100,
                    'evidence_count': pattern['evidence_count'],
                    'complexity': 'low',
                    'novelty': 'high',
                    'testable': True,
                }
                conjectures.append(conj)
                conjecture_id += 1
        
        # Digit pattern conjectures
        for pattern in patterns.get('digit_patterns', []):
            if pattern['type'] == 'digit_ending':
                conj = {
                    'id': conjecture_id,
                    'type': 'digit_property',
                    'statement': pattern['description'],
                    'property': 'final_digit',
                    'confidence': 100,
                    'evidence_count': pattern['evidence_count'],
                    'complexity': 'low',
                    'novelty': 'high',
                    'testable': True,
                }
                conjectures.append(conj)
                conjecture_id += 1
        
        return conjectures
    
    @staticmethod
    def generate_novel_conjectures(number_set: List[int],
                                   set_name: str = "Numbers") -> List[Dict]:
        """Generate novel conjectures specific to a number set"""
        conjectures = []
        conjecture_id = 1000
        
        # Growth rate conjecture
        if len(number_set) > 1:
            growth_rates = []
            for i in range(1, len(number_set)):
                if number_set[i-1] > 0:
                    growth_rates.append(number_set[i] / number_set[i-1])
            
            if growth_rates and all(r > 1 for r in growth_rates):
                conj = {
                    'id': conjecture_id,
                    'type': 'growth_pattern',
                    'statement': f'{set_name} grow exponentially',
                    'growth_rates': growth_rates,
                    'confidence': 85,
                    'evidence_count': len(number_set) - 1,
                    'complexity': 'medium',
                    'novelty': 'high',
                    'testable': True,
                }
                conjectures.append(conj)
                conjecture_id += 1
        
        return conjectures
    
    @staticmethod
    def rank_conjectures(conjectures: List[Dict]) -> List[Dict]:
        """Rank conjectures by quality metrics"""
        for conj in conjectures:
            # Calculate quality score
            score = 0
            score += conj.get('confidence', 50) * 0.4
            
            # Novelty factor
            if conj.get('novelty') == 'high':
                score += 20
            elif conj.get('novelty') == 'medium':
                score += 10
            
            # Testability bonus
            if conj.get('testable'):
                score += 15
            
            # Complexity factor (simpler is better)
            if conj.get('complexity') == 'low':
                score += 10
            elif conj.get('complexity') == 'medium':
                score += 5
            
            # Evidence bonus
            if conj.get('evidence_count', 0) >= 5:
                score += 10
            
            conj['quality_score'] = score
        
        return sorted(conjectures, key=lambda x: x['quality_score'], reverse=True)
    
    @staticmethod
    def format_conjecture(conj: Dict) -> str:
        """Format a conjecture for display"""
        return f"""
Conjecture #{conj['id']}
Statement: {conj['statement']}
Type: {conj['type']}
Confidence: {conj['confidence']:.1f}%
Complexity: {conj['complexity']}
Novelty: {conj['novelty']}
Testable: {'Yes' if conj['testable'] else 'No'}
Evidence: {conj['evidence_count']} cases
Quality Score: {conj['quality_score']:.1f}
"""
