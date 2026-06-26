"""
Quick Start Demo - MathDiscoveryAI
Run this to see the system in action
"""

from engine.analyzer import MathAnalyzer
from visualization.charts import Visualizer
from data.sequences import PerfectNumbers, MersenneNumbers
import sys

def demo_perfect_numbers():
    """Demo: Analyze perfect numbers"""
    print("\n" + "=" * 100)
    print("DEMO 1: ANALYZING PERFECT NUMBERS")
    print("=" * 100)
    
    analyzer = MathAnalyzer()
    
    # Get perfect numbers
    perfect_nums = PerfectNumbers.get_all()
    print(f"\nAnalyzing {len(perfect_nums)} perfect numbers...")
    print(f"Numbers: {perfect_nums}\n")
    
    # Analyze
    analysis = analyzer.analyze_perfect_numbers()
    
    # Print results
    print(f"Total Features Extracted: {analysis['total_features_extracted']}")
    print(f"\nTotal Patterns Found:")
    for ptype, patterns in analysis['patterns'].items():
        print(f"  {ptype}: {len(patterns)} patterns")
    
    print(f"\nTop 5 Conjectures:")
    for i, conj in enumerate(analysis['conjectures'][:5], 1):
        print(f"\n{i}. {conj['statement']}")
        print(f"   Type: {conj['type']}")
        print(f"   Confidence: {conj['confidence']:.1f}%")
        print(f"   Complexity: {conj['complexity']}")
        print(f"   Quality Score: {conj['quality_score']:.1f}")
    
    return analysis

def demo_mersenne_numbers():
    """Demo: Analyze Mersenne exponents"""
    print("\n" + "=" * 100)
    print("DEMO 2: ANALYZING MERSENNE EXPONENTS")
    print("=" * 100)
    
    analyzer = MathAnalyzer()
    
    # Get Mersenne exponents
    exponents = MersenneNumbers.get_exponents()[:15]
    print(f"\nAnalyzing first 15 Mersenne exponents...")
    print(f"Exponents: {exponents}\n")
    
    # Analyze
    analysis = analyzer.analyze_number_set(exponents, "Mersenne Exponents (First 15)")
    
    print(f"Total Features Extracted: {analysis['total_features_extracted']}")
    print(f"\nTop 3 Conjectures:")
    for i, conj in enumerate(analysis['conjectures'][:3], 1):
        print(f"\n{i}. {conj['statement']}")
        print(f"   Confidence: {conj['confidence']:.1f}%")

def demo_custom_analysis():
    """Demo: Analyze a custom sequence"""
    print("\n" + "=" * 100)
    print("DEMO 3: ANALYZING CUSTOM SEQUENCE (Powers of 2)")
    print("=" * 100)
    
    analyzer = MathAnalyzer()
    
    # Powers of 2
    powers_of_2 = [2**i for i in range(1, 11)]
    print(f"\nAnalyzing powers of 2: {powers_of_2}\n")
    
    analysis = analyzer.analyze_number_set(powers_of_2, "Powers of 2")
    
    print(f"Total Features Extracted: {analysis['total_features_extracted']}")
    print(f"\nTop 2 Conjectures:")
    for i, conj in enumerate(analysis['conjectures'][:2], 1):
        print(f"\n{i}. {conj['statement']}")
        print(f"   Confidence: {conj['confidence']:.1f}%")

def demo_feature_extraction():
    """Demo: Show detailed feature extraction"""
    print("\n" + "=" * 100)
    print("DEMO 4: FEATURE EXTRACTION DETAILS")
    print("=" * 100)
    
    from engine.feature_extractor import FeatureExtractor
    
    extractor = FeatureExtractor()
    
    # Extract features from perfect number 28
    print("\nExtracting 350+ features from perfect number 28...\n")
    features = extractor.extract_all(28)
    
    print(f"Total Features: {len(features)}\n")
    
    # Show sample features
    print("Sample Features:")
    feature_samples = ['number', 'divisor_count', 'sigma_1', 'abundance', 
                      'digit_count', 'digit_sum', 'digital_root',
                      'is_prime', 'bit_length', 'binary_ones', 'euler_totient']
    
    for fname in feature_samples:
        if fname in features:
            print(f"  {fname}: {features[fname]}")

def main():
    """Run all demos"""
    print("=" * 100)
    print("MATHDISCOVERYAI - QUICK START DEMO")
    print("=" * 100)
    
    try:
        # Run demos
        demo_feature_extraction()
        analysis1 = demo_perfect_numbers()
        demo_mersenne_numbers()
        demo_custom_analysis()
        
        # Attempt visualization
        print("\n" + "=" * 100)
        print("DEMO 5: GENERATING VISUALIZATIONS")
        print("=" * 100)
        
        try:
            visualizer = Visualizer()
            print("\nGenerating charts...")
            visualizer.plot_number_growth(analysis1['numbers'], analysis1['set_name'])
            visualizer.plot_conjecture_quality_scores(analysis1)
            print("✓ Visualizations generated successfully!")
        except Exception as e:
            print(f"Note: Visualization requires matplotlib/seaborn: {e}")
        
        # Summary
        print("\n" + "=" * 100)
        print("DEMO COMPLETE")
        print("=" * 100)
        print("\nKey Features Demonstrated:")
        print("✓ 350+ feature extraction per number")
        print("✓ Automatic pattern discovery")
        print("✓ Mathematical conjecture generation")
        print("✓ Confidence-based ranking")
        print("✓ Multiple number sequence analysis")
        print("✓ Visualization generation")
        
        print("\nNext Steps:")
        print("1. Run: python main.py")
        print("2. Explore interactive menu")
        print("3. Analyze your own number sequences")
        print("4. Check reports/ folder for generated reports")
        
    except Exception as e:
        print(f"\nError during demo: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
