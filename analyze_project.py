#!/usr/bin/env python3
"""
Project Analyzer - Scans Python files and classifies them
Run inside Cursor Terminal on the server:
    python analyze_project.py
"""

import os
import sys

# Colors for terminal output
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
BLUE = "\033[94m"
CYAN = "\033[96m"
RESET = "\033[0m"
BOLD = "\033[1m"

def analyze_project(root_dir="."):
    empty_files = []      # Completely empty
    stub_files = []       # Only pass/placeholder
    minimal_files = []    # Very small (< 20 lines)
    active_files = []     # Has real logic
    large_files = []      # > 100 lines
    
    total_files = 0
    
    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Skip hidden and cache directories
        dirnames[:] = [d for d in dirnames 
                       if not d.startswith('.') 
                       and d not in ('__pycache__', '.venv', '.git', 'node_modules')]
        
        for filename in filenames:
            if not filename.endswith('.py'):
                continue
            
            filepath = os.path.join(dirpath, filename)
            total_files += 1
            
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
            except Exception as e:
                continue
            
            lines = content.strip().split('\n')
            line_count = len([l for l in lines if l.strip()])
            stripped = content.strip()
            
            # Classification
            if line_count == 0:
                empty_files.append((filepath, line_count))
            elif line_count <= 3 and ('pass' in stripped or stripped == ''):
                stub_files.append((filepath, line_count))
            elif line_count < 20:
                minimal_files.append((filepath, line_count))
            elif line_count > 100:
                large_files.append((filepath, line_count))
            else:
                active_files.append((filepath, line_count))
    
    # Print Report
    print(f"\n{BOLD}{'='*80}{RESET}")
    print(f"{BOLD}{CYAN}  ODOO AI AUDIT PLATFORM - PROJECT ANALYSIS{RESET}")
    print(f"{BOLD}{'='*80}{RESET}\n")
    
    print(f"{BOLD}Total Python files scanned:{RESET} {total_files}\n")
    
    # Empty files
    print(f"{RED}{BOLD}❌ EMPTY FILES ({len(empty_files)}):{RESET}")
    print(f"   These files have zero content. Consider deleting.\n")
    for fp, lc in sorted(empty_files):
        print(f"   {RED}•{RESET} {fp}")
    
    # Stub files
    print(f"\n{YELLOW}{BOLD}⚠️  STUB FILES ({len(stub_files)}):{RESET}")
    print(f"   These files only contain 'pass' or imports. Need implementation.\n")
    for fp, lc in sorted(stub_files):
        print(f"   {YELLOW}•{RESET} {fp} ({lc} lines)")
    
    # Minimal files
    print(f"\n{YELLOW}{BOLD}⚡ MINIMAL FILES ({len(minimal_files)}):{RESET}")
    print(f"   These files have very little code. May need expansion.\n")
    for fp, lc in sorted(minimal_files):
        print(f"   {YELLOW}•{RESET} {fp} ({lc} lines)")
    
    # Active files
    print(f"\n{GREEN}{BOLD}✅ ACTIVE FILES ({len(active_files)}):{RESET}")
    print(f"   These files contain real logic.\n")
    for fp, lc in sorted(active_files):
        print(f"   {GREEN}•{RESET} {fp} ({lc} lines)")
    
    # Large files
    print(f"\n{BLUE}{BOLD}📦 LARGE FILES ({len(large_files)}):{RESET}")
    print(f"   These files are substantial (>100 lines).\n")
    for fp, lc in sorted(large_files):
        print(f"   {BLUE}•{RESET} {fp} ({lc} lines)")
    
    # Summary
    print(f"\n{BOLD}{'='*80}{RESET}")
    print(f"{BOLD}{CYAN}  SUMMARY{RESET}")
    print(f"{BOLD}{'='*80}{RESET}")
    print(f"   {RED}Empty:     {len(empty_files):>3}{RESET}")
    print(f"   {YELLOW}Stub:      {len(stub_files):>3}{RESET}")
    print(f"   {YELLOW}Minimal:   {len(minimal_files):>3}{RESET}")
    print(f"   {GREEN}Active:    {len(active_files):>3}{RESET}")
    print(f"   {BLUE}Large:     {len(large_files):>3}{RESET}")
    print(f"   {'─'*20}")
    print(f"   {BOLD}Total:     {total_files:>3}{RESET}")
    print(f"{BOLD}{'='*80}{RESET}\n")
    
    # Recommendations
    print(f"{BOLD}{CYAN}  RECOMMENDATIONS:{RESET}\n")
    if empty_files:
        print(f"   {RED}1. Delete empty files or fill them with logic.{RESET}")
    if stub_files:
        print(f"   {YELLOW}2. Implement stub files (currently just 'pass').{RESET}")
    if minimal_files:
        print(f"   {YELLOW}3. Review minimal files - may need expansion.{RESET}")
    print(f"   {GREEN}4. Active files are good - keep them.{RESET}")
    print(f"   {BLUE}5. Large files - review if they need splitting.{RESET}\n")

if __name__ == "__main__":
    root = sys.argv[1] if len(sys.argv) > 1 else "."
    analyze_project(root)
