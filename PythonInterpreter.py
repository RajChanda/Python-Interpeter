import math
import copy

# few important lists used in the program
BINARY_OPERATOR = ["+", "-", "*", "/", ">", "<", "<=", ">=", "==", "!=", "and", "or"]
OPERATIONS = ["+", "-", "*", "/"]
UNARY_OPERATOR = ["-", "not"]
OPERATORS = ['True', 'False', 'and', 'or', 'not']
COMPARISON_OPERATORS = ["=", ">", "<", "<=", ">=", "==", "!=", "and", "or"]
SPECIAL_BOOLEAN_OPERATORS = ['True', 'False']
TYPE_list = ['BLE', 'BLT', 'BE', 'Branch']


# HELPER FUNCTIONS

# Intersection of two lists
def intersection(lst1, lst2):
    lst3 = [value for value in lst1 if value in lst2]
    return lst3


# Following functions are used for the execution part of the statements
# All of them have constant time complexity O(1)
# For BLE execution
def BLE_execution(arg1, arg2):
    if int(arg1) <= int(arg2):
        return True
    else:
        return False


# For BLT execution
def BLT_execution(arg1, arg2):
    if int(arg1) < int(arg2):
        return True
    else:
        return False


# For BE execution
def BE_execution(arg1, arg2):
    if int(arg1) == int(arg2):
        return True
    else:
        return False


# This function is used to handle while statements of the final_instruction_list
def while_statement_execution(l):
    # INPUT : l list of following syntax
    #           [type(BLE, BLT, BE), arg1, arg2, target_index]
    #       or  [Branch, target_index]
    # OUTPUT : Boolean value of condition, target_index
    type = l[0]
    if type in TYPE_list[:3]:
        arg1 = l[1]
        arg2 = l[2]
        if type == 'BLE':
            return BLE_execution(arg1, arg2), l[3]
        elif type == 'BLT':
            return BLT_execution(arg1, arg2), l[3]
        elif type == 'BE':
            return BE_execution(arg1, arg2), l[3]
    # If type Branch, then always False because it is necessary to go to the target index
    else:
        if type == 'Branch':
            return False, l[1]


# Used to print garbage values and values of variables
def print_variable_garbage_values(GARBAGE, DATA):
    # referenced_values list contains the values from DATA list which are referred by some variable
    referenced_values = []
    print('value of the variables')
    for elements in DATA:
        if type(elements) == tuple:  # check the elements in DATA which are of tuple type
            variable = elements[0]
            value = DATA[elements[1]]
            referenced_values.append(value)  # Append the values which are referenced by the variables
            # also print these values as they are the final values of the variables defined in the input file

            print(variable + " : " + str(value), end="   ")
    req_list = intersection(GARBAGE, referenced_values)
    for values in req_list:
        GARBAGE.remove(values)
    for elements in DATA:
        k = 0
        # for each element in DATA, check if it is in the referenced_values list
        found = False
        for k in range(0, len(referenced_values)):
            # Using 'is' operator instead of == because True/False are distinguished from 1/0 by 'is'
            if referenced_values[k] is elements:
                found = True  # update found variable to True
                break  # immediately exit the loop
        # If element not found in referenced_values list and if element is not a tuple => GARBAGE VALUE
        if not found and type(elements) != tuple:
            # print(elements)  # print the GARBAGE VALUE
            GARBAGE.append(elements)  # append it in the GARBAGE lst
    print('')
    print('GARBAGE list')
    print(GARBAGE)


# This has time complexity of O(len(DATA_list))

# MAIN PROGRAM STARTING FROM HERE


lines = []  # initialise to empty list

tab_for_while_loop = -1
# initial instruction list, not the final one
instruction_list = []
with open('input_file.txt') as f:
    lines = f.readlines()  # read all lines into a list of strings
count_line = 0
for statement in lines:  # each statement is on a separate line
    count_line += 1
    statement = statement.replace("    ", '\t')  # used from piazza given by some instructor
    statement = statement.replace(":", ' :')
    tabs = 0
    while statement[tabs] == '\t':
        tabs = tabs + 1

    # values in this instruction_list of the form

    # [line_count, tab count, whether while statement or not(boolean value), [general statement: none if while],
    #                                                                   [statement of while: none if normal line]]

    # converting the while statements and appending them in the instruction_list

    if 'while' in statement:
        token_list_1 = statement.split()
        # when no statement is given in while => error
        if len(token_list_1) == 1:
            print('error => incomplete while statement')
            exit()
        tab_for_while_loop = tabs
        while_statement = token_list_1[1:-1]
        # None because no general statement
        instruction_list.append([count_line, tabs, True, None, while_statement])
    else:
        evaluation_statement = statement.split()
        instruction_list.append([count_line, tabs, False, evaluation_statement, None])

# Time complexity = O(max{len(statements)} * number of input lines)

# Complete DATA_list initialised form an empty list
DATA_list = []


# This function is used to make the instruction list
def making_instruction_list(final_instruction_list, instruction_list):
    # OUTPUT : The final_instruction_list

    # Initial Number of tabs, this variable is used for handling while loop
    tab_1 = 0  # indicates the recent while loop that is handled
    # This list stores the indexes where the while list conditions are present in the final_instruction_list
    while_list = []
    # Initial Tab list, stores the tabs of while loops
    tab_list = [0]

    n = len(instruction_list)
    for i in range(n):
        # working_list for each list of the instruction_list
        # syntax of working_list => [line of input file, tab_count, boolean value whether while or not,
        #                                      general statement(only if no while), while statement(when while present)]
        working_list = instruction_list[i]
        # check if while or not
        if working_list[2] == False:  # if not while
            # check if tab_count is same as the recent while loop handled
            if working_list[1] == tab_1:
                # If yes, that means this statement is part of this while loop (only if tab_1 =\= 0, else)
                # append the general statement => present at 3rd index of working_list
                final_instruction_list.append(working_list[3])
            else:
                # If no, that means statement is outside the while loop (end of the recent while loop)
                if tab_1 - working_list[1] < 0:  # if tab increases without the presence of while => wrong syntax
                    print('error, wrong syntax at line', working_list[0])
                    exit()
                else:
                    # means we need to put the 'Branch' statement in final_instruction_list
                    for m in range(tab_1 - working_list[1], 0, -1):
                        # while_list[-1] gives the target_index
                        final_instruction_list.append(['Branch', while_list[-1]])
                        final_instruction_list[while_list[-1]].append(len(final_instruction_list))
                        final_instruction_list.append(working_list[3])
                        tab_1 = tab_1 - 1  # decrease the tab count by 1
                        # remove the last while loop since it is exited
                        while_list.pop()
        else:  # if while
            tab_1 = working_list[1] + 1  # increase tab count by 1 since now this is the recent while loop to be handled
            # Use type_identifier function to find what= type of while => BLE, BLT, BE
            final_instruction_list.append(type_identifier(working_list[-1]))
            # append the new while loop in both while_list and tab_list
            while_list.append(len(final_instruction_list) - 1)
            tab_list.append(working_list[1] + 1)

    return final_instruction_list


# This has time complexity of O(len(instruction_list))  which is approximately equal to O(len(number of lines))


# Used to identify the type : BLE, BLT, BE, Branch
def type_identifier(l):
    # INPUT : list l which contains a statement in the form of list
    # OUTPUT : list of form [type of condition, arg1, arg2] where arg are the values which are compared

    COMPARISON = [">", "<", "<=", ">=", "!="]
    not_of_COMPARISON = ["<=", ">=", ">", "<", "=="]  # the negation of the COMPARISON values, written for understanding
    found = False  # find the comparison operator which is present in l
    for signs in COMPARISON:
        # find the sign in l
        if signs in l:
            index_of_comparison = l.index(signs)  # find the index at which comparison is done in l
            I = COMPARISON.index(signs)  # find the index of the sign as I
            found = True  # change found to True
            break  # exit the loop immediately
    # if sign not found => error
    if found == False:
        print("error, invalid syntax with no valid comparison given in while statement")
        exit()
    # Combining the two values on the either side of the comparison operator as two values: arg1, arg2
    arg1_list = l[:index_of_comparison]
    arg2_list = l[index_of_comparison + 1:]
    arg1 = ''
    arg2 = ''
    for values in arg1_list:
        arg1 = arg1 + values
    for values in arg2_list:
        arg2 = arg2 + values
    if arg1.isnumeric() == True:
        arg1 = int(arg1)
    if arg2.isnumeric() == True:
        arg2 = int(arg2)
    # Doing manually, and assigning BLE, BLT, BE to the comparison condition
    if I == 0:
        return ['BLE', arg1, arg2]
    elif I == 1:
        return ['BLE', arg2, arg1]
    elif I == 2:
        return ['BLT', arg2, arg1]
    elif I == 3:
        return ['BLT', arg1, arg2]
    elif I == 4:
        return ['BE', arg1, arg2]


# Constant time complexity O(1)

# CLASS INSTRUCTIONS
class Instructions:

    # two attributes,= : instruction_list and DATA_list
    def __init__(self, l, k):
        self.instruction_list = l
        self.DATA_list = k

    # method to change the variables into respective values from DATA_list
    # similar to helper function used in part1 of Assignment
    def change_variable_value(self, l1, start, k):
        # l1 : list in which replacements are made (token_list)
        # start : start index of list l
        # k : list in which the values of the variables are stored (DATA_list) such that it has no duplicates
        # OUTPUT : updated l and k and count of number of terms in the list k

        l = copy.deepcopy(l1)
        end = len(l)
        term_count = 0  # keeps track of number of terms that are given in input line
        j = start
        for j in range(start, end):
            if type(l[j]) == int:
                l[j] = l[j]
            elif l[j] == 'True' or l[j] == 'False':  # if boolean expression
                term_count = term_count + 1  # update term_count by +1
                a = l[j] == 'True'  # Converting the str value into boolean
                found = False
                for elements in k:
                    # Using 'is' operator instead of == because True/False are distinguished from 1/0 by 'is'
                    if elements is a:
                        found = True  # value found in k
                        break  # exit the loop immediately

                if not found:  # value not available in k
                    k.append(a)  # append it

            elif l[j].isnumeric() == True:  # if numeric value encountered
                term_count = term_count + 1  # update term_count by +1
                found = False
                for elements in k:
                    if elements is int(l[j]):
                        found = True  # found value in k
                        break  # exit loop immediately
                if not found:  # if not found
                    k.append(int(l[j]))  # append the value

            elif l[j].isalpha() == True and l[j] not in OPERATORS:  # if variable encountered
                term_count = term_count + 1  # update term_count by +1
                for elements in k:
                    if type(elements) == tuple and l[j] in elements:
                        l[j] = str(k[elements[1]])  # replacing its value

        return l, k, term_count

    # Time complexity of O(len(l1))

    # method to evaluate a statement
    def evaluate_statement(self, l, start, DATA_list, count):
        # INPUT : l list which contains the statement
        #         start index
        #         DATA_list
        #         count : line count (for error identification)
        # OUTPUT : No output, modifies the DATA_list and the l list of statement

        # This method is similar to the program used in the first part of the assignment
        token_list = copy.deepcopy(l)
        token_list, DATA_list, term_count = self.change_variable_value(token_list, start, DATA_list)    # O(l)
        count = count

        # THIS LOOP IS USED TO FIND ERROR: if any variable is not replaced => no reference found for it => error
        k = len(token_list) - 1
        for k in range(len(token_list) - 1, 0, -1):  # if variable used which is not defined earlier
            if token_list[k].isalpha() == True and token_list[k] not in OPERATORS:  # i.e. if any variable left on RHS
                print("error line: " + str(count) + " => type : NameError, " + token_list[k] + " is not defined")
                exit()
        for elements in OPERATORS:  # if numbers used with boolean values
            if elements in token_list:
                for k in range(0, len(token_list)):
                    if token_list[k].isnumeric() == True:
                        print("error line: " + str(count) + " => type : TypeMismatch ")
                        exit()
        if term_count > 2:  # MAXIMUM number of terms should be 2 as given in assignment sheet
            print(term_count)
            print("error line: " + str(count) + ", number of terms exceeding the limit")
            exit()
        for x in OPERATORS:  # this loop for error when boolean values used with arithmetic operators
            if x in token_list:
                for y in OPERATIONS:
                    if y in token_list:
                        print("error line: " + str(count) + " => type : TypeMismatch ")
                        exit()

        # Concatenating the string values in token_list starting from start index
        s = token_list[start]  # stores the concatenated values
        j = start + 1  # index
        for j in range(start + 1, len(token_list)):
            s = s + ' ' + token_list[j]

        # Using eval() to evaluate s and storing it in variable 'value'
        try:
            value = eval(s)
        except:
            print('INVALID SYNTAX ERROR in line : ' + str(count))
            exit()
        # converting float to int (this interpreter works only for integer values) using floor function
        if type(value) == float:
            value = math.floor(value)

        found_value = False
        index = -1  # keeps count of index of DATA
        for elements in DATA_list:
            index = index + 1  # update index each time for every element in DATA
            if elements is value:  # Using 'is' operator instead of == because True/False are distinguished from 1/0 by 'is'
                I = index  # I variable IS USED TO KEEP TRACK OF REFERENCE VALUE (INDEX VALUE TO BE STORED)
                found_value = True  # if value is found in DATA, save the index of that element in I and update found_value
                break  # exit loop immediately
        if found_value == False:  # If value not found in DATA
            DATA_list.append(value)  # append it in the DATA list
            I = len(DATA_list) - 1  # I becomes the index of last elements

        # NOW WE ARE FINDING WHETHER THE VARIABLE ON LHS IN INPUT LINE HAS ALREADY BEEN REFERRED PREVIOUSLY OR NOT :-
        VARIABLE_EXIST = False
        for elements in DATA_list:
            # if previously referred, then change the index value to new index value (I)
            if type(elements) == tuple and token_list[0] == elements[0]:  # Using two conditions for precise search
                # Changing the reference to I
                k = DATA_list.index(elements)
                elements = list(elements)
                elements[1] = I
                elements = tuple(elements)
                DATA_list[k] = elements
                VARIABLE_EXIST = True  # Updating to True if VARIABLE EXISTS
        if not VARIABLE_EXIST:  # if variable does not exist
            DATA_list.append((token_list[0], I))  # append the variable with its reference value

    # This has time complexity of O(max{len(l), len(DATA_list)} * len(l))

    # This method executes the lines of the final_instruction List
    def line_execution(self, DATA_list):
        # INPUT : DATA_list, garbage_list
        # prints the whole program values and executes all the lines

        # FOR INFINITE LOOP HANDLING, these two variables are used
        count = 0
        value_check = []

        instruction_list = self.instruction_list
        # i will be the pointer which will be moving along the instruction_list
        i = 0
        n = len(instruction_list)
        while i < n:  # along the whole list        # O(number of input lines)
            # defined working_list on which operations will be done at a time
            working_list = copy.deepcopy(instruction_list[i])
            # If there is no BLE, BLT, BE, Branch in the working_list
            if not intersection(working_list, TYPE_list):
                # we evaluate the working_list using function used in the first part of the assgn
                self.evaluate_statement(working_list, 2, DATA_list, i + 1)     # assuming O(len(DATA_list)) == O(length of input statement)
                i = i + 1  # increment the value of i                          # O(max{len(length of input statement)}^2)

            # If 'Branch' is present in the working_list
            elif intersection(working_list, TYPE_list) == ['Branch']:
                # simply shift the pointer to the target index
                i = working_list[1]

                # This is used to check if there is INFINITE LOOP
                l = value_check[-1]

                # Check the value of the arguments of while loop after reaching the 'Branch'
                present_value, DATA_list, term_count = self.change_variable_value([l[1], l[2]], 0, DATA_list)
                # IF the value is same, increase the count by 1
                if present_value == l[3][1:3]:
                    count = count + 1

                # For this while loop, if the value of this count becomes greater than 998, then it is infinite loop.
                # ERROR
                if count > 998:
                    print('error => infinite loop')
                    exit()
                # O(1)
                # Whenever 'Branch' is reached, one iteration of the loop ends
                # Print the variable values and the garbage values
                # print_variable_garbage_values([], DATA_list)
                print_variable_garbage_values([], DATA_list)

            # If either of the BLE, BLT, BE present in the working_list
            elif intersection(working_list, TYPE_list) == ['BLT'] or ['BLE'] or ['BE']:

                # first change the values of variables to their values from the DATA_list
                # Using the change_variable_value method

                req_list, DATA_list, term_count = self.change_variable_value([working_list[1], working_list[2]], 0,
                                                                             DATA_list)
                # each time BLE, BLT, BE is handled, append the arg values with the index of this while
                value_check.append([i, working_list[1], working_list[2], req_list])
                # print(value_check)
                # CHECK if some variable is not converted to value => no reference found => error
                token_list = req_list
                for k in range(len(token_list) - 1, -1, -1):  # if variable used which is not defined earlier
                    if type(token_list[k]) == int:
                        pass
                    elif token_list[k].isalpha() == True and token_list[
                        k] not in OPERATORS:  # i.e. if any variable left on RHS
                        print("error => type : NameError, " + token_list[k] + " is not defined")
                        exit()

                # Convert the req_list obtained from change_variable_value method to general syntax
                req_list.insert(0, working_list[0])
                req_list.append(working_list[-1])

                # evaluate this statement and find whether it True or False
                bool_value, target_index = while_statement_execution(req_list)

                # If False => condition of while loop fulfilled => move to the next index of instruction_list
                if bool_value == False:
                    i = i + 1
                # Else, move to the target index of the while loop
                else:
                    i = target_index
    # Expected time complexity = O(max{len of input statements}^2 * number of input lines)

# INITIALISED THE final_instruction_list to []
final_instruction_list = []

# first the final_instruction_list is made
final_instruction_list = making_instruction_list(final_instruction_list, instruction_list)

# An instruction_set object is created
# Two attributes : final_instruction_list and DATA_list
instruction_set = Instructions(final_instruction_list, DATA_list)

# execute the instruction set lines using line_execution method
# line_execution method is the main method which finally executes the whole final_instruction_list
instruction_set.line_execution(DATA_list)

# Printing the final variables and there values and the garbage values
print('--------------------------------------------------------------')
print('Final values : variables and the garbage list ')
print_variable_garbage_values([], DATA_list)
print('THE INSTRUCTION LIST')
# # Printing the final_instruction_list at the end of the program
print(final_instruction_list)

# NOTE : values of variables and garbage list are printed after loop iteration. Instruction list is printed at the end

"""
***************************************************************************************************************
TEST CASES AND THEIR TIME COMPLEXITIES

# I have tried to do general time complexity analysis under each function


TEST 1 :-
INPUT LINES :-
b = 3
x = 3
y = 4
z = 2
while x <= 7 :
    x = x + 1
    y = y + 1
    while y < 10 :
        z = z + 1
        y = y + 1
a = 10

OUTPUT :-
value of the variables
b : 3   x : 4   y : 6   z : 3   
GARBAGE list
[2, 1, 5]
value of the variables
b : 3   x : 4   y : 7   z : 4   
GARBAGE list
[2, 1, 5, 6]
value of the variables
b : 3   x : 4   y : 8   z : 5   
GARBAGE list
[2, 1, 6, 7]
value of the variables
b : 3   x : 4   y : 9   z : 6   
GARBAGE list
[2, 1, 5, 7, 8]
value of the variables
b : 3   x : 4   y : 10   z : 7   
GARBAGE list
[2, 1, 5, 6, 8, 9]
value of the variables
b : 3   x : 4   y : 10   z : 7   a : 10   
GARBAGE list
[2, 1, 5, 6, 8, 9]
value of the variables
b : 3   x : 5   y : 11   z : 7   a : 10   
GARBAGE list
[4, 2, 1, 6, 8, 9]
value of the variables
b : 3   x : 6   y : 12   z : 7   a : 10   
GARBAGE list
[4, 2, 1, 5, 8, 9, 11]
value of the variables
b : 3   x : 7   y : 13   z : 7   a : 10   
GARBAGE list
[4, 2, 1, 5, 6, 8, 9, 11, 12]
value of the variables
b : 3   x : 8   y : 14   z : 7   a : 10   
GARBAGE list
[4, 2, 1, 5, 6, 9, 11, 12, 13]
--------------------------------------------------------------
Final values : variables and the garbage list 
value of the variables
b : 3   x : 8   y : 14   z : 7   a : 10   
GARBAGE list
[4, 2, 1, 5, 6, 9, 11, 12, 13]
THE INSTRUCTION LIST
[['b', '=', '3'], ['x', '=', '3'], ['y', '=', '4'], ['z', '=', '2'], ['BLT', 7, 'x', 13], ['x', '=', 'x', '+', '1'], ['y', '=', 'y', '+', '1'], ['BLE', 10, 'y', 11], ['z', '=', 'z', '+', '1'], ['y', '=', 'y', '+', '1'], ['Branch', 7], ['a', '=', '10'], ['Branch', 4], ['a', '=', '10']]


TEST 2:-
INPUT LINES :-
a = 1
b = 2
while a < 5:
    a = a + 1
    b = b + 1
c = a + b
while b > a:
    b = b - 1
c = a - b

OUTPUT :-

value of the variables
a : 2   b : 3   
GARBAGE list
[1]
value of the variables
a : 3   b : 4   
GARBAGE list
[1, 2]
value of the variables
a : 4   b : 5   
GARBAGE list
[1, 2, 3]
value of the variables
a : 5   b : 6   
GARBAGE list
[1, 2, 3, 4]
value of the variables
a : 5   b : 5   c : 11   
GARBAGE list
[1, 2, 3, 4, 6]
--------------------------------------------------------------
Final values : variables and the garbage list 
value of the variables
a : 5   b : 5   c : 0   
GARBAGE list
[1, 2, 3, 4, 6, 11]
THE INSTRUCTION LIST
[['a', '=', '1'], ['b', '=', '2'], ['BLE', 5, 'a', 6], ['a', '=', 'a', '+', '1'], ['b', '=', 'b', '+', '1'], ['Branch', 2], ['c', '=', 'a', '+', 'b'], ['BLE', 'b', 'a', 10], ['b', '=', 'b', '-', '1'], ['Branch', 7], ['c', '=', 'a', '-', 'b']]



TEST 3 :-
INPUT LINES:-

i = 0
    while i < 3 :
    j = 1
    while j < 2 :
    x = i + j
    j = j + 1
    i = i + 1
y = 0

This is case of infinite loop
OUTPUT :- 
error => infinite loop


"""
