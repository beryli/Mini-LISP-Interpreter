reserved = {
   'lambda'     : 'Lambda',
   'define'     : 'Def',
   'print-num'  : 'PN',
   'print-bool' : 'PB',
   'if'  : 'IF',
   'and' : 'And',
   'or'  : 'Or',
   'not' : 'Not',
   'mod' : 'Modulus',
   'ret' : 'RET',
}
tokens = list(reserved.values())+[
  'Boolean','NUMBER',
  'PLUS','MINUS','DIVIDE','Multiply',
  'Greater','Smaller','Equal',
  'LPAREN','RPAREN', 'ID',
  ]
# Tokens

t_Boolean = r'\#[t|f]'
t_PLUS    = r'\+'
t_MINUS   = r'-'
t_Multiply= r'\*'
t_DIVIDE  = r'/'
t_Equal   = r'='
t_Greater = r'>'
t_Smaller = r'<'
t_LPAREN  = r'\('
t_RPAREN  = r'\)'

def t_NUMBER(t):
    r'[-]?\d+'
    t.value = int(t.value)
    return t

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9-]*'
    t.type = reserved.get(t.value,'ID')
    # Check for reserved words
    return t

# Ignored characters
t_ignore = " \t"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")
    # return t

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)
    exit()

# Build the lexer
import ply.lex as lex
lex.lex()


"""
lexer = lex.lex()
data = '''(if #f And) lambda (lambda)
123
	1
'''
lexer.input(data)
# Tokenize
for tok in lexer:
    print ((tok))
"""
# while True:
#     tok = lexer.token()
#     if not tok: break      # No more input
#     print (tok)

