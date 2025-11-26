#!/usr/bin/env python3
"""
CNF Benchmark Generator
Generates 100 CNF formulas with 50 variables and 3 literals per clause
Uses phase transition principles (ratio ≈ 4.26 clauses per variable)
"""

import random
import os


def generate_cnf_formula(num_vars: int, num_clauses: int, clause_size: int = 3) -> list:
    """
    Generate a random CNF formula
    
    Args:
        num_vars: Number of variables
        num_clauses: Number of clauses
        clause_size: Number of literals per clause (default 3 for 3-SAT)
    
    Returns:
        List of clauses, where each clause is a list of literals
    """
    clauses = []
    seen_clauses = set()  # To avoid duplicate clauses
    
    attempts = 0
    max_attempts = num_clauses * 10  # Prevent infinite loops
    
    while len(clauses) < num_clauses and attempts < max_attempts:
        attempts += 1
        
        # Select random variables for this clause
        variables = random.sample(range(1, num_vars + 1), clause_size)
        
        # Randomly assign polarities
        clause = []
        for var in variables:
            if random.random() < 0.5:
                clause.append(var)
            else:
                clause.append(-var)
        
        # Sort clause for canonicalization (to detect duplicates)
        clause_canonical = tuple(sorted(clause, key=lambda x: (abs(x), x > 0)))
        
        # Check for duplicate clause
        if clause_canonical not in seen_clauses:
            seen_clauses.add(clause_canonical)
            clauses.append(clause)
    
    return clauses


def write_dimacs_cnf(filename: str, num_vars: int, clauses: list):
    """
    Write CNF formula in DIMACS format
    
    Args:
        filename: Output filename
        num_vars: Number of variables
        clauses: List of clauses
    """
    with open(filename, 'w') as f:
        # Write header
        f.write(f"c CNF formula generated for SAT solver benchmarking\n")
        f.write(f"c Variables: {num_vars}, Clauses: {len(clauses)}\n")
        f.write(f"p cnf {num_vars} {len(clauses)}\n")
        
        # Write clauses
        for clause in clauses:
            clause_str = ' '.join(map(str, clause))
            f.write(f"{clause_str} 0\n")


def generate_benchmark_set(output_dir: str, num_formulas: int = 100, 
                          num_vars: int = 50, clause_size: int = 3):
    """
    Generate a set of benchmark CNF formulas using phase transition principles
    
    For 3-SAT, phase transition occurs around ratio = 4.26
    We'll generate formulas around this ratio to create interesting problems
    
    Args:
        output_dir: Directory to save CNF files
        num_formulas: Number of formulas to generate
        num_vars: Number of variables per formula
        clause_size: Literals per clause (3 for 3-SAT)
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Phase transition for 3-SAT is around 4.26 clauses per variable
    # We'll generate formulas in range [3.5, 5.0] to span the transition
    base_ratio = 4.26
    ratio_range = 0.8  # +/- range around base ratio
    
    print(f"Generating {num_formulas} CNF formulas...")
    print(f"Variables: {num_vars}, Clause size: {clause_size}")
    print(f"Clause/variable ratio range: {base_ratio - ratio_range} to {base_ratio + ratio_range}")
    
    for i in range(1, num_formulas + 1):
        # Vary the clause/variable ratio around phase transition
        # Most formulas near the critical ratio, some above and below
        ratio = random.gauss(base_ratio, ratio_range / 3)
        ratio = max(3.5, min(5.5, ratio))  # Clamp to reasonable range
        
        num_clauses = int(ratio * num_vars)
        
        # Generate formula
        clauses = generate_cnf_formula(num_vars, num_clauses, clause_size)
        
        # Write to file
        filename = os.path.join(output_dir, f"formula_{i}.cnf")
        write_dimacs_cnf(filename, num_vars, clauses)
        
        if i % 10 == 0:
            print(f"Generated {i}/{num_formulas} formulas...")
    
    print(f"Successfully generated {num_formulas} formulas in {output_dir}")


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Generate CNF benchmark formulas')
    parser.add_argument('--output', '-o', default='benchmark', 
                       help='Output directory (default: benchmark)')
    parser.add_argument('--count', '-n', type=int, default=100,
                       help='Number of formulas to generate (default: 100)')
    parser.add_argument('--vars', '-v', type=int, default=50,
                       help='Number of variables per formula (default: 50)')
    parser.add_argument('--clause-size', '-k', type=int, default=3,
                       help='Literals per clause (default: 3)')
    parser.add_argument('--seed', '-s', type=int, default=None,
                       help='Random seed for reproducibility')
    
    args = parser.parse_args()
    
    # Set random seed if provided
    if args.seed is not None:
        random.seed(args.seed)
        print(f"Using random seed: {args.seed}")
    
    # Generate benchmark set
    generate_benchmark_set(
        output_dir=args.output,
        num_formulas=args.count,
        num_vars=args.vars,
        clause_size=args.clause_size
    )


if __name__ == "__main__":
    main()
