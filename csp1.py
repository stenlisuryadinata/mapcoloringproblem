# -*- coding: utf-8 -*-
"""
Created on Sat Feb 26 22:30:06 2022

@author: DELL
"""

from typing import Generic, TypeVar, Dict, List, Optional
from abc import ABC, abstractmethod
V = TypeVar('V')
D = TypeVar('D')

# This setups the constraint class.
class Constraint(Generic[V, D], ABC):

    def __init__(self, variables: List[V]) -> None:
        self.variables = variables

    # To be adapted in coloring class
    @abstractmethod
    def satisfied(self, assignment: Dict[V,D]) -> bool:
        pass

# This runs the CSP algorithm with Generic inputs
class CSP(Generic[V,D]):
    def __init__(self, variables: List[V], domains: Dict[V, List[D]]) -> None:
        self.variables: List[V] = variables
        self.domains: Dict[V, List[D]] = domains
        self.constraints: Dict[V, List[Constraint[V,D]]] = {}
        for variable in self.variables:
            self.constraints[variable] = []
            if variable not in self.domains:
                raise LookupError("Variable needs a domain.")

    # Set the constraint
    def add_constraint(self, constraint: Constraint[V, D]) -> None:
        for variable in constraint.variables:
            if variable not in self.variables:
                raise LookupError("Variable is in constraint but not in CSP")
            else:
                self.constraints[variable].append(constraint)

    # Determine if the rule is satisfied
    def consistent(self,variable: V, assignment: Dict[V,D]) -> bool:
        for constraint in self.constraints[variable]:
            if not constraint.satisfied(assignment):
                return False
        return True

    # Performs recursive search to make sure we can assign to every variable
    def backtracking_search(self, assignment: Dict[V,D] = {}) -> Optional[Dict[V, D]]:
        if len(assignment) == len(self.variables):
            return assignment

        unassigned: List[V] = [v for v in self.variables if v not in assignment]

        first: V = unassigned[0]
        # Trying to assign a domain value to variable
        for value in self.domains[first]:
            local_assignment = assignment.copy()
            local_assignment[first] = value

            # Check it works with given constraint.
            if self.consistent(first, local_assignment):
                result: Optional[Dict[V,D]] = self.backtracking_search(local_assignment)
                if result is not None:
                    return result
        return None