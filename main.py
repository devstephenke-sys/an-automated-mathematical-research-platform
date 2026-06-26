"""
Main Application - MathDiscoveryAI Interactive Console
"""

import sys
from typing import List
from engine.analyzer import MathAnalyzer
from visualization.charts import Visualizer
from data.sequences import PerfectNumbers, MersenneNumbers
import config

class MathDiscoveryAI:
    """Main application interface"""
    
    def __init__(self):
        self.analyzer = MathAnalyzer()
        self.visualizer = Visualizer()
        self.last_analysis = None
    
    def run_interactive(self):
        """Start interactive console"""
        print("=" * 120)
        print("WELCOME TO MATHDISCOVERYAI - Automated Mathematical Discovery Platform")
        print("=" * 120)
        print()
        
        while True:
            print("\nMAIN MENU:")
            print("1. Analyze Perfect Numbers")
            print("2. Analyze Mersenne Exponents")
            print("3. Analyze Custom Number Set")
            print("4. View Last Analysis Report")
            print("5. Generate Visualizations")
            print("6. View Database Statistics")
            print("7. Exit")
            
            choice = input("\nEnter your choice (1-7): ").strip()
            
            if choice == '1':
                self.analyze_perfect_numbers()
            elif choice == '2':
                self.analyze_mersenne_numbers()
            elif choice == '3':
                self.analyze_custom_set()
            elif choice == '4':
                self.view_last_report()
            elif choice == '5':
                self.generate_visualizations()
            elif choice == '6':
                self.view_database_stats()
            elif choice == '7':
                print("\nThank you for using MathDiscoveryAI!")
                break
            else:
                print("Invalid choice. Please try again.")
    
    def analyze_perfect_numbers(self):
        """Analyze perfect numbers"""
        print("\n" + "=" * 120)
        print("ANALYZING PERFECT NUMBERS")
        print("=" * 120)
        
        perfect_nums = PerfectNumbers.get_all()
        print(f"Found {len(perfect_nums)} known perfect numbers")
        print(f"Numbers: {perfect_nums}")
        
        self.last_analysis = self.analyzer.analyze_perfect_numbers()
        self.analyzer.print_summary(self.last_analysis)
        
        print(f"\nTop Conjecture: {self.last_analysis['conjectures'][0]['statement']}")
        print(f"Confidence: {self.last_analysis['conjectures'][0]['confidence']:.1f}%")
    
    def analyze_mersenne_numbers(self):
        """Analyze Mersenne exponents"""
        print("\n" + "=" * 120)
        print("ANALYZING MERSENNE EXPONENTS")
        print("=" * 120)
        
        mersenne_exp = MersenneNumbers.get_exponents()
        print(f"Found {len(mersenne_exp)} known Mersenne prime exponents")
        print(f"Exponents: {mersenne_exp[:20]}{'...' if len(mersenne_exp) > 20 else ''}")
        
        self.last_analysis = self.analyzer.analyze_mersenne_numbers()
        self.analyzer.print_summary(self.last_analysis)
        
        print(f"\nTop Conjecture: {self.last_analysis['conjectures'][0]['statement']}")
        print(f"Confidence: {self.last_analysis['conjectures'][0]['confidence']:.1f}%")
    
    def analyze_custom_set(self):
        """Analyze custom number set"""
        print("\nEnter numbers separated by commas (or type 'example' for a sample set):")
        user_input = input("> ").strip()
        
        if user_input.lower() == 'example':
            numbers = [1, 2, 3, 5, 8, 13, 21, 34, 55, 89]  # Fibonacci
            set_name = "Fibonacci Numbers"
        else:
            try:
                numbers = [int(x.strip()) for x in user_input.split(',')]
                set_name = "Custom Number Set"
            except ValueError:
                print("Invalid input. Please enter comma-separated integers.")
                return
        
        print(f"\nAnalyzing {len(numbers)} numbers...")
        self.last_analysis = self.analyzer.analyze_number_set(numbers, set_name)
        self.analyzer.print_summary(self.last_analysis)
    
    def view_last_report(self):
        """Display last analysis report"""
        if self.last_analysis is None:
            print("No analysis performed yet.")
        else:
            print(self.analyzer.generate_report(self.last_analysis))
    
    def generate_visualizations(self):
        """Generate charts and visualizations"""
        if self.last_analysis is None:
            print("No analysis to visualize. Please run an analysis first.")
            return
        
        print("\nGenerating visualizations...")
        
        try:
            self.visualizer.plot_number_growth(
                self.last_analysis['numbers'],
                self.last_analysis['set_name']
            )
            
            self.visualizer.plot_conjecture_quality_scores(self.last_analysis)
            
            self.visualizer.create_analysis_summary_dashboard(self.last_analysis)
            
            print("Visualizations saved to:", config.REPORTS_DIR)
        except Exception as e:
            print(f"Error generating visualizations: {e}")
    
    def view_database_stats(self):
        """Display database statistics"""
        print("\n" + "=" * 120)
        print("DATABASE STATISTICS")
        print("=" * 120)
        
        discoveries = self.analyzer.db.get_all_discoveries()
        conjectures = self.analyzer.db.get_all_conjectures()
        
        print(f"Total Discoveries: {len(discoveries)}")
        print(f"Total Conjectures: {len(conjectures)}")
        
        # Count by status
        open_conj = len([c for c in conjectures if c.get('status') == 'open'])
        verified = len([c for c in conjectures if c.get('status') == 'verified'])
        refuted = len([c for c in conjectures if c.get('status') == 'refuted'])
        
        print(f"\nConjecture Status:")
        print(f"  Open: {open_conj}")
        print(f"  Verified: {verified}")
        print(f"  Refuted: {refuted}")
        
        # Confidence statistics
        if conjectures:
            confidences = [c.get('confidence', 0) for c in conjectures]
            avg_conf = sum(confidences) / len(confidences)
            print(f"\nAverage Confidence: {avg_conf:.1f}%")

def main():
    """Main entry point"""
    try:
        app = MathDiscoveryAI()
        app.run_interactive()
    except KeyboardInterrupt:
        print("\n\nInterrupted by user.")
        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
