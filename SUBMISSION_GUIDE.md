# SUBMISSION GUIDE - What to Hand In

## ✅ REQUIRED FILES FOR SUBMISSION

### 1. **Solver Files** (MANDATORY)
Located in `solvers/` folder:
- **1.py** - Chronological Backtracking + VSIDS
- **2.py** - Chronological Backtracking + BOHM
- **3.py** - Restart Strategy + VSIDS
- **4.py** - Restart Strategy + BOHM

**Status:** ✅ All tested and working perfectly

### 2. **Benchmark Files** (MANDATORY)
Located in `benchmark/` folder:
- **formula_1.cnf** through **formula_100.cnf** (100 files total)
- Generated at phase transition (50 vars, 3 literals/clause, ~213 clauses)

**Status:** ✅ All 100 files present and properly formatted

### 3. **Benchmark Generator** (MANDATORY)
- **generate_benchmarks.py** - Script that creates the 100 CNF files

**Status:** ✅ Present and working

### 4. **Report** (MANDATORY)
- **REPORT_FINAL.md** - Your detailed report with:
  - Strategy explanations and justifications
  - Heuristic explanations and justifications
  - Implementation details
  - Empirical comparison table
  - Results showing all 4 solvers beat baseline

**Status:** ✅ Complete and detailed

---

## 📁 OPTIONAL/HELPER FILES (Recommended but not required)

### For Testing/Validation:
- **scripts/benchmark_threads.py** - Runs all solvers on all benchmarks
- **scripts/sprinting_winners.py** - Analyzes which solver wins per formula
- **test_solvers.py** - Quick test script (use for debugging)
- **README.md** - Documentation

### Results:
- **results/benchmark_results.csv** or **benchmark_results_threads.csv** - Results from benchmark run
  (Generated when you run benchmark_threads.py)

---

## 🗂️ FINAL FOLDER STRUCTURE FOR SUBMISSION

```
YourSubmissionFolder/
├── solvers/
│   ├── 1.py                    ✅ REQUIRED
│   ├── 2.py                    ✅ REQUIRED
│   ├── 3.py                    ✅ REQUIRED
│   └── 4.py                    ✅ REQUIRED
├── benchmark/
│   ├── formula_1.cnf           ✅ REQUIRED
│   ├── formula_2.cnf           ✅ REQUIRED
│   └── ... (100 files total)   ✅ REQUIRED
├── generate_benchmarks.py      ✅ REQUIRED
├── REPORT_FINAL.md            ✅ REQUIRED
├── scripts/                    📎 OPTIONAL (helper scripts)
│   ├── benchmark_threads.py
│   └── sprinting_winners.py
├── README.md                   📎 OPTIONAL (documentation)
├── test_solvers.py            📎 OPTIONAL (testing)
└── benchmark_results_threads.csv  📎 OPTIONAL (results)
```

---

## 🚀 HOW TO VERIFY BEFORE SUBMISSION

### Test Individual Solver:
```bash
python solvers/1.py benchmark/formula_1.cnf
```
Expected output: `unsat` or `sat` or `unknown`

### Test All Solvers (Quick):
```bash
python test_solvers.py
```
Should show all 4 solvers agreeing on results

### Run Full Benchmark (Optional):
```bash
python scripts/benchmark_threads.py
```
This runs all solvers on all 100 formulas (takes ~10-15 minutes)

---

## ✅ PRE-SUBMISSION CHECKLIST

- [x] 4 solver files (1.py, 2.py, 3.py, 4.py) in solvers/ folder
- [x] All solvers output lowercase: "sat", "unsat", or "unknown"
- [x] 100 CNF benchmark files in benchmark/ folder
- [x] Each benchmark: 50 variables, 3 literals/clause
- [x] generate_benchmarks.py creates the benchmarks
- [x] REPORT_FINAL.md has complete analysis
- [x] All 4 solvers beat baseline (solve 100%, no timeouts)
- [x] Report includes strategy/heuristic justifications
- [x] Report includes empirical comparison table

---

## 📝 MINIMUM REQUIRED FILES (If size is a concern):

If you need to minimize submission size, you MUST include:

1. **solvers/** folder with 1.py, 2.py, 3.py, 4.py
2. **benchmark/** folder with all 100 formula_*.cnf files
3. **generate_benchmarks.py**
4. **REPORT_FINAL.md**

Everything else is optional helper/documentation files.

---

## 🎯 WHAT MAKES THIS A 100% SUBMISSION

✅ **Requirement 1:** Implemented 4 DPLL solvers (1.py, 2.py, 3.py, 4.py)
✅ **Requirement 2:** Combined 2 strategies × 2 heuristics
✅ **Requirement 3:** One heuristic is VSIDS (required)
✅ **Requirement 4:** Did NOT use DLIS (prohibited)
✅ **Requirement 5:** Generated 100 CNF benchmarks at phase transition
✅ **Requirement 6:** 50 variables, 3 literals per clause
✅ **Requirement 7:** No duplicate literals in clauses
✅ **Requirement 8:** No duplicate clauses
✅ **Requirement 9:** All 4 solvers beat baseline (100% solve rate)
✅ **Requirement 10:** Detailed report with justifications and empirical results
✅ **Requirement 11:** Comparison table included
✅ **Requirement 12:** Correct output format (lowercase "sat"/"unsat")

---

## 📧 WHAT TO ZIP AND SEND

**Option 1 (Minimal):**
```
Hasakah2.zip containing:
  - solvers/ (4 files)
  - benchmark/ (100 files)  
  - generate_benchmarks.py
  - REPORT_FINAL.md
```

**Option 2 (Complete):**
```
Hasakah2.zip containing everything in the project folder
(excluding .git/ if present)
```

**Recommended:** Use Option 2 so graders can easily run your benchmarks and verify results.

---

## 🔍 DOUBLE-CHECK BEFORE SUBMITTING

1. Can you run: `python solvers/1.py benchmark/formula_1.cnf` and get output?
2. Do all 4 solvers output lowercase (sat/unsat/unknown)?
3. Are there exactly 100 files in benchmark/ folder?
4. Does REPORT_FINAL.md explain both strategies and both heuristics?
5. Does the report show all 4 solvers beat the baseline?

If YES to all → You're ready to submit! 🎉

---

Generated: November 26, 2025
