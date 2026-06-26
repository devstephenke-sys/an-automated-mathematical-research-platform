"""
Core Analyzer - Orchestrates feature extraction, pattern finding, and conjecture generation
"""

from typing import Dict, List, Any
from engine.feature_extractor import FeatureExtractor
from engine.pattern_finder import PatternFinder
from engine.conjecture_engine import ConjectureEngine
from database.database import DiscoveryDatabase
from data.sequences import PerfectNumbers, MersenneNumbers
import config
import hashlib

class MathAnalyzer:
    """Main analysis orchestrator"""
    
    def __init__(self):
        self.db = DiscoveryDatabase(str(config.DATABASE_PATH))
        self.feature_extractor = FeatureExtractor()
        self.pattern_finder = PatternFinder()
        self.conjecture_engine = ConjectureEngine()
    
    def analyze_number_set(self, numbers: List[int], set_name: str = "Numbers",
                          use_cache: bool = True) -> Dict[str, Any]:
        """Comprehensive analysis of a number set"""
        
        # Generate cache key
        cache_key = self._generate_hash(numbers)
        
        # Check cache
        if use_cache:
            cached = self.db.get_cached_analysis(cache_key)
            if cached:
                print(f"Using cached analysis for {set_name}")
                all_features = cached['features']
                patterns = cached['patterns']
                features_by_name = {}
                for num_str, features in all_features.items():
                    num = int(num_str)
                    for fname, fvalue in features.items():
                        features_by_name.setdefault(fname, []).append(fvalue)

                conjectures = self.conjecture_engine.generate_from_patterns(patterns, numbers)
                conjectures.extend(self.conjecture_engine.generate_novel_conjectures(numbers, set_name))
                conjectures = self.conjecture_engine.rank_conjectures(conjectures)

                return {
                    'set_name': set_name,
                    'number_count': len(numbers),
                    'numbers': numbers,
                    'features': all_features,
                    'feature_summary': features_by_name,
                    'patterns': patterns,
                    'conjectures': conjectures,
                    'total_features_extracted': len(features_by_name),
                }

        print(f"Analyzing {len(numbers)} numbers from {set_name}...")

        # Extract features for all numbers
        all_features = {}
        features_by_name = {}
        
        print("  Extracting features...")
        for i, num in enumerate(numbers):
            features = self.feature_extractor.extract_all(num)
            all_features[num] = features
            
            # Organize by feature name
            for fname, fvalue in features.items():
                if fname not in features_by_name:
                    features_by_name[fname] = []
                features_by_name[fname].append(fvalue)
        
        print(f"  Extracted {len(features_by_name)} features per number")
        
        # Find patterns
        print("  Finding patterns...")
        patterns = self.pattern_finder.find_all_patterns(numbers, features_by_name)
        
        # Generate conjectures
        print("  Generating conjectures...")
        conjectures = self.conjecture_engine.generate_from_patterns(patterns, numbers)
        conjectures.extend(self.conjecture_engine.generate_novel_conjectures(numbers, set_name))
        conjectures = self.conjecture_engine.rank_conjectures(conjectures)
        
        analysis_result = {
            'set_name': set_name,
            'number_count': len(numbers),
            'numbers': numbers,
            'features': all_features,
            'feature_summary': features_by_name,
            'patterns': patterns,
            'conjectures': conjectures,
            'total_features_extracted': len(features_by_name),
        }
        
        # Cache result
        self.db.cache_analysis(cache_key, set_name, all_features, patterns)
        
        return analysis_result
    
    def analyze_perfect_numbers(self) -> Dict[str, Any]:
        """Analyze known perfect numbers"""
        perfect_nums = PerfectNumbers.get_all()
        return self.analyze_number_set(perfect_nums, "Perfect Numbers")
    
    def analyze_mersenne_numbers(self) -> Dict[str, Any]:
        """Analyze Mersenne exponents"""
        mersenne_exponents = MersenneNumbers.get_exponents()
        return self.analyze_number_set(mersenne_exponents, "Mersenne Exponents")
    
    def generate_report(self, analysis: Dict[str, Any]) -> str:
        """Generate a comprehensive report from analysis"""
        report = []
        report.append("=" * 120)
        report.append(f"MATHEMATICAL DISCOVERY REPORT: {analysis['set_name']}")
        report.append("=" * 120)
        
        report.append(f"\nNumber Count: {analysis['number_count']}")
        report.append(f"Features Extracted: {analysis['total_features_extracted']}")
        report.append(f"Numbers Analyzed: {analysis['numbers'][:5]}{'...' if len(analysis['numbers']) > 5 else ''}")
        
        # Patterns section
        report.append("\n" + "=" * 120)
        report.append("DISCOVERED PATTERNS")
        report.append("=" * 120)
        
        all_patterns = []
        for pattern_type, pattern_list in analysis['patterns'].items():
            all_patterns.extend(pattern_list)
        
        if all_patterns:
            for i, pattern in enumerate(all_patterns[:20], 1):
                report.append(f"\nPattern {i}: {pattern.get('type', 'unknown').upper()}")
                report.append(f"  Description: {pattern.get('description', pattern.get('statement', 'N/A'))}")
                if 'correlation' in pattern:
                    report.append(f"  Correlation: {pattern['correlation']:.4f}")
                if 'evidence_count' in pattern:
                    report.append(f"  Evidence: {pattern['evidence_count']} cases")
        else:
            report.append("No patterns found.")
        
        # Top conjectures
        report.append("\n" + "=" * 120)
        report.append("TOP CONJECTURES")
        report.append("=" * 120)
        
        top_conjectures = analysis['conjectures'][:10]
        for conj in top_conjectures:
            report.append(f"\nConjecture #{conj['id']}: {conj['statement']}")
            report.append(f"  Type: {conj['type']}")
            report.append(f"  Confidence: {conj['confidence']:.1f}%")
            report.append(f"  Complexity: {conj['complexity']}")
            report.append(f"  Novelty: {conj['novelty']}")
            report.append(f"  Quality Score: {conj['quality_score']:.1f}")
        
        report.append("\n" + "=" * 120)
        return "\n".join(report)
    
    def _generate_hash(self, numbers: List[int]) -> str:
        """Generate hash of number set for caching"""
        combined = ",".join(str(n) for n in numbers)
        return hashlib.md5(combined.encode()).hexdigest()
    
    def print_summary(self, analysis: Dict[str, Any]):
        """Print a summary of analysis"""
        print(self.generate_report(analysis))
        
        # Also save to file
        report_file = config.REPORTS_DIR / f"{analysis['set_name'].replace(' ', '_')}_report.txt"
        with open(report_file, 'w') as f:
            f.write(self.generate_report(analysis))
        print(f"\nReport saved to: {report_file}")
