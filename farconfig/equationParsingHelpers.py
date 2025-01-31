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
import re

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

def removeFunction(equation_str, function_str):
    return re.sub(r"^" + function_str + "\((.+?), \d+\)", r"(\1)", equation_str)

def extractValueOffsetAndDivisor(equation_str):
    pattern = r"\(value-(\d+\.?\d*)\)/(\d+\.?\d*)"
    match = re.match(pattern, equation_str)

    if match:
        value1 = float(match.group(1))  # Extract and convert the first number
        value2 = float(match.group(2))  # Extract and convert the second number
        return value1, value2
    else:
        raise ValueError("Equation format is invalid")

def extractValueOffsetAndMultiplier(equation_str):
    pattern = r"value-(\d+\.?\d*)\)\*\(?(\d+\.?\d*)"
    match = re.search(pattern, equation_str)

    if match:
        # Extract the numbers and convert them to float
        number1 = float(match.group(1))
        number2 = float(match.group(2))
        return number1, number2
    else:
        raise ValueError("Equation format is invalid")

def extractZeroCoefficientOffset(equation):
    """
    Parses an equation to extract zeroPosition, coefficient, and offset,
    ensuring correct differentiation between components and retaining their signs.

    Args:
        equation (str): The equation as a string.

    Returns:
        dict: A dictionary with keys 'zeroPosition', 'coefficient', and 'offset'.
              Missing zeroPosition and offset default to 0, coefficient defaults to 1.
    """
    # Initialize defaults
    result = {"zeroPosition": 0, "coefficient": 1, "offset": 0}

    # Remove all whitespaces from the equation for consistent matching
    equation = re.sub(r"\s+", "", equation)

    # Match the zeroPosition (value +/- number)
    zero_position_match = re.search(r"value([\+\-]\d+(\.\d*)?)", equation)
    if zero_position_match:
        result["zeroPosition"] = float(zero_position_match.group(1))

    # Match the coefficient (multiplication or division)
    coefficient_match = re.search(r"([*/])([\d.]+)", equation)
    if coefficient_match:
        operator = coefficient_match.group(1)
        value = float(coefficient_match.group(2))
        if operator == "*":
            result["coefficient"] = value
        elif operator == "/":
            result["coefficient"] = 1 / value

    # Match the offset (addition or subtraction at the end, with or without parentheses)
    offset_match = re.search(r"[+\-]\(?([\d.]+)\)?$", equation)
    if offset_match:
        offset_value = offset_match.group(1)  # Extract only the numeric part
        offset_sign = offset_match.group(0)[0]  # Extract the sign
        result["offset"] = float(offset_value) if offset_sign == "+" else -float(offset_value)

    return result


def stripBoolIBool(expression):
    """
    Extracts the numerical value from an expression like "bool(value-2000)" or "ibool(value-25000)".
    Strips everything except the numerical value inside the parentheses.

    Args:
        expression (str): The expression to extract the number from.

    Returns:
        float: The numerical value inside the parentheses.
    """
    # Remove whitespaces
    expression = re.sub(r"\s+", "", expression)

    # Match the pattern for 'value' followed by a number (either addition or subtraction)
    match = re.search(r"\((.*)\)", expression)
    if match:
        inside_parentheses = match.group(1)

        # Extract the number inside the parentheses (allowing for negative signs and decimals)
        number_match = re.search(r"[-+]?\d*\.?\d+", inside_parentheses)
        if number_match:
            return float(number_match.group(0))

    return None  # If no number is found, return None
