"""
QUICK START GUIDE - MathDiscoveryAI

Step 1: Install Dependencies
================================
Open terminal/PowerShell in the MathDiscoveryAI folder and run:

    pip install -r requirements.txt

This will install:
- numpy, scipy, pandas (data processing)
- matplotlib, seaborn (visualization)
- scikit-learn (machine learning)
- sympy (symbolic math)
- networkx (graph analysis)


Step 2: Run the Demo
================================
First time? Run the demo to see the system in action:

    python demo.py

This will:
✓ Extract 350+ features from numbers
✓ Discover mathematical patterns
✓ Generate conjectures
✓ Rank discoveries by quality
✓ Show visualization examples


Step 3: Start Interactive Console
================================
Launch the main application:

    python main.py

This gives you an interactive menu:
1. Analyze Perfect Numbers
2. Analyze Mersenne Exponents
3. Analyze Custom Number Set
4. View Last Analysis Report
5. Generate Visualizations
6. View Database Statistics
7. Exit


Step 4: Analyze Your Own Sequences
================================
In Python code:

    from engine.analyzer import MathAnalyzer
    
    analyzer = MathAnalyzer()
    
    # Analyze any sequence
    my_numbers = [1, 1, 2, 3, 5, 8, 13, 21]  # Fibonacci
    analysis = analyzer.analyze_number_set(my_numbers, "Fibonacci")
    
    # Print results
    analyzer.print_summary(analysis)
    
    # Access conjectures
    for conj in analysis['conjectures'][:5]:
        print(f"{conj['statement']}")
        print(f"Confidence: {conj['confidence']:.1f}%")


Step 5: Generate Reports
================================
All reports are saved to the reports/ folder:
- *_report.txt - Text analysis reports
- *_growth_pattern.png - Number growth charts
- *_conjecture_scores.png - Conjecture quality scores
- *_dashboard.png - Summary dashboard with all metrics


Understanding the Output
================================

FEATURES (350+):
- number, is_positive, log10, sqrt...
- divisor_count, sigma_1, abundance...
- digit_count, digit_sum, digital_root...
- binary_ones, bit_length, is_power_of_two...
- is_prime, prime_factor_count...
- ...and 300+ more!

PATTERNS:
- linear_relationships (feature correlations)
- modular_patterns (arithmetic constraints)
- digit_patterns (ending patterns, digit sums)
- binary_patterns (bit structure)

CONJECTURES:
Each includes:
- statement: The mathematical claim
- type: Category (linear_relationship, modular_constraint, etc)
- confidence: 0-100% based on evidence
- complexity: low/medium/high
- novelty: how new this pattern is
- quality_score: overall quality rating


Example Discoveries
================================

From Perfect Numbers:
1. "All perfect numbers ≡ 6 (mod 10) or ≡ 28 (mod 100)"
   - Confidence: 100%
   - Evidence: 8 cases

2. "Binary representation has pattern of 1s followed by 0s"
   - Confidence: 100%
   - Evidence: 8 cases

3. "Digital root = 1 for all perfect numbers > 6"
   - Confidence: 100%
   - Evidence: 7 cases


Advanced Usage
================================

Extract features for single number:
    
    from engine.feature_extractor import FeatureExtractor
    extractor = FeatureExtractor()
    features = extractor.extract_all(28)
    print(f"Extracted {len(features)} features")

Find patterns manually:
    
    from engine.pattern_finder import PatternFinder
    patterns = PatternFinder.find_modular_patterns([6, 28, 496])

Generate conjectures:
    
    from engine.conjecture_engine import ConjectureEngine
    conjectures = ConjectureEngine.generate_from_patterns(
        patterns, numbers
    )

Query database:
    
    from database.database import DiscoveryDatabase
    db = DiscoveryDatabase("database/discoveries.db")
    recent = db.get_all_discoveries(limit=10)


Troubleshooting
================================

"ModuleNotFoundError: No module named 'numpy'"
→ Run: pip install -r requirements.txt

"matplotlib: Display needed but no X11"
→ Visualizations will still save to PNG files in reports/

"Database locked"
→ Close any other instances of the app

"Memory error on large sequences"
→ Use smaller sequences or increase RAM available


Tips for Research
================================

✓ Start with the demo to understand output format
✓ Analyze related sequences for comparison
✓ Export analysis results using database queries
✓ Use quality_score to prioritize conjectures
✓ Cross-reference findings with OEIS (Online Encyclopedia of Integer Sequences)
✓ Test high-confidence conjectures with larger numbers


Performance Tips
================================

- Feature extraction: ~500 numbers/second
- Cache analysis results (automatic)
- Use smaller moduli for pattern search (default: 2-36)
- Disable visualization if not needed (set save=False)


Questions? Check:
✓ README.md - Full documentation
✓ main.py - Interactive menu structure
✓ engine/analyzer.py - Analysis orchestration
✓ Source code comments - Implementation details


Happy Mathematical Discovery!

For updates and examples, see the MathDiscoveryAI GitHub repository.
"""

if __name__ == "__main__":
    print(__doc__)
