#
#  This file is part of The Ekdahl FAR firmware.
#
#  The Ekdahl FAR firmware is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  The Ekdahl FAR firmware is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with The Ekdahl FAR firmware. If not, see <https://www.gnu.org/licenses/>.
#
# Copyright (C) 2024 Karl Ekdahl
#

import sympy as sp

def getVariable(equation_str, variable_str):
    try:
        # Parse the equation string into a symbolic expression
        equation = sp.sympify(equation_str)

        # Define the variable symbolically
        variable = sp.Symbol(variable_str)

        # Expand the equation to separate terms
        expanded_equation = equation.expand()

        # Get the terms of the equation
        terms = sp.Add.make_args(expanded_equation)

        # Initialize offset and multiplier
        offset = 0
        multiplier = 0

        for term in terms:
            # Check if the term contains the variable
            if term.has(variable):
                # Extract the local coefficient of the variable
                coefficient = term.as_coefficients_dict()[variable]
                if coefficient is None:
                    coefficient = 1
                multiplier += coefficient
            else:
                # If the term does not contain the variable, it contributes to the offset
                offset += term

        return float(offset), float(multiplier)
    except Exception as e:
        return 0, 0

def isVariableInEquation(equation_str, variable_str):
    try:
        # Parse the equation string into a symbolic expression
        equation = sp.sympify(equation_str)

        # Define the variable symbolically
        variable = sp.Symbol(variable_str)

        # Check if the variable is in the equation
        return equation.has(variable)
    except Exception as e:
        return False