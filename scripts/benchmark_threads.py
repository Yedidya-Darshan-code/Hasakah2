import subprocess
import time
import os
import math
import csv
from concurrent.futures import ThreadPoolExecutor

# Configuration
SOLVER_FILES = ["1.py", "2.py", "3.py", "4.py", "dpll-solver.py"]
SOLVERS_DIR = "solvers"
BENCHMARK_DIR = "benchmark"
PYTHON_COMMAND = "python"  # Changed from python3 to python for Windows
NUM_FORMULAS = 100  # From 1 to 100
TIMEOUT = 5  # timeout in seconds per run, or None if no timeout
CSV_FILENAME = "benchmark_results_threads.csv"

# Data structure to hold results
# results[solver][formula_number] = {"time": runtime_in_seconds, "result": "SAT"/"UNSAT"/"UNKNOWN"}
results = {solver: {} for solver in SOLVER_FILES}


def parse_result(output):
    """
    Parse the solver's output to determine the result.
    Minisat prints 'SAT' or 'UNSAT' in uppercase.
    Python solvers might print in lowercase, so convert to lowercase before checking.
    """
    output_lower = output.lower()
    if "sat" in output_lower and "unsat" not in output_lower:
        return "sat"
    elif "unsat" in output_lower:
        return "unsat"
    else:
        return "unknown"


def run_solver(solver):
    """Run a single solver on all formulas and store results in the global results dict."""
    print(f"Starting solver: {solver}")
    for i in range(1, NUM_FORMULAS + 1):
        print(f"{solver}: running formula_{i}.cnf")
        cnf_path = os.path.join(BENCHMARK_DIR, f"formula_{i}.cnf")
        if not os.path.isfile(cnf_path):
            print(f"Warning: {cnf_path} not found, skipping.")
            continue

        start = time.perf_counter()
        try:
            # Determine the command to run depending on the solver type
            if solver.endswith(".py"):
                cmd = [PYTHON_COMMAND, os.path.join(SOLVERS_DIR, solver), cnf_path]
            else:
                # For Minisat or other non-python solvers
                cmd = [solver, cnf_path]

            completed_process = subprocess.run(
                cmd,
                timeout=TIMEOUT,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True  # Decode output as string
            )
            end = time.perf_counter()
            elapsed = end - start
            # Parse the result from solver's stdout
            result = parse_result(completed_process.stdout)
            results[solver][i] = {"time": elapsed, "result": result}
        except subprocess.TimeoutExpired:
            print(f"{solver} timed out on formula {i}.")
            results[solver][i] = {"time": float('inf'), "result": "unknown"}
        except Exception as e:
            print(f"Error running {solver} on formula {i}: {e}")
            results[solver][i] = {"time": float('inf'), "result": "ERROR"}
    print(f"Finished solver: {solver}")


# Run all solvers concurrently using 5 threads (or more if you like)
with ThreadPoolExecutor(max_workers=6) as executor:
    futures = [executor.submit(run_solver, solver) for solver in SOLVER_FILES]
    for future in futures:
        future.result()  # wait for all to complete

# Print summary
print("Benchmark Results:")
print("=================")
for solver in SOLVER_FILES:
    solver_results = results[solver].values()
    solved_times = [r["time"] for r in solver_results if r["time"] != float('inf')]
    timeouts = sum(1 for r in solver_results if r["time"] == float('inf') and r["result"] == "unknown")
    errors = sum(1 for r in solver_results if r.get("result") == "ERROR")
    if solved_times:
        avg_time = sum(solved_times) / len(solved_times)
    else:
        avg_time = float('inf')
    print(f"Solver: {solver}")
    print(f"  Solved: {len(solved_times)} / {len(results[solver])}")
    print(f"  Timeouts: {timeouts}")
    print(f"  Errors: {errors}")
    if solved_times:
        print(f"  Average Time (for solved instances): {avg_time:.4f} seconds")
    print()

# Determine the winner per formula and write to CSV
formulas = sorted(set(i for solver in SOLVER_FILES for i in results[solver].keys()))
# CSV columns: formula, solver1_time, solver1_result, solver2_time, solver2_result, ..., winner, winner_time
header = ["formula"]
for solver in SOLVER_FILES:
    header.extend([f"{solver}_time", f"{solver}_result"])
header += ["winner", "winner_time"]

with open(CSV_FILENAME, "w", newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(header)

    for i in formulas:
        row = [f"formula_{i}"]
        solver_times_results = []
        for solver in SOLVER_FILES:
            solver_data = results[solver].get(i, {"time": float('inf'), "result": "unknown"})
            time_str = "inf" if math.isinf(solver_data["time"]) else f"{solver_data['time']:.4f}"
            result_str = solver_data["result"]
            row.extend([time_str, result_str])
            solver_times_results.append((solver, solver_data["time"]))

        # Find the solver with the minimum time that didn't timeout or error
        valid_solvers = [(s, t) for s, t in solver_times_results if not math.isinf(t)]
        if valid_solvers:
            winner_solver, winner_time = min(valid_solvers, key=lambda x: x[1])
            winner_time_str = f"{winner_time:.4f}"
        else:
            winner_solver = "None"
            winner_time_str = "inf"

        row.extend([winner_solver, winner_time_str])

        writer.writerow(row)

print(f"CSV results saved to {CSV_FILENAME}.")
