# ------------------------------------------------------------
# rubylex.py
# ------------------------------------------------------------

import ply.lex as lex

# ============================================================
# Palabras reservadas de Ruby
# ============================================================

reserved = {
    'if'     : 'IF',
    'else'   : 'ELSE',
    'while'  : 'WHILE',
    'for'    : 'FOR',
    'def'    : 'DEF',
    'return' : 'RETURN',
    'end'    : 'END',
    'puts'   : 'PUTS',
    'gets'   : 'GETS',
    'true'   : 'TRUE',
    'false'  : 'FALSE',
    'nil'    : 'NIL'
}

# ============================================================
# Lista de tokens
# ============================================================

tokens = (

    # Variables
    'VARIABLE_LOCAL',
    'VARIABLE_INSTANCIA',
    'CONSTANTE',

    # Tipos de datos
    'ENTERO',
    'FLOTANTE',
    'CADENA',

    # Operadores aritméticos
    'MAS',
    'MENOS',
    'PRODUCTO',
    'DIVISION',
    'MODULO',

    # Operadores relacionales
    'IGUALDAD',
    'DIFERENTE',
    'MAYOR',
    'MENOR',
    'MAYORIGUAL',
    'MENORIGUAL',

    # Operadores lógicos
    'AND',
    'OR',
    'NOT',

    # Operadores de asignación
    'ASIGNACION',
    'MASIGUAL',
    'MENOSIGUAL',
    'MULTIGUAL',
    'DIVIGUAL',

    # Delimitadores
    'LPAREN',
    'RPAREN',
    'LBRACKET',
    'RBRACKET',
    'LBRACE',
    'RBRACE',
    'COMA',
    'PUNTO',
    'DOSPUNTOS'

) + tuple(reserved.values())

# ============================================================
# Expresiones regulares para tokens simples
# ============================================================

# Asignación compuesta
t_MASIGUAL    = r'\+='
t_MENOSIGUAL  = r'-='
t_MULTIGUAL   = r'\*='
t_DIVIGUAL    = r'/='

# Relacionales
t_IGUALDAD    = r'=='
t_DIFERENTE   = r'!='
t_MAYORIGUAL  = r'>='
t_MENORIGUAL  = r'<='
t_MAYOR       = r'>'
t_MENOR       = r'<'

# Lógicos
t_AND         = r'&&'
t_OR          = r'\|\|'
t_NOT         = r'!'

# Asignación
t_ASIGNACION  = r'='

# Aritméticos
t_MAS         = r'\+'
t_MENOS       = r'-'
t_PRODUCTO    = r'\*'
t_DIVISION    = r'/'
t_MODULO      = r'%'

# Delimitadores
t_LPAREN      = r'\('
t_RPAREN      = r'\)'
t_LBRACKET    = r'\['
t_RBRACKET    = r'\]'
t_LBRACE      = r'\{'
t_RBRACE      = r'\}'
t_COMA        = r','
t_PUNTO       = r'\.'
t_DOSPUNTOS   = r':'

# ============================================================
# Reglas con acciones
# ============================================================

# Float
def t_FLOTANTE(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

# Integer
def t_ENTERO(t):
    r'\d+'
    t.value = int(t.value)
    return t

# String
def t_CADENA(t):
    r'\"([^\\\n]|(\\.))*?\"'
    return t

# Variables de instancia
def t_VARIABLE_INSTANCIA(t):
    r'@[a-zA-Z_][a-zA-Z0-9_]*'
    return t

# Constantes
def t_CONSTANTE(t):
    r'[A-Z][a-zA-Z0-9_]*'
    return t

# Variables locales y palabras reservadas
def t_VARIABLE_LOCAL(t):
    r'[a-z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'VARIABLE_LOCAL')
    return t

# ============================================================
# Comentarios
# ============================================================

def t_COMMENT(t):
    r'\#.*'
    pass

# ============================================================
# Saltos de línea
# ============================================================

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# ============================================================
# Ignorar espacios y tabs
# ============================================================

t_ignore = ' \t'

# ============================================================
# Manejo de errores
# ============================================================

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# ============================================================
# Construcción del lexer
# ============================================================

lexer = lex.lex()

# ============================================================
# Código Ruby de prueba
# ============================================================

# ============================================================
# Código Ruby de prueba
# ============================================================

# data = '''
# PI = 3.1416

# @contador = 0
# @@total = 100

# edad = 20
# nombre = "Camila"

# if edad >= 18 && edad <= 60
#     puts nombre
# else
#     puts "Menor de edad"
# end
# '''

# ============================================================
# TEST 1
# ============================================================

# print("----- TOKENS -----")

# lexer.lineno = 1
# lexer.input(data)

# while True:
#     tok = lexer.token()

#     if not tok:
#         break

#     print(tok)

# ============================================================
# TEST 2
# ============================================================

# print("\n----- ATRIBUTOS -----")

# lexer.lineno = 1
# lexer.input(data)

# while True:
#     tok = lexer.token()

#     if not tok:
#         break

#     print(tok.type, tok.value, tok.lineno, tok.lexpos)