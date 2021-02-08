digits = {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.'}
operators = {'+', '-', '*', '/', '^', '(', ')'}
# Arithmetic operations dictionary.
operations = {'+': lambda x, y: x + y, '-': lambda x, y: x - y,
              '*': lambda x, y: x * y, '/': lambda x, y: x / y,
              '^': lambda x, y: x ** y}
precedence = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3, '(': 4, ')': 4}


class ParserException(Exception):
    def __init__(self, message):
        self.message = message


class Tree:
    def __init__(self, l, r, d):
        self.left = l
        self.right = r
        self.data = d

    def eval(self) -> float:
        """
        Evaluates the expression contained in the parse
        tree recursively
        """
        if self.data not in operators:
            return self.data

        # In normal conditions this try/catch statement
        # will never catch the exception: the expression
        # has been curated in the parsing phase, and any weird
        # character has been dealt with (with the proper parser
        # exception module).
        try:
            operand1 = float(self.left.eval())
            operand2 = float(self.right.eval())
        except ValueError:
            print("This shouldn't have happened")

        return operations[self.data](operand1, operand2)

class Parser:
    def __init__(self):
        self.tree_stack = []
    
    def __parse_tree(self, token: str):
        if not token:
            raise ParserException("Invalid Syntax")
  
        tree = Tree(None, None, token)

        if tree.data in operators:
            try:
                tree.right = self.tree_stack.pop()
                tree.left = self.tree_stack.pop()
            except IndexError:
                raise ParserException("Invalid Syntax")

        self.tree_stack.append(tree)


    def parse(self, tokens: str) -> Tree:
        i = 0
        operator_stack = []
        number = ""  # Add the digits to our number.
        
        while i < len(tokens):
            if tokens[i] not in operators and tokens[i] not in digits:
                raise ParserException("Invalid Token")

            # Let's create our operands with the digits we find.
            while i < len(tokens) and tokens[i] not in operators:
                number += tokens[i]
                i += 1

            if number:
                self.__parse_tree(number)
                number = ""  # Let's delete our string so we can start anew.

            if i >= len(tokens):
                break
            
            if tokens[i] != '(' and tokens[i] != ')':
                while (operator_stack
                       and precedence[operator_stack[-1]] >= precedence[tokens[i]]
                       and operator_stack[-1] != '('):
                    self.__parse_tree(operator_stack.pop())
                    
                operator_stack.append(tokens[i])

            elif tokens[i] == '(':
                operator_stack.append(tokens[i])
            else:  # The token is a right parenthesis.
                while operator_stack and operator_stack[-1] != '(':
                    self.__parse_tree(operator_stack.pop())

                if not operator_stack:
                    raise ParserException("Mismatched parenthesis")

                if operator_stack[-1] == '(':
                    operator_stack.pop()
            i += 1

        while operator_stack:
            if operator_stack[-1] == '(' or operator_stack == ')':
                raise ParserException("Mismatched parenthesis")

            self.__parse_tree(operator_stack.pop())

        tree = self.tree_stack.pop()

        if self.tree_stack:
            raise ParserException("Invalid syntax")

        return tree
