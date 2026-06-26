"""
Visualization Module - Creates charts and graphs
"""

import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, List, Any
from pathlib import Path
import config

class Visualizer:
    """Generate visualizations of mathematical discoveries"""
    
    def __init__(self):
        sns.set_theme(style="whitegrid")
        self.output_dir = config.REPORTS_DIR
    
    def plot_feature_distribution(self, analysis: Dict, feature_name: str, 
                                  save: bool = True) -> str:
        """Plot distribution of a feature across number set"""
        features = analysis['features']
        values = [features[num].get(feature_name, 0) for num in analysis['numbers']]
        
        fig, ax = plt.subplots(figsize=config.CHART_FIGSIZE, dpi=config.CHART_DPI)
        
        ax.plot(analysis['numbers'], values, marker='o', linewidth=2, markersize=8)
        ax.set_xlabel('Number')
        ax.set_ylabel(feature_name)
        ax.set_title(f"{feature_name} Distribution - {analysis['set_name']}")
        ax.grid(True, alpha=0.3)
        
        filename = f"{analysis['set_name']}_{feature_name.replace(' ', '_')}.png"
        filepath = self.output_dir / filename
        
        if save:
            plt.savefig(filepath, dpi=config.CHART_DPI, bbox_inches='tight')
            print(f"Saved chart: {filepath}")
        
        plt.close()
        return str(filepath)
    
    def plot_feature_correlation_heatmap(self, analysis: Dict, save: bool = True) -> str:
        """Create correlation heatmap of top features"""
        try:
            import numpy as np
            
            # Get top 10 features
            features_dict = analysis['feature_summary']
            top_features = sorted(features_dict.items(), 
                                key=lambda x: len(set(x[1])), reverse=True)[:10]
            
            feature_names = [name for name, _ in top_features]
            feature_values = [[v for v in values] for _, values in top_features]
            
            # Create correlation matrix
            correlations = np.corrcoef(feature_values)
            
            fig, ax = plt.subplots(figsize=(12, 10), dpi=config.CHART_DPI)
            sns.heatmap(correlations, annot=True, fmt='.2f', 
                       xticklabels=feature_names, yticklabels=feature_names,
                       ax=ax, cmap='coolwarm', center=0)
            
            ax.set_title(f"Feature Correlation Matrix - {analysis['set_name']}")
            
            filename = f"{analysis['set_name']}_correlation_heatmap.png"
            filepath = self.output_dir / filename
            
            if save:
                plt.savefig(filepath, dpi=config.CHART_DPI, bbox_inches='tight')
                print(f"Saved chart: {filepath}")
            
            plt.close()
            return str(filepath)
        except:
            print("Warning: Could not create correlation heatmap")
            return None
    
    def plot_conjecture_quality_scores(self, analysis: Dict, save: bool = True) -> str:
        """Plot quality scores of conjectures"""
        conjectures = analysis['conjectures'][:15]
        
        ids = [c['id'] for c in conjectures]
        scores = [c['quality_score'] for c in conjectures]
        
        fig, ax = plt.subplots(figsize=config.CHART_FIGSIZE, dpi=config.CHART_DPI)
        
        bars = ax.barh(ids, scores, color='steelblue')
        ax.set_xlabel('Quality Score')
        ax.set_ylabel('Conjecture ID')
        ax.set_title(f"Top Conjecture Quality Scores - {analysis['set_name']}")
        
        # Add value labels
        for bar in bars:
            width = bar.get_width()
            ax.text(width, bar.get_y() + bar.get_height()/2, 
                   f'{width:.1f}', ha='left', va='center')
        
        filename = f"{analysis['set_name']}_conjecture_scores.png"
        filepath = self.output_dir / filename
        
        if save:
            plt.savefig(filepath, dpi=config.CHART_DPI, bbox_inches='tight')
            print(f"Saved chart: {filepath}")
        
        plt.close()
        return str(filepath)
    
    def plot_number_growth(self, numbers: List[int], set_name: str, save: bool = True) -> str:
        """Plot growth of number set"""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5), dpi=config.CHART_DPI)
        
        # Linear scale
        ax1.plot(range(len(numbers)), numbers, marker='o', linewidth=2, markersize=8)
        ax1.set_xlabel('Index')
        ax1.set_ylabel('Number Value')
        ax1.set_title(f"Growth Pattern (Linear) - {set_name}")
        ax1.grid(True, alpha=0.3)
        
        # Log scale
        ax2.semilogy(range(len(numbers)), numbers, marker='o', linewidth=2, markersize=8)
        ax2.set_xlabel('Index')
        ax2.set_ylabel('Number Value (log scale)')
        ax2.set_title(f"Growth Pattern (Log Scale) - {set_name}")
        ax2.grid(True, alpha=0.3)
        
        filename = f"{set_name}_growth_pattern.png"
        filepath = self.output_dir / filename
        
        if save:
            plt.savefig(filepath, dpi=config.CHART_DPI, bbox_inches='tight')
            print(f"Saved chart: {filepath}")
        
        plt.close()
        return str(filepath)
    
    def create_analysis_summary_dashboard(self, analysis: Dict, save: bool = True) -> str:
        """Create a multi-panel summary dashboard"""
        fig = plt.figure(figsize=(16, 12), dpi=config.CHART_DPI)
        
        # Title
        fig.suptitle(f"Mathematical Discovery Dashboard - {analysis['set_name']}", 
                    fontsize=16, fontweight='bold')
        
        # Create subplots
        gs = fig.add_gridspec(3, 2, hspace=0.3, wspace=0.3)
        
        # Top conjectures
        ax1 = fig.add_subplot(gs[0, :])
        conj_ids = [str(c['id']) for c in analysis['conjectures'][:10]]
        conj_scores = [c['quality_score'] for c in analysis['conjectures'][:10]]
        ax1.bar(conj_ids, conj_scores, color='steelblue', alpha=0.7)
        ax1.set_title('Top 10 Conjectures by Quality Score')
        ax1.set_ylabel('Quality Score')
        
        # Number set summary
        ax2 = fig.add_subplot(gs[1, 0])
        ax2.text(0.1, 0.9, f"Analysis Summary", fontsize=12, fontweight='bold', 
                transform=ax2.transAxes)
        ax2.text(0.1, 0.7, f"Numbers Analyzed: {analysis['number_count']}", 
                transform=ax2.transAxes)
        ax2.text(0.1, 0.5, f"Features Extracted: {analysis['total_features_extracted']}", 
                transform=ax2.transAxes)
        ax2.text(0.1, 0.3, f"Conjectures Generated: {len(analysis['conjectures'])}", 
                transform=ax2.transAxes)
        ax2.axis('off')
        
        # Pattern summary
        ax3 = fig.add_subplot(gs[1, 1])
        all_patterns = []
        for pattern_list in analysis['patterns'].values():
            all_patterns.extend(pattern_list)
        
        pattern_types = {}
        for p in all_patterns:
            ptype = p.get('type', 'unknown')
            pattern_types[ptype] = pattern_types.get(ptype, 0) + 1
        
        if pattern_types:
            ax3.pie(pattern_types.values(), labels=pattern_types.keys(), autopct='%1.0f%%')
            ax3.set_title('Pattern Type Distribution')
        else:
            ax3.text(0.5, 0.5, 'No patterns found', ha='center', va='center')
            ax3.set_title('Pattern Type Distribution')
        
        # Growth visualization
        if len(analysis['numbers']) > 1:
            ax4 = fig.add_subplot(gs[2, :])
            ax4.semilogy(range(len(analysis['numbers'])), analysis['numbers'], 
                        marker='o', linewidth=2, markersize=8, color='green')
            ax4.set_xlabel('Index')
            ax4.set_ylabel('Number Value (log scale)')
            ax4.set_title('Number Set Growth Pattern')
            ax4.grid(True, alpha=0.3)
        
        filename = f"{analysis['set_name'].replace(' ', '_')}_dashboard.png"
        filepath = self.output_dir / filename
        
        if save:
            plt.savefig(filepath, dpi=config.CHART_DPI, bbox_inches='tight')
            print(f"Saved dashboard: {filepath}")
        
        plt.close()
        return str(filepath)
