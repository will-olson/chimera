#!/usr/bin/env python3
"""
Automated Puzzle.md Analysis Script
Following SYSTEMATIC_PUZZLE_ANALYSIS_STRATEGY.md methodology
"""

import re
from pathlib import Path
import json
from typing import Dict, List, Tuple

class PuzzleAnalyzer:
    def __init__(self, puzzle_file: str = "../puzzle.md"):
        self.puzzle_file = puzzle_file
        self.content = ""
        self.results = {}
        
    def load_content(self):
        """Load the puzzle.md content"""
        try:
            with open(self.puzzle_file, 'r', encoding='utf-8') as f:
                self.content = f.read()
            print(f"✅ Loaded {len(self.content)} characters from {self.puzzle_file}")
            return True
        except FileNotFoundError:
            print(f"❌ File not found: {self.puzzle_file}")
            return False
        except Exception as e:
            print(f"❌ Error loading file: {e}")
            return False
    
    def extract_patterns(self) -> Dict[str, List[Tuple[int, int, str]]]:
        """Extract all patterns following the strategy document"""
        print("🔍 Extracting patterns systematically...")
        
        patterns = {
            'functions': r'function\s+\w+\s*\([^)]*\)\s*\{',
            'math_functions': r'Math\.\w+\s*\(',
            'event_handlers': r'addEventListener\s*\(',
            'mouse_events': r'mousedown|mouseup|mousemove|touchstart|touchend',
            'drag_events': r'drag|drop|move|slide',
            'success_conditions': r'done|success|complete|finished',
            'coordinate_calc': r'position|coordinate|offset|distance',
            'validation_logic': r'validate|check|verify',
            'timing_functions': r'setTimeout|setInterval|delay|wait',
            'detection_logic': r'detect|detection|bot|automation',
            'state_management': r'state|status|condition',
            'cleanup_logic': r'cleanup|reset|clear|destroy'
        }
        
        results = {}
        
        for pattern_name, pattern in patterns.items():
            print(f"  🔍 Searching for: {pattern_name}")
            matches = re.finditer(pattern, self.content, re.MULTILINE | re.IGNORECASE)
            pattern_results = []
            
            for match in matches:
                line_number = self.content[:match.start()].count('\n') + 1
                context = self.extract_context(match.start(), 3)
                pattern_results.append({
                    'line': line_number,
                    'start_pos': match.start(),
                    'end_pos': match.end(),
                    'match': match.group(),
                    'context': context
                })
            
            results[pattern_name] = pattern_results
            print(f"    ✅ Found {len(pattern_results)} matches")
        
        self.results = results
        return results
    
    def extract_context(self, position: int, lines: int = 3) -> str:
        """Extract context around a position"""
        start = max(0, position - 200)
        end = min(len(self.content), position + 200)
        
        context = self.content[start:end]
        # Find line boundaries
        lines_before = context[:200].count('\n')
        lines_after = context[200:].count('\n')
        
        return f"Lines {lines_before} before to {lines_after} after position {position}"
    
    def analyze_math_functions(self) -> Dict:
        """Analyze mathematical functions specifically"""
        print("🧮 Analyzing mathematical functions...")
        
        math_analysis = {
            'coordinate_calculations': [],
            'position_validation': [],
            'movement_calculations': [],
            'success_thresholds': []
        }
        
        # Look for specific mathematical patterns
        math_patterns = {
            'coordinate_calculations': r'Math\.(sin|cos|tan|atan2|sqrt|pow)\s*\(',
            'position_validation': r'(position|coordinate|offset|distance)\s*[<>=!]',
            'movement_calculations': r'(move|slide|drag)\s*[+\-*/]',
            'success_thresholds': r'(threshold|tolerance|precision|accuracy)'
        }
        
        for category, pattern in math_patterns.items():
            matches = re.finditer(pattern, self.content, re.MULTILINE | re.IGNORECASE)
            for match in matches:
                line_number = self.content[:match.start()].count('\n') + 1
                math_analysis[category].append({
                    'line': line_number,
                    'match': match.group(),
                    'context': self.extract_context(match.start(), 2)
                })
        
        return math_analysis
    
    def generate_analysis_report(self) -> str:
        """Generate a comprehensive analysis report"""
        report = []
        report.append("# 🧩 AUTOMATED PUZZLE.MD ANALYSIS REPORT")
        report.append(f"Generated from: {self.puzzle_file}")
        report.append(f"Total content length: {len(self.content)} characters")
        report.append(f"Total lines: {self.content.count(chr(10)) + 1}")
        report.append("")
        
        # Summary statistics
        report.append("## 📊 PATTERN SUMMARY")
        for pattern_name, matches in self.results.items():
            report.append(f"- **{pattern_name}**: {len(matches)} matches")
        report.append("")
        
        # High-priority findings
        report.append("## 🎯 HIGH-PRIORITY FINDINGS")
        
        # Mathematical functions
        if self.results.get('math_functions'):
            report.append("### 🧮 Mathematical Functions")
            for match in self.results['math_functions'][:5]:  # Top 5
                report.append(f"- Line {match['line']}: {match['match']}")
            report.append("")
        
        # Event handlers
        if self.results.get('event_handlers'):
            report.append("### 🖱️ Event Handlers")
            for match in self.results['event_handlers'][:5]:  # Top 5
                report.append(f"- Line {match['line']}: {match['match']}")
            report.append("")
        
        # Success conditions
        if self.results.get('success_conditions'):
            report.append("### ✅ Success Conditions")
            for match in self.results['success_conditions'][:5]:  # Top 5
                report.append(f"- Line {match['line']}: {match['match']}")
            report.append("")
        
        # Coordinate calculations
        if self.results.get('coordinate_calc'):
            report.append("### 📍 Coordinate Calculations")
            for match in self.results['coordinate_calc'][:5]:  # Top 5
                report.append(f"- Line {match['line']}: {match['match']}")
            report.append("")
        
        return "\n".join(report)
    
    def save_results(self, output_file: str = "puzzle_analysis_results.json"):
        """Save results to JSON file"""
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(self.results, f, indent=2, ensure_ascii=False)
            print(f"✅ Results saved to {output_file}")
        except Exception as e:
            print(f"❌ Error saving results: {e}")
    
    def run_complete_analysis(self):
        """Run the complete analysis following the strategy"""
        print("🚀 Starting systematic puzzle analysis...")
        print("=" * 60)
        
        # Phase 1: Load content
        if not self.load_content():
            return False
        
        # Phase 2: Extract patterns
        self.extract_patterns()
        
        # Phase 3: Analyze mathematical functions
        math_analysis = self.analyze_math_functions()
        self.results['math_analysis'] = math_analysis
        
        # Phase 4: Generate report
        report = self.generate_analysis_report()
        
        # Phase 5: Save results
        self.save_results()
        
        # Phase 6: Display report
        print("\n" + "=" * 60)
        print("📋 ANALYSIS REPORT")
        print("=" * 60)
        print(report)
        
        return True

def main():
    """Main execution function"""
    analyzer = PuzzleAnalyzer()
    
    if analyzer.run_complete_analysis():
        print("\n✅ Analysis completed successfully!")
        print("📁 Check puzzle_analysis_results.json for detailed results")
    else:
        print("\n❌ Analysis failed!")

if __name__ == "__main__":
    main()
