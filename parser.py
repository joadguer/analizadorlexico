import ply.yacc as yacc
import datetime
from lex import lexer, tokens

# ============================================================
# CONFIGURACIÓN DEL LOG
# ============================================================

USUARIO = "CamilaMoran"

fecha = datetime.datetime.now().strftime("%d-%m-%Y-%Hh%M")
log_name = f"sintactico-{USUARIO}-{fecha}.txt"

log = open(log_name, "w", encoding="utf-8")

log.write("============================================================\n")
log.write("LOG DE ANÁLISIS SINTÁCTICO - AVANCE 2\n")
log.write("============================================================\n")
log.write(f"Usuario: {USUARIO}\n")
log.write(f"Fecha  : {fecha}\n")
log.write("============================================================\n\n")


# ============================================================
# INICIO DEL PARSER
# ============================================================

def p_programa(p):
    '''programa : instrucciones'''
    p[0] = p[1]


# ============================================================
# LISTA DE INSTRUCCIONES
# ============================================================

def p_instrucciones_lista(p):
    '''instrucciones : instrucciones instruccion'''
    p[0] = p[1] + [p[2]]

def p_instrucciones_simple(p):
    '''instrucciones : instruccion'''
    p[0] = [p[1]]


# ============================================================
# INSTRUCCIONES PRINCIPALES
# ============================================================

# IMPRESIÓN
def p_imprimir(p):
    '''instruccion : PUTS expresion'''
    print("PRINT:", p[2])
    p[0] = ("puts", p[2])


# INGRESO DE DATOS
def p_input(p):
    '''instruccion : GETS'''
    print("INPUT DETECTADO")
    p[0] = ("gets",)


# ASIGNACIÓN
def p_asignacion(p):
    '''instruccion : VARIABLE_LOCAL ASIGNACION expresion'''
    print("ASIGNACION:", p[1], p[3])
    p[0] = ("assign", p[1], p[3])


# ============================================================
# ESTRUCTURAS DE CONTROL - Camila Moran
# ============================================================

def p_if(p):
    '''instruccion : IF expresion instrucciones END'''
    print("IF detectado")
    p[0] = ("if", p[2], p[3])


def p_while(p):
    '''instruccion : WHILE expresion instrucciones END'''
    print("WHILE detectado")
    p[0] = ("while", p[2], p[3])


# ============================================================
# ESTRUCTURAS DE DATOS (LISTA SIMPLE) - Camila Morán
# ============================================================

def p_lista(p):
    '''expresion : LBRACKET elementos RBRACKET'''
    p[0] = ("list", p[2])


