"""
Day 18
"""
from abc import ABC, abstractmethod
from enum import Enum


class Term(ABC):
    @abstractmethod
    def calc(self) -> int:
        pass


class UnaryTerm(Term):
    def __init__(self, val: int):
        self.val = val

    def calc(self) -> int:
        return self.val

    def __str__(self) -> str:
        return str(self.val)


ADD = "+"
MUL = "*"


class BinaryTerm(Term):
    def __init__(self, lhs: Term, rhs: Term, ops: str): 
        self.lhs = lhs
        self.rhs = rhs
        self.ops = ops

    def calc(self) -> int:
        if self.ops == ADD:
            return self.lhs.calc() + self.rhs.calc()
        elif self.ops == MUL:
            return self.lhs.calc() * self.rhs.calc()
        else:
            raise ValueError("Illegal binary operation!")

    def __str__(self) -> str:
        ops = '+' if self.ops == ADD else '*'
        return f'{self.lhs.__str__()} {ops} {self.rhs.__str__()}'


def parse_term(term_str: str) -> Term:
    """
    Assumption: numbers are only between 0 and 9
    """
    term_list = term_str.split(' ')
    stack = []
    ops = []

    for curr in term_list:
        # Check whether the curr is an operator
        if curr == '+':
            ops.append(ADD)
            continue
        elif curr == '*':
            ops.append(MUL)
            continue

        # Create the unary term
        curr_str = curr
        while curr_str[0] == '(':
            curr_str = curr_str[1:]
        while curr_str[-1] == ')':
            curr_str = curr_str[:-1]
        
        unary = UnaryTerm(int(curr_str))

        # Now, we must decide where to add the unary term
        if len(stack) == 0 and curr[0] != '(':
            stack.append(unary)
        elif curr[0] == '(':
            # We need to open up new sub-terms
            i = 0
            while i < len(curr) and curr[i] == '(':
                stack.append(None)
                i += 1
            # The last one will be the unary
            stack[-1] = unary
        elif curr[-1] == ')':
            # We first add the unary to the last one and then, we start combining sub-terms
            stack[-1] = BinaryTerm(stack[-1], unary, ops[-1])
            ops.pop()
            i = 1
            while i <= len(curr) and curr[-i] == ')' and len(stack) > 1:
                if stack[-2] is None:
                    stack[-2] = stack[-1]
                else:
                    stack[-2] = BinaryTerm(stack[-2], stack[-1], ops[-1])
                    ops.pop()
                stack.pop()
                i += 1
        else:
            # Combine the last and the current
            stack[-1] = BinaryTerm(stack[-1], unary, ops[-1])
            ops.pop()

    assert len(stack) == 1
    return stack[0]


def parse_term_sequence_without_parentheses(term_list: list, start: int, end: int) -> Term:
    stack = []
    ops = []

    for i in range(start, end + 1):
        curr = term_list[i]
        
        # Check whether the curr is an operator
        if isinstance(curr, str):
            ops.append(curr)
            continue

        if len(stack) == 0:
            stack.append(curr)
        elif ops[-1] == ADD:
            # Combine the last and the current
            stack[-1] = BinaryTerm(stack[-1], curr, ops[-1])
            ops.pop()
        else:
             # Last ops is *
             stack.append(curr)

    while len(ops) > 0:
        stack[-2] = BinaryTerm(stack[-2], stack[-1], ops[-1])
        ops.pop()
        stack.pop()

    assert len(stack) == 1
    return stack[0]


def parse_term_problem2(term_str: str) -> Term:
    term_list = term_str.split(' ')

    # Split up the parentheses
    nested_parentheses = 0
    fine_grained_term_list = []
    for term in term_list:
        if term == '+':
            fine_grained_term_list.append(ADD)
        elif term == '*':
            fine_grained_term_list.append(MUL)
        elif term[0] != '(' and term[-1] != ')':
            fine_grained_term_list.append(UnaryTerm(int(term)))
        else:
            for c in term:
                if c == '(':
                    nested_parentheses += 1
                if c != '(' and c != ')':
                    fine_grained_term_list.append(UnaryTerm(int(c)))
                else:
                    fine_grained_term_list.append(c)

    term_list = fine_grained_term_list

    stack = []
    i = 0
    while nested_parentheses > 0:
        if term_list[i] == ')':
            temp = parse_term_sequence_without_parentheses(term_list, stack[-1] + 1, i - 1)
            term_list = term_list[:stack[-1]] + [temp] + term_list[i + 1:]
            stack.pop()
            i = stack[-1] + 1 if len(stack) > 0 else 0
            nested_parentheses -= 1
            continue
        elif term_list[i] == '(':
            stack.append(i)
        i += 1

    return parse_term_sequence_without_parentheses(term_list, 0, len(term_list) - 1)


def read_input(path: str, parse=parse_term) -> list:
    read_terms = []

    with open(path, "r") as file_handle:
        line = file_handle.readline()
        while line != '':
            line = line[:-1] if line[-1] == '\n' else line
            read_terms.append(parse(line))
            line = file_handle.readline()

    return read_terms


def solve(terms: list) -> int:
    out = 0
    for term in terms:
        out += term.calc()
    return out


if __name__ == "__main__":
    # Problem 1
    # input_terms = read_input('/Users/danielgrittner/development/advent-of-code2020/day18/input.txt')
    # Problem 2
    input_terms = read_input('/Users/danielgrittner/development/advent-of-code2020/day18/input.txt', parse=parse_term_problem2)
    print(solve(input_terms))
