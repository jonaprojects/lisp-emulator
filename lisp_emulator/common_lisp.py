# Imports
import string
from pyfiglet import Figlet
import os
from math import pi, sin, asin, cos, acos, tan, atan, sinh, cosh, tanh, asinh, acosh, atanh, sqrt, e
# Constants
signs = [' ', '"', "'"]
type_signs = ['"', "'"]
agreement = ['YES', 'YE', 'OF COURSE', 'INDEED', 'YEP', 'POSITIVE', 'ABSOLUTELY', 'DEFINITELY'
                                                                                  'OK', 'FINE']
not_sure = ['MAYBE', 'MAY BE', 'PERHAPS',
            "I DON'T KNOW", "I DONT KNOW", 'IDK', 'PROBABLY']
# Functions
built_in_functions = ['+', '-', '*', '/', '=', 'WRITE', 'PRINT', 'EQ', 'CONCATENATE', 'MAX', 'MIN', 'IF', 'DEFUN',
                      'DEFGENERIC', 'SET', 'SETQ', 'SETF', 'LIST', 'CONS', 'QUOTE', 'COMPLEX', 'GCD', 'SIN', 'ASIN', 'COS', 'ACOS', 'TAN', 'ATAN', 'CTAN', 'ACTAN', 'SINH', 'COSH', 'TANH', 'ASINH', 'ACOSH', 'ATANH' 'ABS', 'SQRT', 'EXP', ''
                      'EXPT', 'ZEROP', 'EVENP', 'ODDP', 'ZEROP', 'NULL', 'LESSP', 'GREATERP', 'NUMBERP', 'STRINGP']

variable_types = ['sym', 'str', 'int', 'ratio',
                  'dec', 'clex', 'vec', 'lst', 'T', 'NIL']
lists = []  # lists of nodes, perhaps
variables = []
new_functions = {

}
trigo = ['SIN', 'ASIN', 'COS', 'ACOS', 'TAN', 'ATAN',
         'SINH', 'ASINH', 'COSH', 'ACOSH', 'TANH', 'ATANH']
lines_of_code = []  # lines of code used mainly for TEXT EDITOR and FILE modes


"""
TO DO LIST:
1. Fix the way that expressions are turned into lists, so spaces in strings don't matter.
2. Implement the list macro. -----  DONE  ------
3. Implement the cons macro. ----- HALF DONE -----
4. Check what to do if an attempt to create a variable which already exists is made .
"""


def clean_input(inserted):
    """ cleans the input """
    return inserted.strip().upper()


def check_valid_input(s_expression):
    """ returns True if  a single layer S_Expression is valid, else - False"""
    if s_expression[0] != '(' and s_expression[len(s_expression) - 1] != ')':
        temp = get_data_type(s_expression)
        if temp not in variable_types and temp not in variables:
            return False
    # Further checks should be placed here
    return True


def is_string(operand):
    """ checks if a given value is a string"""
    if operand.strip().startswith('"') and operand.strip().endswith('"'):
        return True
    return False


def is_integer(operand):  # 1 if true , 0 if not
    """ is of an integer type """
    if operand[0] == '-':
        operand = operand[1:]
    for char in operand:
        if char not in string.digits:
            return 0
    return 1


def number_but_not_integer(operand, sign):
    """ when the sign is '.' it checks for floating point and when '/' it checks for ratio """
    sign_counter = 0
    for char in operand:
        if char != sign and char not in string.digits:
            return 0
        elif char == sign:
            sign_counter += 1

        if sign_counter > 1:
            return 0
    if operand.find(sign) < 1 or operand.find(sign) > len(operand) - 2:
        return 0
    return 1


def is_even(number):
    """ Returns T if the number is even, else, return NIL"""
    if not isinstance(number, int):  # if the number isn't of type int, try to convert it to int.
        try:
            # if it's of type str and it can be converted to int
            if isinstance(number, str) and is_integer(number) == 1:
                number = int(number)
            # if not, then it's considered as invalid - thus a type error is raised.
            else:
                raise TypeError()
        # the type error is handled here. An error message to the user will be returned.
        except TypeError:
            return f"EVENP: {number} is not an integer "
    if number % 2 == 0:  # if the reesult number modulu 2 equals 0, it's an even , so return T .
        return 'T'
    return 'NIL'  # Else: return NIL, as it is odd.


def is_odd(number):
    """ Returns T if the number is odd, else, return NIL"""
    if is_even(number) == 'T':  # just return the opposite from the is_even method.
        return 'NIL'
    return 'T'


def equalp(value1, value2):
    """ Equals predicates """
    if value1 == value2:
        return 'T'
    return 'NIL'


def is_complex(expression):
    """ checks if an expression is a valid complex number"""

    if expression.startswith('#C'):
        first_bracket_index = expression.find('(')
        end_expression_index = expression.find(')')
        if first_bracket_index < 0 or end_expression_index < 0 or end_expression_index < first_bracket_index:
            # check if the brackets are not placed validly.
            return False
        # splits what's inside the brackets into a list
        operands = expression[3:-1].strip().split()
        if len(operands) > 2 or len(operands) == 0:
            return False
        if len(operands) == 1:
            operands.append(0)
        return True
    return False


# receives #C(A B ) and returns ( +  A ( * B i )  )
def simplify_complex(complex_number):
    operands = complex_number[3:-1].strip().split()
    return operands[0], operands[1]
    # return ' ( + {} ( *  {} i ) ) '.format(operands[0],operands[1])


def greatest_common_denominator(numerator, denominator):
    """ finds the greatest common denominator of 2 integers """
    min_digit = min(numerator, denominator)
    for i in range(min_digit, 0, -1):
        if numerator % i == 0 and denominator % i == 0:
            return i
    return -1


def gcd_list(numbers_list):
    """ returns the greatest common denominator of all the integers in a given list """
    gcd = abs(int(numbers_list[0]))
    for number in numbers_list:
        gcd = greatest_common_denominator(gcd, abs(int(number)))
        if gcd == 1:  # if it becomes 1 at any point it's pointless to continue, since it'll continue to be 1
            return 1
    if gcd == -1:
        return 0
    return gcd


def simplfy_variables(operands):
    """Replaces variable's names with their values """
    for i in range(len(operands)):
        is_variable = return_if_variable(operands[i])
        if is_variable[0]:
            operands[i] = str(is_variable[1].value)
    return operands


def simplify_ratio(ratio):
    """ simplifies the given ratio using the common denominator"""
    index = ratio.find('/')
    try:
        numerator = int(ratio[:index])
        denominator = int(ratio[index + 1:])
        gcd = greatest_common_denominator(numerator, denominator)
        if gcd == -1:
            return ratio
        return str(int(numerator / gcd)) + '/' + str(int(denominator / gcd))
    except TypeError as tp:
        print(tp.__class__)
        return -1


def ratio_to_decimal(ratio):
    """ converts ratio to decimal - in order to calculate it  """
    index = ratio.find('/')
    try:
        numerator = int(ratio[:index])
        denominator = int(ratio[index + 1:])
        return float(numerator / denominator)
    except TypeError as tp:
        print(tp.__class__)
        return -1


def is_ratio(operand):  # 1 if true, 0 if not
    """ is of a ratio type """
    return number_but_not_integer(operand, '/')


# used when the operands must be of only 1 type.
def one_type_in_list(lst, data_type):
    # For example, concatenate must get only string values.
    """ checks if all of the operands in the given list are in the same given type"""
    if data_type == 'str':
        for operand in lst:
            if not is_string(operand):
                return False
        return True
    elif data_type == 'int':
        pass
    elif data_type == 'ratio':
        pass
    elif data_type == 'dec':
        pass
    elif data_type == 'sym':
        pass


def is_floating_point(operand):  # 1 if true, 0 if not
    """ is a floating point"""
    return number_but_not_integer(operand, '.')

def match_types(my_str: str):
    """Convert the string to the datatype that it represents"""
    if is_integer(my_str):
        return int(my_str)
    if is_floating_point(my_str) or is_ratio(my_str):
        return float(my_str)
    if is_complex(my_str):
        return complex(my_str)
    return my_str # keep it otherwise a string
        
# used in a wrapper for operand list when the operands can be from more than 1 kind
def get_data_type(operand):
    """ Gets the data type of an operand """
    if operand is None or operand == '':
        return ''
    if is_complex(operand):
        return 'clex'
    if operand == 'T':
        return 'T'
    if operand == 'NIL':
        return 'NIL'
    if is_string(operand):  # can't do this yet
        return 'str'
    if operand.startswith("'") and not operand.endswith("'"):
        return 'sym'
    type_sum = is_integer(operand) + is_floating_point(operand) + is_ratio(operand) + is_string(
        operand)  # + is_symbol()
    if type_sum == 0:
        is_variable = return_if_variable(operand)
        if is_variable[0]:
            return is_variable[1]
        return "404"
    elif type_sum > 1:
        print(f'More than 1 type for {operand} was found')
    elif type_sum == 1:
        # If only one type found, as it should be
        if is_integer(operand) == 1:
            return 'int'
        if is_floating_point(operand) == 1:
            return 'dec'
        if is_ratio(operand) == 1:
            return 'ratio'
        if is_string(operand) == 1:
            return 'str'
        # check for is_symbol here

        else:
            return "404"
    else:
        return "404"


def clean_lst(lst):
    """ Removes redundant spaces which interrupts with correct execution of code"""
    for item in lst:
        if item.strip() in signs or item.strip() == '"':
            del item
    return lst


def return_if_variable(operand):
    """ Returns the operand's value as a variable, if it's not a variable: False"""
    for var_object in variables:
        if var_object.name == operand:
            return True, var_object
    return False, -1


def simplify_s_expression(s_expression):
    """ returns the result of a single layer s expression """
    if get_data_type(s_expression) == 'clex':
        print('found a complex number')
    command, operands = extract(s_expression)
    updated_operands = simplfy_variables(operands)
    # print(f'{operands} ARE THE OPERANDS')
    if command in built_in_functions:  # if the command exists
        if command == '+':  # ***********************  PLUS METHOD  ********************************
            sums = [0, 0]
            for operand in operands:
                operand_type = get_data_type(operand)
                if isinstance(operand_type, Variable):
                    operand = operand_type.value
                    operand_type = get_data_type(operand)
                if operand_type == 'int':
                    sums[0] += int(operand)
                elif operand_type == 'dec':
                    sums[0] += float(operand)
                elif operand_type == 'ratio':
                    sums[0] += ratio_to_decimal(operand)
                elif operand_type == 'clex':  # if received #C(4 3 )
                    print(f'{operand} is a complex number')
                    a, b = simplify_complex(operand)
                    sums[0] += a
                    sums[1] += b
            # print(sums)

            return sums[0]

        elif command == '-':  # *********************  MINUS METHOD  ********************************
            op = operands[0]
            operand_type = get_data_type(op)
            if isinstance(operand_type, Variable):
                op = operand_type.value
                operand_type = get_data_type(op)
            if operand_type == 'int':
                sums = int(op)
            elif operand_type == 'dec':
                sums = float(op)
            elif operand_type == 'ratio':
                sums = ratio_to_decimal(op)
            else:
                print('Type Error')
                return
            del operands[0]
            for operand in operands:
                operand_type = get_data_type(operand)
                if isinstance(operand_type, Variable):
                    operand = operand_type.value
                    operand_type = get_data_type(operand)
                if operand_type == 'int':
                    sums -= int(operand)
                elif operand_type == 'dec':
                    sums -= float(operand)
                elif operand_type == 'ratio':
                    sums -= ratio_to_decimal(operand)
            return sums
        elif command == '*':  # *********************  MULTIPLY METHOD  ********************************
            sums = 1
            for operand in operands:
                operand_type = get_data_type(operand)
                if isinstance(operand_type, Variable):
                    operand = operand_type.value
                    operand_type = get_data_type(operand)
                if operand_type == 'int':
                    sums *= int(operand)
                elif operand_type == 'dec':
                    sums *= float(operand)
                elif operand_type == 'ratio':
                    sums *= ratio_to_decimal(operand)
            return round(sums, 8)

        elif command == '=':
            sums = operands[0]
            for operand in operands:
                operand_type = get_data_type(operand)
                if isinstance(operand_type, Variable):
                    operand = operand_type.value
                if operand != sums:
                    return 'NIL'
            return 'T'
        elif command == '/':  # *********************  DIVIDE METHOD  ********************************
            op = operands[0]
            operand_type = get_data_type(op)
            if isinstance(operand_type, Variable):
                op = operand_type.value
                operand_type = get_data_type(op)
            if operand_type == 'int':
                sums = int(op)
            elif operand_type == 'dec':
                sums = float(op)
            elif operand_type == 'ratio':
                sums = ratio_to_decimal(op)
            else:
                print('Type Error')
                return
            del operands[0]
            for operand in operands:
                operand_type = get_data_type(operand)
                if isinstance(operand_type, Variable):
                    operand = operand_type.value
                    operand_type = get_data_type(operand)
                try:
                    if operand_type == 'int':
                        sums /= int(operand)
                    elif operand_type == 'dec':
                        sums /= float(operand)
                    elif operand_type == 'ratio':
                        sums /= ratio_to_decimal(operand)
                except ZeroDivisionError:
                    print('Cannot divide by 0 !')
            return sums
        elif command == 'EQ':  # *********************  EQ METHOD  ********************************
            if len(operands) < 2:
                raise Exception(f' not enough operators {len(operands)} ')
            if len(operands) > 2:
                raise Exception(f'Too much operators: {len(operands)}')
            if operands[0] == operands[1]:
                return 'T'
            return 'NIL'
        elif command == '=':
            op = operands[0]
            for operand in updated_operands:
                if operand != op:  # later on use more advanced predicates , such as equalp, perhaps.
                    return 'NIL'
            return 'T'
        elif command == 'CONCATENATE':  # ****************** CONCATENATE *******************************
            accumulator = ''
            for operand in operands:
                operand_type = get_data_type(operand)
                if isinstance(operand_type, Variable):
                    operand = operand_type.value
                    operand_type = get_data_type(operand)
                    if operand_type != 'str':
                        raise Exception(
                            'Concatenate Macro Receives Only Strings')
                accumulator += operand[1:-1]
            return '"' + accumulator + '"'
            # if one_type_in_list(operands, 'str'):
            #   return '"'+'' .join(map(lambda op: op[1:len(op) - 1], operands)) + '"'

        elif command == 'MAX':  # *********************************  MAX METHOD  **********************
            op = operands[0]
            operand_type = get_data_type(op)
            # if it's a variable, extract the value and its type
            if isinstance(operand_type, Variable):
                op = operand_type.value
                operand_type = get_data_type(op)
            if operand_type == 'int':
                max_number = int(operands[0])
            elif operand_type == 'dec':
                max_number = float(operands[0])
            elif operand_type == 'ratio':
                max_number = ratio_to_decimal(operands[0])
            else:
                raise Exception(
                    f"{operands[0]}: type {get_data_type(operands[0])} . MAX receives only numbers")
            current = max_number
            del operands[0]
            for op in operands:
                value = op
                operand_type = get_data_type(op)
                # if it's a variable, extract the value and its type
                if isinstance(operand_type, Variable):
                    value = operand_type.value
                    operand_type = get_data_type(value)
                if operand_type == 'int':
                    current = int(value)
                elif operand_type == 'dec':
                    current = float(value)
                elif operand_type == 'ratio':
                    current = ratio_to_decimal(value)
                else:
                    raise Exception(
                        f"{operands[0]}: type {get_data_type(operands[0])} . MAX receives only numbers")
                if current > max_number:
                    max_number = current
            return max_number
        elif command == 'MIN':  # *********************************  MIN METHOD  ************************
            if is_integer(operands[0]):
                min_number = int(operands[0])
            elif is_floating_point(operands[0]):
                min_number = float(operands[0])
            elif is_ratio(operands[0]):
                min_number = ratio_to_decimal(operands[0])
            else:
                raise Exception(
                    f"{operands[0]}: type {get_data_type(operands[0])} . MIN receives only numbers")
            current = min_number
            del operands[0]
            for op in operands:
                if is_integer(op):
                    current = int(op)
                elif is_floating_point(op):
                    current = float(op)
                elif is_ratio(op):
                    current = ratio_to_decimal(op)
                else:
                    raise Exception(
                        f"{operands[0]}: type {get_data_type(operands[0])} . MIN receives only numbers")
                if current < min_number:
                    min_number = current
            return min_number
        elif command == 'PRINT':  # prints with a new line  # ************* PRINT ***************
            if len(operands) > 1:
                raise Exception('print receives only one operand ')
            return "{}\n".format(operands[0])
        elif command == 'WRITE':  # prints without a new line # ************* WRITE ***************
            if len(operands) > 1:
                raise Exception('print receives only one operand ')
            return operands[0]
        elif command == 'IF':  # *****************************  IF  ****************************
            if len(operands) > 3:
                print('Invalid number of operands ')
            elif len(operands) == 3:
                if operands[0] == 'T':
                    return operands[1]
                elif operands[0] == 'NIL':
                    return operands[2]
                else:
                    print(f'{operands}')
        elif command == 'GCD':  # *************************************** GCD *********************************
            return gcd_list(updated_operands)
        elif command == 'ABS':
            return abs(int(updated_operands[0]))
        elif command == 'SETQ':  # ****************************** SETQ  ************************
            if len(operands) != 2:
                raise Exception('SETQ receives only 2 operands')
            if not return_if_variable(operands[0])[0]:
                variables.append(Variable(operands[0], operands[1]))
            else:
                print(f'Variable {operands[0]} already exists !')

            return operands[1]
        elif command == 'LIST':  # ********************************  LIST  ***************************
            first_item = GenericNode(operands[0])
            pos = first_item
            del operands[0]
            for operand in operands:
                pos.set_next(GenericNode(operand))
                pos = pos.next_node
            return first_item.wrap_str_()
        elif command == 'CONS':  # ********************************  CONS  ******************************
            if operands[-1] == 'NIL':
                del operands[-1]
            return ' '.join(operands)
            # return '(LIST ' + ' '.join(operands)+')'
        elif command == 'SQRT':
            if len(updated_operands) != 1:
                return f'INVALID NUMBER OF ARGUMENTS. EXPECTED 1, GOT {len(updated_operands)}'
            return str(sqrt(float(updated_operands[0])))
        elif command in trigo:
            # **************************  TRIGONOMETRY  ******************************
            if len(updated_operands) != 1:
                return f'INVALID NUMBER OF ARGUMENTS. EXPECTED 1, GOT {len(updated_operands)}'
            data_type = get_data_type(updated_operands[0])
            try:
                if data_type != 'dec' and data_type != 'int':
                    raise TypeError()
                if command == 'SIN':  # IN CASE THE COMMAND IS SINE
                    return str(round(sin(float(updated_operands[0])), 11))
                elif command == 'COS':  # IN CASE THE COMMAND IS COSINE
                    return str(round(cos(float(updated_operands[0])), 11))
                elif command == 'TAN':  # IN CASE THE COMMAND IS TANGENTS
                    return str(round(tan(float(updated_operands[0])), 11))
                elif command == 'ASIN':
                    return str(round(asin(float(updated_operands[0])), 11))
                elif command == 'ACOS':
                    return str(round(acos(float(updated_operands[0])), 11))
                elif command == 'ATAN':
                    return str(round(atan(float(updated_operands[0])), 11))
                elif command == 'SINH':
                    return str(round(sinh(float(updated_operands[0])), 11))
                elif command == 'SINH':
                    return str(round(cosh(float(updated_operands[0])), 11))
                elif command == 'TANH':
                    return str(round(tanh(float(updated_operands[0])), 11))
                elif command == 'ASINH':
                    return str(round(asinh(float(updated_operands[0])), 11))
                elif command == 'ACOSH':
                    return str(round(acosh(float(updated_operands[0])), 11))
                elif command == 'ATANH':
                    return str(round(atanh(float(updated_operands[0])), 11))
                else:
                    print('Trigonometric method not found.')
            except TypeError as te:
                print(f'TYPE {data_type.upper()} DOES NOT EXIST')
        elif command == 'EXP' or command == 'EXPT':
            if len(updated_operands) != 2 and len(updated_operands) != 1:
                return f'INVALID NUMBER OF ARGUMENTS. EXPECTED 1, GOT {len(updated_operands)}'
            data_type = get_data_type(updated_operands[0])
            try:
                if data_type != 'dec' and data_type != 'int':
                    raise TypeError()
                if command == 'EXPT':
                    return pow(float(updated_operands[0]), float(updated_operands[1]))
                if command == 'EXP':
                    return pow(e, float(updated_operands[0]))
            except TypeError:
                print(f'TYPE {data_type.upper()} DOES NOT EXIST')
        # *************************************  PREDICATES  *************************************8
        elif command == 'EVENP' or command == 'ODDP':
            if len(updated_operands) != 1:
                return f'INVALID NUMBER OF ARGUMENTS. EXPECTED 1, GOT {len(updated_operands)}'
            if command == 'EVENP':
                return is_even(updated_operands[0])
            return is_odd(updated_operands[0])
        elif command == 'ZEROP':
            if len(updated_operands) != 1:
                return f'INVALID NUMBER OF ARGUMENTS. EXPECTED 1, GOT {len(updated_operands)}'
            return equalp(updated_operands[0], '0')
        elif command == 'LESSP' or command == 'GREATERP':
            if len(updated_operands) != 2:
                return f'INVALID NUMBER OF ARGUMENTS. EXPECTED 1, GOT {len(updated_operands)}'
            if command == 'LESSP':
                return 'T' if float(updated_operands[0]) < float(updated_operands[1]) else 'NIL'
            return 'T' if float(updated_operands[0]) > float(updated_operands[1]) else 'NIL'

        elif command in new_functions:
            print('a user-defined function was called')
        else:
            print(f'COMMAND {command} DOES NOT EXISTS')


def simplify_layers(expression):
    """ receives an expression and simplifies all the layers in it """
    if expression.startswith(';'):
        return
    if expression.startswith('(') and expression.endswith(')'):
        # until one layer is left
        while expression.startswith('(') and expression.endswith(')'):
            start_index = expression.rfind(
                '(')  # a method to check if it's inside a string. iterates from both sides
            end_index = -1
            # print(f'start :{start_index}')

            for i in range(start_index, len(expression)):
                if expression[i] == ')':
                    end_index = i
                    break
            if end_index == -1:
                print('invalid end index ')
            # print(f'end: {end_index}')
            deepest_expression = expression[start_index:end_index + 1]
            if start_index > 1:
                if expression[start_index - 1] == 'C' and expression[
                        start_index - 2] == '#':  # recognized a complex number
                    deepest_expression = '#C' + deepest_expression
            # print(deepest_expression)
            if check_valid_input(deepest_expression):
                deepest_expression = simplify_s_expression(
                    deepest_expression)  # deepest_expression becomes its value
                # print(deepest_expression)
            else:
                raise Exception(f"Invalid Expression in {deepest_expression}")
            expression = expression[:start_index] + \
                str(deepest_expression) + expression[end_index + 1:]
        if expression.endswith(')'):
            return expression[:-1]
        return expression
    else:
        expression_type = get_data_type(expression)
        if expression_type == '404':
            print('INVALID.')
        else:
            if isinstance(expression_type, Variable):
                expression_value = expression_type.value
                return expression_value
            if expression_type == 'ratio':
                return simplify_ratio(expression)
            return expression


# RUN IT
def receive_expression():
    expression = clean_input(input('>>> '))
    while expression.count('(') != expression.count(')'):
        expression += ' ' + clean_input(input('... '))
    return expression


class Variable:
    def __init__(self, name, value, var_type="404"):
        """ Creates a new instance of class Variable"""
        # should the class perform checks, if they're done in the other side .. ?
        if var_type == '404':
            var_type = get_data_type(value)
        self.name = name
        self.value = value
        self.var_type = var_type

    # Index system like lisp? when two values are equal then just point to the list?

    def __str__(self):
        """ Prints the data about the variable """
        return " {}'s value is {} and its type is {} ".format(self.name, self.value, self.var_type)


# GLOBAL VARIABLES AT THE LISP ENVIRONMENT !
# should be in the start of the program. initializing i( root of -1 )
variables.append(Variable('I', 'clex'))
variables.append(Variable('PI', str(pi)))
variables.append(Variable('E', str(e)))


class GenericNode:
    def __init__(self, value, next_node=None):
        """ creates a new instance of GenericNode - a new node in the linked list."""
        self.value = value  # GENERIC VALUE
        self.next_node = next_node

    def has_next(self):
        """ Returns true if the next value isn't None, otherwise: False """
        return self.next_node is not None

    def set_next(self, next_node):
        """ Sets the next attribute which holds the GenericNode attribute"""
        if isinstance(next_node, GenericNode):  # GenericNode Objects Only
            self.next_node = next_node

    def get_next_value(self):
        """Returns the next GenericNode object's value property"""
        return self.next_node.value

    def set_next_value(self, value):
        """ Sets the next's GenericNode value property """
        self.next_node.value = value

    def get_length(self):
        """ Gets the number of items in the list. """
        counter = 0
        pos = self
        while pos is not None:
            counter += 1
            pos = pos.next_node
        return counter

    def __eq__(self, other):
        """ checks if two GenericNode lists are equal """
        if not isinstance(other, GenericNode):
            print(
                f"Can't compare between) {type(self)} and type {type(other)} ")
            return False
        if self.get_length() != other.get_length():
            return False
        pos_one = self
        pos_two = other
        while pos_one is not None and pos_two is not None:
            if pos_one.value != pos_two.value:
                return False
            pos_one = pos_one.next_node
            pos_two = pos_two.next_node
        return True

    def __str__(self):
        """ prints data about the current node """
        lst = '{} {}'.format(self.value, self.next_node).strip().upper()
        if lst.endswith('NONE'):
            lst = lst[:lst.rfind('NONE')]
        return lst

    def wrap_str_(self):
        """ prints data about the current node """
        lst = '{} {}'.format(self.value, self.next_node).strip().upper()
        if lst.endswith('NONE'):
            lst = lst[:lst.rfind('NONE')]
        return lst


class Function:

    # ******************  CONSTRUCTOR  *********************

    def __init__(self, name, number_of_parameters=0, parameters=[], number_of_return=0, return_values=[]):
        """ Creates a new instance of class Function, and assigns the required parameters."""
        self.name = name  # str
        self.number_of_parameters = number_of_parameters  # int
        self.number_of_return = number_of_return  # int
        self.parameters = parameters  # list
        self.return_values = return_values

    # ********************  SETS  *********************

    def set_number_of_parameters(self, number_of_parameters):
        """ set the number of parameters that the function can receive """
        self.number_of_parameters = number_of_parameters

    def set_parameters(self, parameters):
        """ sets the value of the parameters."""
        self.parameters = parameters

    def set_number_of_return(self, number_of_return):
        self.number_of_return = number_of_return

    def set_name(self, name):
        self.name = name

    def set_return_values(self, return_values):
        self.return_values = return_values

    # ********************  GETS  *********************

    def get_number_of_parameters(self):
        return self.number_of_parameters

    def get_parameters(self):
        return self.parameters

    def get_number_of_return(self):
        return self.number_of_return

    def get_name(self):
        return self.name

    def get_return_values(self):
        return self.return_values

    # *****************     METHODS   ***********************
    def generate_parameters_as_variables(self):
        pass

    def execute(self):
        pass

    def fill_properties(self):
        pass

    #  *****************  STATIC METHODS  *****************

    # ****************** __STR__() *********************
    def __str__(self):
        return f'Function {self.name} receives {self.number_of_parameters} : {self.parameters}, and returns ' \
               f' {self.number_of_return} values : {self.return_values}'


def run_a_list_of_code(lst_of_code):
    """Executes a list of code. Necessary for Text-Editor and File mode. Perhaps for looping too."""
    index = 1
    for line in lst_of_code:
        line = clean_input(line)
        if not check_valid_input(line):
            print(f'Error in line {index}')
            break
        print(simplify_layers(line))
        index += 1


def export_code_to_file(name_of_file, code_list):
    """ creates a file with the specified name and inserts the code in there"""
    # check if it ends with a valid ending
    if os.path.exists(name_of_file):  # if the path already exists
        answer = clean_input(input('The file already exists. ADD to append the code, CHOOSE to rewrite it, or any other'
                                   ' key to re-write it  '))
        if answer == 'ADD':
            print('code should be appended')
        elif answer == 'CHOOSE':
            name_of_file = input('New name: ').strip()
            export_code_to_file(name_of_file, code_list)
        else:
            with open(name_of_file, 'wt') as name_of_file:
                for line in lines_of_code:
                    name_of_file.write(line + '\n')
    else:
        with open(name_of_file, 'wt') as name_of_file:
            for line in lines_of_code:
                name_of_file.write(line + '\n')


def export_wrapper(lst_of_code=lines_of_code):
    """ manages the exportation of code to files """
    answer = input('Do you want to save your work? ').strip().upper()
    while answer in not_sure:
        print('If you are not sure, the recommendation is to save your work.')
        answer = input('Do you want to save your work? ').strip().upper()
    if answer in agreement:
        print('Your code is:')
        for line in lines_of_code:
            print(line)
        name_of_file = input("File's name:").strip()
        export_code_to_file(name_of_file, lst_of_code)


def extract(expression):
    """ returns a tuple of the command ( type str ) , and the operands ( type list ) """
    content = expression[1:len(expression) - 1]
    content = content.strip()
    command = content[:content.find(' ')]  # content = command a b c d
    content = content[content.find(' '):].strip()  # content = a b c d
    operands = []
    accumulator = ""
    i = 0
    while i < len(content):
        if content[i] == '"':
            j = i + 1  # i is the index of the " sign - therefore we increase the index in order to not include it
            while j < len(content) and content[j] != '"':
                j += 1
            # add to the operands_list the characters between the " "
            operands.append(content[i:j + 1])
            i = j
        else:
            if content[i] == ' ':
                if accumulator.strip() != '':
                    operands.append(accumulator)
                accumulator = ''
            else:
                accumulator += content[i]
        i += 1
    if accumulator.strip() != '':
        operands.append(accumulator)

    return command, operands


def eval_lisp(lisp_code: str):
    """ The method receives a string that represents a lisp expression and evaluates it.
    The result is returned
    """
    clean_code = clean_input(lisp_code)
    result = simplify_layers(clean_code)
    typed_result = match_types(result)
    return typed_result


def run():
    """ The main method."""

    intro_font = Figlet(font='standard')
    print(intro_font.renderText('LISPER '), end='')
    print('Version 1.0.3')

    try:
        user_choice = clean_input(
            input('Choose your mode: REPL, FILE, OR TEXT EDITOR  '))
        if user_choice == 'REPL' or user_choice == 'CONSOLE':
            while True:
                try:
                    command = receive_expression()
                    command = clean_input(command)
                    if command == '%FINISH':
                        break
                    final_result = simplify_layers(command)
                    if final_result is not None:
                        print(final_result)
                    lines_of_code.append(command)
                except KeyboardInterrupt:
                    print()
                    print(
                        'Program has stopped unexpectedly... Going back to the command line..')
            export_wrapper(lines_of_code)
        elif user_choice == 'TEXT' or user_choice == 'TEXT EDITOR' or user_choice == 'EDITOR':
            # implement text editor mode here
            index = 1
            while True:
                print(f'{index}. ', end=' ')
                line = clean_input(input())
                if line == '%FINISH' or line == '%EXIT':
                    break
                lines_of_code.append(line)
                index += 1
            run_a_list_of_code(lines_of_code)
            export_wrapper()
            pass
        elif user_choice == 'FILE' or user_choice == 'IMPORT':
            # implement file import mode here
            name = input("File's name and/or path:  ")
            if not os.path.isfile(name):
                print(f"{name} does not exists in the specified context")
            else:
                with open(name, 'rt') as file:
                    for line in file:  # adding each line as an item in the list of code
                        lines_of_code.append(line)
                    run_a_list_of_code(lines_of_code)
    except KeyboardInterrupt as kb:
        print(' \n EXECUTION HAS BEEN CLOSED BY THE USER')

run()
