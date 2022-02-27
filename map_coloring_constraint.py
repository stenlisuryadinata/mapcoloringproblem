# -*- coding: utf-8 -*-
"""
Created on Mon Feb 28 01:06:37 2022

@author: DELL
"""

from csp1 import Constraint, CSP
from typing import Dict, List, Optional

# Sets the Coloring class which also determines if criteria is met.
class Coloring(Constraint[str,str]):
    def __init__(self, district1: str, district2: str) -> None:
        super().__init__([district1,district2])
        self.district1: str = district1
        self.district2: str = district2

    def satisfied(self, assignment: Dict[str,str]) -> bool:
        if self.district1 not in assignment or self.district2 not in assignment:
            return True
        return assignment[self.district1] != assignment[self.district2]

if __name__ == "__main__":
    # Set out variables
    input = []
    vertices = ""
    adjacent = {}
    vertex = ""
    variables = []
    # Read in text file
    with open('graph.txt') as f:
        input = f.read().splitlines()
    # Split up text file input into needed pieces
    if len(input) != 0:
        vertices=input[0]
        input.remove(vertices)
        if len(input) == int(vertices):
            for i in range(int(vertices)):
                v = input[i].split(' ')
                vertex = v[0]
                if len(v) != 1:
                    v.remove(vertex)
                    for vert in v:
                        adjacent[vertex] = v
                else:
                    # This is to handle the vertex at the end that has no adjacent vertex
                    adjacent[vertex] = 0
    for key in adjacent:
        variables.append(key)
        if(adjacent[key] == 0):
            variables.append("None")

    domains: Dict[str, List[str]] = {}
    colors = ["red", "green", "blue", "yellow", "violet", "pink","cyan" ]
    for variable in variables:
        domains[variable] = colors
    csp: CSP[str, str] = CSP(variables, domains)

    # Iterate through input and add constraint
    for key in adjacent:
        if (type(adjacent[key]) != int):
            for val in adjacent[key]:
                csp.add_constraint(Coloring(key, val))
        else:
            csp.add_constraint(Coloring(key, "None"))

    # Apply CSP and get result
    solution: Optional[Dict[str, str]] = csp.backtracking_search()
    if solution is None:
        if(len(colors) == 7):
            print("Not possible with 7 colors.")
        print("No solution found")
    else:
        # Removing any None refs
        solution.pop("None")
        for key in solution:
            print(f"{key} {solution[key]}")