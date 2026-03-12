import re
import math

class ExpressionEvaluator:
    """
    Main Expression Evaluator class that handles:
    - Tokenization of input expressions
    - Infix to Postfix conversion using Shunting Yard Algorithm
    - Postfix expression evaluation using stack-based approach
    - Variable and function support
    """
    
    def __init__(self):
        """
        Initialize the evaluator with:
        - Operator precedence levels (higher number = higher precedence)
        - Right associative operators (like power ^)
        - Supported mathematical functions mapped to Python math library
        - Variable storage dictionary
        """
        self.precedence = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3}
        self.right_assoc = {'^'}
        self.functions = {'sin': math.sin, 'cos': math.cos, 'tan': math.tan, 
                         'sqrt': math.sqrt, 'log': math.log, 'exp': math.exp}
        self.variables = {}
    
    def tokenize(self, expr):
        """
        Tokenization Component:
        Breaks the input expression string into individual tokens.
        
        Process:
        1. Remove all whitespace from expression
        2. Use regex to extract:
           - Numbers (integers and decimals): \d+\.?\d*
           - Variables/Functions (identifiers): [a-zA-Z_]\w*
           - Operators and parentheses: [+\-*/^()]
        
        Example: "3 + 4 * 2" → ['3', '+', '4', '*', '2']
        """
        return re.findall(r'\d+\.?\d*|[a-zA-Z_]\w*|[+\-*/^()]', expr.replace(' ', ''))
    
    def infix_to_postfix(self, tokens):
        """
        Infix to Postfix Conversion Component (Shunting Yard Algorithm):
        Converts infix notation to postfix (Reverse Polish Notation).
        
        Algorithm:
        1. Create output queue and operator stack
        2. For each token:
           - If NUMBER: add directly to output
           - If VARIABLE: add to output (unless it's a function)
           - If FUNCTION: push to stack
           - If '(': push to stack
           - If ')': pop stack to output until '(' found, then pop '('
           - If OPERATOR: pop higher/equal precedence operators to output, then push current
        3. Pop remaining operators from stack to output
        
        Example: "3 + 4 * 2" → ['3', '4', '2', '*', '+']
        
        This ensures correct operator precedence and associativity.
        """
        output, stack = [], []
        for token in tokens:
            # If token is a number, add to output
            if re.match(r'\d+\.?\d*', token):
                output.append(token)
            # If token is a variable or function name
            elif token in self.variables or token.isalpha():
                if token in self.functions:
                    stack.append(token)  # Functions go to stack
                else:
                    output.append(token)  # Variables go to output
            # Left parenthesis goes to stack
            elif token == '(':
                stack.append(token)
            # Right parenthesis: pop until matching left parenthesis
            elif token == ')':
                while stack and stack[-1] != '(':
                    output.append(stack.pop())
                stack.pop()  # Remove '('
                # If function is on top, pop it to output
                if stack and stack[-1] in self.functions:
                    output.append(stack.pop())
            # If token is an operator
            elif token in self.precedence:
                # Pop operators with higher or equal precedence (considering associativity)
                while (stack and stack[-1] in self.precedence and
                       (self.precedence[stack[-1]] > self.precedence[token] or
                        (self.precedence[stack[-1]] == self.precedence[token] and token not in self.right_assoc))):
                    output.append(stack.pop())
                stack.append(token)
        # Pop remaining operators from stack
        while stack:
            output.append(stack.pop())
        return output
    
    def evaluate_postfix(self, postfix):
        """
        Postfix Evaluation Component (Stack-based Evaluation):
        Evaluates postfix expression using a stack.
        
        Algorithm:
        1. Create an empty stack
        2. For each token in postfix expression:
           - If NUMBER: convert to float and push to stack
           - If VARIABLE: get value from variables dict and push to stack
           - If FUNCTION: pop operand, apply function, push result
           - If OPERATOR: pop two operands, apply operation, push result
        3. Final result is the only element left in stack
        
        Example: ['3', '4', '2', '*', '+'] → 3 + (4 * 2) = 11
        
        Stack operations:
        - Push 3 → [3]
        - Push 4 → [3, 4]
        - Push 2 → [3, 4, 2]
        - Pop 2,4, multiply, push 8 → [3, 8]
        - Pop 8,3, add, push 11 → [11]
        """
        stack = []
        for token in postfix:
            # If token is a number, push to stack
            if re.match(r'\d+\.?\d*', token):
                stack.append(float(token))
            # If token is a variable, push its value to stack
            elif token in self.variables:
                stack.append(self.variables[token])
            # If token is a function, pop operand, apply function, push result
            elif token in self.functions:
                stack.append(self.functions[token](stack.pop()))
            # If token is an operator, pop two operands, compute, push result
            elif token in self.precedence:
                b, a = stack.pop(), stack.pop()  # Note: order matters (a op b)
                if token == '+': stack.append(a + b)
                elif token == '-': stack.append(a - b)
                elif token == '*': stack.append(a * b)
                elif token == '/': stack.append(a / b)
                elif token == '^': stack.append(a ** b)
        return stack[0]
    
    def evaluate(self, expr):
        """
        Main Evaluation Pipeline:
        Orchestrates the complete evaluation process.
        
        Flow:
        1. Tokenize: Break expression into tokens
        2. Convert: Transform infix to postfix notation
        3. Evaluate: Compute the result from postfix expression
        
        Example: "3 + 4 * 2"
        → Tokenize: ['3', '+', '4', '*', '2']
        → Postfix: ['3', '4', '2', '*', '+']
        → Evaluate: 11.0
        """
        tokens = self.tokenize(expr)
        postfix = self.infix_to_postfix(tokens)
        return self.evaluate_postfix(postfix)

# Demo
if __name__ == "__main__":
    evaluator = ExpressionEvaluator()
    
    # Test cases
    print("Expression Evaluator Demo\n" + "="*40)
    
    # Basic arithmetic
    print(f"3 + 4 * 2 = {evaluator.evaluate('3 + 4 * 2')}")
    print(f"(3 + 4) * 2 = {evaluator.evaluate('(3 + 4) * 2')}")
    print(f"10 - 2 * 3 = {evaluator.evaluate('10 - 2 * 3')}")
    print(f"2 ^ 3 ^ 2 = {evaluator.evaluate('2 ^ 3 ^ 2')}")
    
    # With variables
    evaluator.variables = {'x': 5, 'y': 3}
    print(f"\nWith x=5, y=3:")
    print(f"x + y * 2 = {evaluator.evaluate('x + y * 2')}")
    print(f"(x + y) * 2 = {evaluator.evaluate('(x + y) * 2')}")
    
    # With functions
    evaluator.variables = {'x': 0}
    print(f"\nWith functions:")
    print(f"sin(0) + 2 = {evaluator.evaluate('sin(x) + 2')}")
    print(f"sqrt(16) * 2 = {evaluator.evaluate('sqrt(16) * 2')}")
    print(f"cos(0) + sin(0) = {evaluator.evaluate('cos(0) + sin(0)')}")
