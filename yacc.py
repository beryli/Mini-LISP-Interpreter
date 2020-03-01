from lex import tokens
import numpy as np 
import math
from itertools import chain 
from functools import reduce
names = { }

def eval (var, body):
    # print(var)
    # print(body)
    for idx, val in enumerate(body):
        if val in var:
            body = [sub.replace(val, str(var[val])) for sub in body]
    # assignment
    body = "ret " + ' '.join(body)
    value = yacc.parse(body)
    return value


def p_statement_expr(p):
    'statement : expression'

# ---------------- 8 named function
def p_statement_defFunc(p):
    'statement : LPAREN Def ID LPAREN Lambda para var RPAREN RPAREN'
    if len(p[6]) == 0:
        names[p[3]] = p[7]
    else:
        names[p[3]] = [[], []]
        names[p[3]][0] = p[6]
        names[p[3]][1] = p[7]

def p_expression_defFunc(p):
    '''expression   : LPAREN ID para RPAREN
                    | LPAREN ID items RPAREN'''
    for idx, val in enumerate(p[3]):
        if not isinstance(val, int) and (not val == '#f' and not val == '#t'):
            p[3][idx] = names[val]
    # print(names[p[2]][0], names[p[2]][1])
    local = dict(zip(names[p[2]][0], p[3]))
    body = np.hstack(np.array(names[p[2]][1]))
    # print(local)
    # print(body)
    p[0] = eval(local, body)
# ---------------- 8 named function

# ---------------- 7 lambda
# ---------------- 7 lambda lambda_call shold be expression
def p_ret(p):
    'statement : RET expression'
    p[0] = p[2]

def p_expression_lambda(p):
    'expression : LPAREN LPAREN Lambda para var RPAREN items RPAREN'
    for idx, val in enumerate(p[7]):
        if not isinstance(val, int):
            p[7][idx] = names[val]
    # print(p[4])
    # print(list(chain.from_iterable(p[5])))
    # print(p[7])
    local = dict(zip(p[4], p[7]))
    # body = list(chain.from_iterable(p[5]))
    body = np.hstack(np.array(p[5]))
    p[0] = eval(local, body)
    # print(local)
    # print(body)

# ---------------- 7 lambda body
def p_var_if(p):
    'var : LPAREN IF var var var RPAREN'
    p[0] = np.hstack(np.array(p[1:]))

def p_var_boolop(p):
    '''var  : LPAREN And var_and RPAREN
            | LPAREN Or var_or RPAREN
            | LPAREN Equal var_equ RPAREN
            | LPAREN Not var RPAREN
            | LPAREN Greater var var RPAREN
            | LPAREN Smaller var var RPAREN'''
    p[0] = np.hstack(np.array(p[1:]))

def p_var_equ(p):
    '''var_equ    : var_equ var
                  | var var'''
    p[0] = np.hstack(np.array(p[1:]))

def p_var_and(p):
    '''var_and    : var_and var
                  | var var'''
    p[0] = np.hstack(np.array(p[1:]))

def p_var_or(p):
    '''var_or     : var_or var
                  | var var'''
    p[0] = np.hstack(np.array(p[1:]))

def p_var_binop(p):
    '''var  : LPAREN PLUS var_add RPAREN
            | LPAREN MINUS var var RPAREN
            | LPAREN Multiply var_mul RPAREN
            | LPAREN DIVIDE var var RPAREN
            | LPAREN Modulus var var RPAREN'''
    p[0] = np.hstack(np.array(p[1:]))
    # print(p[0])

def p_var_multiply(p):
    '''var_mul    : var_mul var
                  | var var'''
    p[0] = np.hstack(np.array(p[1:]))

def p_var_add(p):
    '''var_add    : var_add var
                  | var var'''
    p[0] = np.hstack(np.array(p[1:]))

def p_var(p):
    '''var  : ID
            | NUMBER
            | Boolean'''
    if isinstance(p[1], bool) :
    	if p[1] : p[0] = "#t"
    	else    : p[0] = "#f"
    else : p[0] = p[1]

# ---------------- 7 lambda body

# ---------------- 7 lambda parameters
def p_para(p):
    'para : LPAREN items RPAREN'
    p[0] = p[2]

def p_items(p):
    'items : item items'
    p[0] = [p[1]] + p[2]

def p_items_empty(p):
    'items : empty'
    p[0] = []

def p_empty(p):
    'empty :'
    pass

def p_item_atom(p):
    '''item : ID
            | NUMBER
            | Boolean'''
    p[0] = p[1]
# ---------------- 7 lambda parameters
# ---------------- 7 lambda

# ---------------- 5,6 if define
def p_statement_def(p):
    'statement : LPAREN Def ID expression RPAREN'
    names[p[3]] = p[4]

def p_expression_if(p):
    'expression : LPAREN IF expression expression expression RPAREN'
    if isinstance(p[3], bool) :
    	if p[3] : p[0] = p[4]
    	else    : p[0] = p[5]
    else : print("Type error!")
# ---------------- 5,6 if define
# ---------------- 5 if

# ---------------- 4 Logical Operations
def p_expression_boolop1(p):
    'expression : LPAREN Not expression RPAREN'
    if isinstance(p[3], bool) :
    	p[0] = not p[3]
    else : print("Type error!")

def p_expression_boolop2(p):
    '''expression : LPAREN Greater expression expression RPAREN
                  | LPAREN Smaller expression expression RPAREN'''
    if not isinstance(p[3], bool) and not isinstance(p[4], bool):
    	if   p[2] == '>' :  p[0] = p[3] > p[4]
    	elif p[2] == '<' :  p[0] = p[3] < p[4]
    else : print("Type error!")

def p_expression_boolop3(p):
    '''expression : LPAREN And exp_and RPAREN
                  | LPAREN Or exp_or RPAREN
                  | LPAREN Equal exp_equ RPAREN'''
    if   p[2] == 'and': p[0] = p[3]
    elif p[2] == 'or' : p[0] = p[3]
    elif p[2] == '='  : p[0] = p[3]

def p_expression_equ(p):
    '''exp_equ    : exp_equ expression
                  | expression expression'''
    if type(p[1]) == type(p[2]):
	    if p[1] == p[2]: p[0] = True
	    else : p[0] = False
    else : print("Type error!")

def p_expression_and(p):
    '''exp_and    : exp_and expression
                  | expression expression'''
    if isinstance(p[1], bool) and isinstance(p[2], bool):
    	p[0] = p[1] and p[2]
    else : print("Type error!")

def p_expression_or(p):
    '''exp_or     : exp_or expression
                  | expression expression'''
    if isinstance(p[1], bool) and isinstance(p[2], bool):
    	p[0] = p[1] or p[2]
    else : print("Type error!")
# ---------------- 4 Logical Operations

# ---------------- 3 Numerical Operations
def p_expression_binop1(p):
    '''expression : LPAREN MINUS expression expression RPAREN
                  | LPAREN DIVIDE expression expression RPAREN
                  | LPAREN Modulus expression expression RPAREN'''
    if not isinstance(p[3], bool) and not isinstance(p[4], bool):
	    if   p[2] == '-': p[0] = p[3] - p[4]
	    elif p[2] == '/': p[0] = math.floor(p[3] / p[4])
	    elif p[2] == 'mod': p[0] = p[3] % p[4]
    else : print("Type error!")

def p_expression_binop2(p):
    '''expression : LPAREN PLUS exp_add RPAREN
                  | LPAREN Multiply exp_mul RPAREN'''
    if   p[2] == '+': p[0] = p[3]
    elif p[2] == '*': p[0] = p[3]
    # print(vars(p), p[0])

def p_expression_multiply(p):
    '''exp_mul    : exp_mul expression
                  | expression expression'''
    if not isinstance(p[1], bool) and not isinstance(p[2], bool):
        p[0] = p[1] * p[2]
    else : print("Type error!")

def p_expression_add(p):
    '''exp_add    : exp_add expression
                  | expression expression'''
    if not isinstance(p[1], bool) and not isinstance(p[2], bool):
    	p[0] = p[1] + p[2]
    else : print("Type error!")
# ---------------- 3 Numerical Operations

# ---------------- 2 print
def p_statement_PB(p):
    'statement : LPAREN PB expression RPAREN'
    if p[3] is not None:
        if isinstance(p[3], bool) :
            if p[3] : print("#t")
            else    : print("#f")
        else : print("Type error!")

def p_statement_PN(p):
    '''statement : LPAREN PN expression RPAREN
                 | LPAREN PN expression'''
    if p[3] is not None:
        if not isinstance(p[3], bool) : print(p[3])
        else : print("Type error!")
# ---------------- 2 print

# ---------------- 0 expression
def p_expression_bool(p):
    'expression : Boolean'
    if p[1] == '#t' : p[0] = True
    else : p[0] = False

def p_expression_number(p):
    'expression : NUMBER'
    p[0] = p[1]

def p_expression_name(p):
    'expression : ID'
    try:
        p[0] = names[p[1]]
    except LookupError:
        print("Undefined name '%s'" % p[1])
        p[0] = 0
# ---------------- 0 expression

def p_error(p):
  if p is not None:
    print("Syntax error at '%s'" % p)
    # print("Syntax error at '%s'" % p.value)


import ply.yacc as yacc
yacc.yacc()

while True:
    try:
        s = input()   # use input() on Python 3
        # s = input('input > ')   # use input() on Python 3
    except EOFError:
        break
    yacc.parse(s)
