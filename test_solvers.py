"""
Quick test script to verify all solvers work correctly
Tests 5 formulas with all 5 solvers
"""
import subprocess
import sys

def test_solver(solver_path, formula_path):
    try:
        result = subprocess.run(
            ['python', solver_path, formula_path],
            capture_output=True,
            text=True,
            timeout=5
        )
        return result.stdout.strip()
    except Exception as e:
        return f"ERROR: {e}"

# Test formulas
test_formulas = [1, 2, 10, 20, 50]
solvers = ['solvers/1.py', 'solvers/2.py', 'solvers/3.py', 'solvers/4.py', 'solvers/dpll-solver.py']
solver_names = ['1.py (Chrono+VSIDS)', '2.py (Chrono+BOHM)', '3.py (Restart+VSIDS)', '4.py (Restart+BOHM)', 'Baseline']

print("=" * 80)
print("QUICK SOLVER TEST - Testing 5 formulas with all solvers")
print("=" * 80)

all_passed = True

for formula_num in test_formulas:
    formula_path = f'benchmark/formula_{formula_num}.cnf'
    print(f"\nTesting formula_{formula_num}.cnf:")
    print("-" * 40)
    
    results = []
    for i, solver in enumerate(solvers):
        result = test_solver(solver, formula_path)
        results.append(result)
        print(f"  {solver_names[i]:25} -> {result}")
    
    # Check if first 4 solvers agree
    if len(set(results[:4])) > 1:
        print(f"  WARNING: Solvers disagree! {results[:4]}")
        all_passed = False

print("\n" + "=" * 80)
if all_passed:
    print("✓ ALL TESTS PASSED! All advanced solvers agree on results.")
else:
    print("✗ SOME TESTS FAILED! Solvers disagree on some formulas.")
print("=" * 80)
