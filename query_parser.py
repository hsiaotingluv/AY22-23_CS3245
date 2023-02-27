class QueryParser:
    
    @classmethod
    def shunting_yard(cls, query):

        # Operator precedence dictionary
        precedence = {"(": 3, ")": 3, "NOT": 2, "AND": 1, "OR": 0}

        # Stack to hold operators and parentheses
        operator_stack = []
        # Output queue to hold the postfix notation
        output_queue = []

        # Tokenize the query string 
        tokens = query.split()
        
        # Loop through to separate parenthesis
        separated_tokens = []
        for token in tokens:
            if "(" in token:
                separated_tokens.append("(")
                separated_tokens.append(token.replace("(", ""))
            elif ")" in token:
                separated_tokens.append(token.replace(")", ""))
                separated_tokens.append(")")
            else:
                separated_tokens.append(token)

        # Join the separated tokens back into a string, then tokenize
        separated_query = " ".join(separated_tokens)
        tokens = separated_query.split()

        for token in tokens:

            if token in precedence:
                # If token is an operator or parenthesis
                if token == "(":
                    # Left parenthesis, push onto the operator stack
                    operator_stack.append(token)
                elif token == ")":
                    # Right parenthesis, pop operators from stack to output queue
                    while operator_stack[-1] != "(":
                        output_queue.append(operator_stack.pop())
                    
                    # Discard the left parenthesis
                    operator_stack.pop()
                else: 
                    # Token is an operator
                    while operator_stack and operator_stack[-1] != "(" and precedence[token] <= precedence[operator_stack[-1]] and precedence[token] != "NOT":
                        output_queue.append(operator_stack.pop())
                    operator_stack.append(token)

            else: 
                # Token is an operand, push onto output queue
                output_queue.append(token)

        # Pop remaining operators from stack to output queue
        while operator_stack:
            output_queue.append(operator_stack.pop())

        # Return the postfix notation as a string
        return " ".join(output_queue)

    @classmethod
    def evaluatePostfix(cls, postfix_expression):
        
        # Create an empty stack for operands 
        postings_stack = []

        # Tokenize the postfix expression
        tokens = postfix_expression.split()

        # Loop over the tokens in the expression
        for token in tokens:

            if token == "AND":
                postings1 = postings_stack.pop()
                postings2 = postings_stack.pop()
                result = operand1 

            elif token == "OR":

            elif token == "NOT":

            else: 
                # Token is an operand, append to stack
                postings_stack.append(result)

query = "term1 AND term2 OR (term3 AND NOT term4)"
postfix_notation = QueryParser.shunting_yard(query)  
print(postfix_notation)


    