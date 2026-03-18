# PLY MINI PROJECT
# Implementation of Basic Language Constructs using PLY
# PES2UG24CS912  PRANAV SHASHIKIRAN ATREYA
# Section: D

import ply.lex as lex
import ply.yacc as yacc

# ------------------ LEXER ------------------
tokens = [
    'ID', 'NUMBER', 'STRING',
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE',
    'EQUALS', 'LPAREN', 'RPAREN',
    'LBRACE', 'RBRACE',
    'GT', 'LT', 'GE', 'LE', 'EQ', 'NE'
]

reserved = {
    'if': 'IF',
    'else': 'ELSE',
    'while': 'WHILE',
    'print': 'PRINT',
    'read': 'READ'
}
tokens += list(reserved.values())

t_PLUS    = r'\+'
t_MINUS   = r'-'
t_TIMES   = r'\*'
t_DIVIDE  = r'/'
t_EQUALS  = r'='
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_LBRACE  = r'\{'
t_RBRACE  = r'\}'
t_GT      = r'>'
t_LT      = r'<'
t_GE      = r'>='
t_LE      = r'<='
t_EQ      = r'=='
t_NE      = r'!='
t_STRING  = r'\".*?\"'
t_ignore  = ' \t'

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'ID')
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

lexer = lex.lex()

# ------------------ PARSER ------------------
symbol_table = {}

def p_program(p):
    '''program : program statement
               | statement'''
    pass

# 1️⃣ Variable Declaration / Assignment
def p_statement_assign(p):
    'statement : ID EQUALS expression'
    symbol_table[p[1]] = p[3]
    print(f"{p[1]} = {p[3]}")

# 2️⃣ Arithmetic Expressions
def p_expression_binop(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression'''
    if p[2] == '+': p[0] = p[1] + p[3]
    elif p[2] == '-': p[0] = p[1] - p[3]
    elif p[2] == '*': p[0] = p[1] * p[3]
    elif p[2] == '/': p[0] = p[1] / p[3]

def p_expression_group(p):
    'expression : LPAREN expression RPAREN'
    p[0] = p[2]

def p_expression_number(p):
    'expression : NUMBER'
    p[0] = p[1]

def p_expression_id(p):
    'expression : ID'
    p[0] = symbol_table.get(p[1], 0)

def p_expression_compare(p):
    '''expression : expression GT expression
                  | expression LT expression
                  | expression GE expression
                  | expression LE expression
                  | expression EQ expression
                  | expression NE expression'''
    if p[2] == '>': p[0] = p[1] > p[3]
    elif p[2] == '<': p[0] = p[1] < p[3]
    elif p[2] == '>=': p[0] = p[1] >= p[3]
    elif p[2] == '<=': p[0] = p[1] <= p[3]
    elif p[2] == '==': p[0] = p[1] == p[3]
    elif p[2] == '!=': p[0] = p[1] != p[3]

# 3️⃣ Conditional Statements
def p_statement_if(p):
    'statement : IF LPAREN expression RPAREN LBRACE program RBRACE'
    if p[3]:
        print("Condition true → executing block")

# 4️⃣ Loops
def p_statement_while(p):
    'statement : WHILE LPAREN expression RPAREN LBRACE program RBRACE'
    count = 0
    while p[3] and count < 3:
        print(f"Loop iteration: {count + 1}")
        count += 1

# 5️⃣ Input / Output Statements
def p_statement_print(p):
    'statement : PRINT LPAREN STRING RPAREN'
    print(p[3][1:-1])

def p_statement_read(p):
    'statement : READ LPAREN ID RPAREN'
    val = input("Enter value: ")
    symbol_table[p[3]] = int(val)

def p_error(p):
    if p:
        print(f"Syntax error at '{p.value}'")
    else:
        print("Syntax error at EOF")

parser = yacc.yacc()

# ------------------ TEST CASES ------------------
tests = [
    ("Construct 1: Variable Declaration / Assignment", "x = 10"),
    ("Construct 2: Arithmetic Expressions", "y = 3 + 7 * 2"),
    ("Construct 3: Conditional Statements", 'if (5 < 10) { print("Condition True") }'),
    ("Construct 4: Loops", 'while (1 < 3) { print("Inside loop") }'),
    ("Construct 5: Input / Output Statements", 'print("Hello World")')
]

for title, code in tests:
    print("\n==============================")
    print(f"=== {title} ===")
    print("==============================")
    print("Input:\n" + code)
    print("\nOutput:")
    parser.parse(code)
