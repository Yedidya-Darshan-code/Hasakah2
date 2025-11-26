#!/usr/bin/env python3
"""
Solver 4: Restart Strategy + BOHM
Combines periodic restart strategy with BOHM variable selection heuristic
"""

import sys
import copy
from typing import List, Set, Dict, Tuple, Optional
from collections import defaultdict


# ============================================================================
# CNF Formula Class
# ============================================================================

class CNFFormula:
    """Represents a CNF formula"""
    
    def __init__(self, num_vars: int, clauses: List[List[int]]):
        self.num_vars = num_vars
        self.clauses = clauses
        self.assignment = {}  # Variable -> True/False
        
    def copy(self):
        """Deep copy of the formula"""
        new_formula = CNFFormula(self.num_vars, copy.deepcopy(self.clauses))
        new_formula.assignment = self.assignment.copy()
        return new_formula


# ============================================================================
# Restart Strategy
# ============================================================================

class RestartStrategy:
    """Periodic restart strategy using Luby sequence"""
    
    def __init__(self, base_interval: int = 100):
        self.name = "Restart"
        self.base_interval = base_interval
        self.conflicts_since_restart = 0
        self.restart_count = 0
        self.luby_index = 0
    
    def should_restart(self, conflicts: int, decisions: int) -> bool:
        self.conflicts_since_restart = conflicts - (self.restart_count * self.base_interval)
        
        if self.conflicts_since_restart >= self._luby(self.luby_index) * self.base_interval:
            self.restart_count += 1
            self.luby_index += 1
            return True
        return False
    
    def on_conflict(self, level: int) -> int:
        return 0
    
    def _luby(self, i: int) -> int:
        k = 1
        while (1 << k) - 1 <= i:
            k += 1
        k -= 1
        
        if i == (1 << k) - 1:
            return 1 << k
        else:
            return self._luby(i - (1 << k) + 1)


# ============================================================================
# BOHM Heuristic
# ============================================================================

class BOHMHeuristic:
    """BOHM - prioritizes variables in smallest clauses with weighted scoring"""
    
    def __init__(self, alpha: int = 1, beta: int = 2):
        self.name = "BOHM"
        self.alpha = alpha
        self.beta = beta
        self.scores = {}
    
    def select_variable(self, formula: CNFFormula, unassigned: Set[int]) -> Optional[int]:
        if not unassigned:
            return None
        
        self._compute_scores(formula, unassigned)
        
        if not self.scores:
            return next(iter(unassigned))
        
        best_var = None
        best_score = -1
        
        for var in unassigned:
            if var in self.scores and self.scores[var] > best_score:
                best_score = self.scores[var]
                best_var = var
        
        return best_var if best_var else next(iter(unassigned))
    
    def on_conflict(self, clause: List[int]):
        pass
    
    def _compute_scores(self, formula: CNFFormula, unassigned: Set[int]):
        self.scores = defaultdict(float)
        
        for clause in formula.clauses:
            if self._is_clause_satisfied(formula, clause):
                continue
            
            unassigned_lits = [lit for lit in clause if abs(lit) in unassigned]
            
            if not unassigned_lits:
                continue
            
            clause_size = len(unassigned_lits)
            weight = 2 ** (5 - clause_size) if clause_size <= 5 else 1
            
            pos_count = defaultdict(int)
            neg_count = defaultdict(int)
            
            for lit in unassigned_lits:
                var = abs(lit)
                if lit > 0:
                    pos_count[var] += 1
                else:
                    neg_count[var] += 1
            
            for var in unassigned:
                if var in pos_count or var in neg_count:
                    score = self.alpha * pos_count.get(var, 0) + self.beta * neg_count.get(var, 0)
                    self.scores[var] += weight * score
    
    def _is_clause_satisfied(self, formula: CNFFormula, clause: List[int]) -> bool:
        for lit in clause:
            var = abs(lit)
            if var in formula.assignment:
                if (lit > 0 and formula.assignment[var]) or \
                   (lit < 0 and not formula.assignment[var]):
                    return True
        return False


# ============================================================================
# DPLL Solver
# ============================================================================

class DPLLSolver:
    """Base DPLL SAT Solver"""
    
    def __init__(self, strategy, heuristic):
        self.strategy = strategy
        self.heuristic = heuristic
        self.decisions = 0
        self.conflicts = 0
        self.propagations = 0
        
    def solve(self, formula: CNFFormula) -> Tuple[bool, Dict[int, bool]]:
        self.decisions = 0
        self.conflicts = 0
        self.propagations = 0
        result = self._dpll(formula)
        return result, formula.assignment if result else {}
    
    def _dpll(self, formula: CNFFormula) -> bool:
        if not self._unit_propagate(formula):
            return False
        
        self._pure_literal_eliminate(formula)
        
        if all(len(clause) == 0 or self._is_clause_satisfied(formula, clause) 
               for clause in formula.clauses):
            return True
        
        if self._has_empty_clause(formula):
            return False
        
        unassigned = self._get_unassigned_vars(formula)
        if not unassigned:
            return self._is_satisfied(formula)
        
        if self.strategy.should_restart(self.conflicts, self.decisions):
            return False
        
        var = self.heuristic.select_variable(formula, unassigned)
        if var is None:
            var = next(iter(unassigned))
        
        self.decisions += 1
        
        for value in [True, False]:
            new_formula = formula.copy()
            new_formula.assignment[var] = value
            simplified = self._simplify(new_formula, var, value)
            
            if self._dpll(simplified):
                formula.assignment.update(simplified.assignment)
                return True
            
            self.conflicts += 1
            self.heuristic.on_conflict(self._get_conflict_clause(simplified))
        
        return False
    
    def _unit_propagate(self, formula: CNFFormula) -> bool:
        changed = True
        while changed:
            changed = False
            for clause in formula.clauses:
                unassigned_lits = []
                satisfied = False
                
                for lit in clause:
                    var = abs(lit)
                    if var in formula.assignment:
                        if (lit > 0 and formula.assignment[var]) or \
                           (lit < 0 and not formula.assignment[var]):
                            satisfied = True
                            break
                    else:
                        unassigned_lits.append(lit)
                
                if satisfied:
                    continue
                
                if len(unassigned_lits) == 0:
                    return False
                
                if len(unassigned_lits) == 1:
                    lit = unassigned_lits[0]
                    var = abs(lit)
                    formula.assignment[var] = (lit > 0)
                    changed = True
                    self.propagations += 1
        
        return True
    
    def _pure_literal_eliminate(self, formula: CNFFormula):
        literal_polarity = {}
        
        for clause in formula.clauses:
            if self._is_clause_satisfied(formula, clause):
                continue
            
            for lit in clause:
                var = abs(lit)
                if var in formula.assignment:
                    continue
                
                if var not in literal_polarity:
                    literal_polarity[var] = set()
                literal_polarity[var].add(lit > 0)
        
        for var, polarities in literal_polarity.items():
            if len(polarities) == 1:
                formula.assignment[var] = next(iter(polarities))
    
    def _simplify(self, formula: CNFFormula, var: int, value: bool) -> CNFFormula:
        new_clauses = []
        
        for clause in formula.clauses:
            satisfied = False
            new_clause = []
            
            for lit in clause:
                if abs(lit) == var:
                    if (lit > 0 and value) or (lit < 0 and not value):
                        satisfied = True
                        break
                else:
                    new_clause.append(lit)
            
            if not satisfied:
                new_clauses.append(new_clause)
        
        result = CNFFormula(formula.num_vars, new_clauses)
        result.assignment = formula.assignment.copy()
        return result
    
    def _is_clause_satisfied(self, formula: CNFFormula, clause: List[int]) -> bool:
        for lit in clause:
            var = abs(lit)
            if var in formula.assignment:
                if (lit > 0 and formula.assignment[var]) or \
                   (lit < 0 and not formula.assignment[var]):
                    return True
        return False
    
    def _is_satisfied(self, formula: CNFFormula) -> bool:
        for clause in formula.clauses:
            if not self._is_clause_satisfied(formula, clause):
                return False
        return True
    
    def _has_empty_clause(self, formula: CNFFormula) -> bool:
        for clause in formula.clauses:
            if len(clause) == 0:
                return True
        return False
    
    def _get_unassigned_vars(self, formula: CNFFormula) -> Set[int]:
        all_vars = set(range(1, formula.num_vars + 1))
        assigned_vars = set(formula.assignment.keys())
        return all_vars - assigned_vars
    
    def _get_conflict_clause(self, formula: CNFFormula) -> List[int]:
        for clause in formula.clauses:
            if len(clause) == 0:
                return clause
            if not self._is_clause_satisfied(formula, clause):
                all_assigned = all(abs(lit) in formula.assignment for lit in clause)
                if all_assigned:
                    all_false = all(
                        (lit > 0 and not formula.assignment[abs(lit)]) or
                        (lit < 0 and formula.assignment[abs(lit)])
                        for lit in clause
                    )
                    if all_false:
                        return clause
        return []


# ============================================================================
# CNF Parser
# ============================================================================

def parse_cnf(filename: str) -> CNFFormula:
    """Parse DIMACS CNF file"""
    num_vars = 0
    num_clauses = 0
    clauses = []
    
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('c'):
                continue
            
            if line.startswith('p'):
                parts = line.split()
                num_vars = int(parts[2])
                num_clauses = int(parts[3])
                continue
            
            clause = [int(x) for x in line.split() if x != '0']
            if clause:
                clauses.append(clause)
    
    return CNFFormula(num_vars, clauses)


# ============================================================================
# Main Entry Point
# ============================================================================

def main():
    if len(sys.argv) < 2:
        print("Usage: python 4.py <cnf_file>")
        sys.exit(1)
    
    cnf_file = sys.argv[1]
    
    try:
        formula = parse_cnf(cnf_file)
        strategy = RestartStrategy()
        heuristic = BOHMHeuristic()
        solver = DPLLSolver(strategy, heuristic)
        
        result, assignment = solver.solve(formula)
        
        if result:
            print("sat")
        else:
            print("unsat")
    
    except Exception as e:
        print("unknown")
        sys.exit(1)


if __name__ == "__main__":
    main()
