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
# REGLA INICIAL
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
# IMPRESIÓN
# ============================================================

def p_print(p):
    'instruccion : PUTS expresion'
    p[0] = ("print", p[2])


# ============================================================
# INGRESO DE DATOS
# ============================================================

def p_input(p):
    'instruccion : GETS'
    p[0] = ("input",)


# ============================================================
# ASIGNACIÓN
# ============================================================

def p_asignacion(p):
    'instruccion : VARIABLE_LOCAL ASIGNACION expresion'
    p[0] = ("assign", p[1], p[3])


# ============================================================
# EXPRESIONES ARITMÉTICAS
# ============================================================

def p_expr_arit(p):
    '''expresion : expresion MAS expresion
                 | expresion MENOS expresion
                 | expresion PRODUCTO expresion
                 | expresion DIVISION expresion
                 | expresion MODULO expresion'''
    p[0] = ("arith", p[2], p[1], p[3])


def p_expr_num(p):
    '''expresion : ENTERO
                 | FLOTANTE'''
    p[0] = p[1]


def p_expr_var(p):
    'expresion : VARIABLE_LOCAL'
    p[0] = ("var", p[1])


# ============================================================
# EXPRESIONES LÓGICAS - Camila Morán
# ============================================================

def p_expr_logica(p):
    '''expresion : expresion AND expresion
                 | expresion OR expresion'''
    p[0] = ("logic", p[2], p[1], p[3])


#def p_expr_relacional(p):
  #  '''expresion : expresion MAYOR expresion
    #             | expresion MENOR expresion
      #           | expresion MAYORIGUAL expresion
     #            | expresion MENORIGUAL expresion
     #            | expresion IGUALDAD expresion
     #            | expresion DIFERENTE expresion'''
    # p[0] = ("rel", p[2], p[1], p[3])


# ============================================================
# ESTRUCTURAS DE DATOS (LISTAS) - Camila Morán
# ============================================================

def p_lista(p):
    'expresion : LBRACKET elementos RBRACKET'
    p[0] = ("list", p[2])


# def p_elementos_lista(p):
   # 'elementos : elementos COMA expresion'
   # p[0] = p[1] + [p[3]]


#def p_elementos_simple(p):
 #   'elementos : expresion'
  #  p[0] = [p[1]]


# ============================================================
# ESTRUCTURAS DE CONTROL - Camila Morán
# ============================================================

def p_if(p):
    'instruccion : IF expresion instrucciones END'
    p[0] = ("if", p[2], p[3])


def p_while(p):
    'instruccion : WHILE expresion instrucciones END'
    p[0] = ("while", p[2], p[3])


# ============================================================
# FUNCIONES - Camila Morán
# ============================================================

def p_function(p):
    'instruccion : DEF VARIABLE_LOCAL instrucciones END'
    p[0] = ("function", p[2], p[3])


# ============================================================
# ERROR SINTÁCTICO (OBLIGATORIO)
# ============================================================

def p_error(p):
    if p:
        msg = f"ERROR SINTACTICO en token: {p.value} (tipo {p.type})\n"
    else:
        msg = "ERROR SINTACTICO: fin de archivo inesperado\n"

    print(msg)
    log.write(msg)


# ============================================================
# CONSTRUCCIÓN DEL PARSER
# ============================================================

parser = yacc.yacc()


# ============================================================
# FUNCIÓN PRINCIPAL
# ============================================================

def analizar(codigo):
    lexer.lineno = 1
    return parser.parse(codigo, lexer=lexer)


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    archivo = "algoritmo_camila.rb"

    try:
        with open(archivo, "r", encoding="utf-8") as f:
            data = f.read()

        print("Analizando código...\n")
        resultado = analizar(data)

        print("\n=== AST GENERADO ===")
        print(resultado)

    except FileNotFoundError:
        print("Archivo no encontrado")

    log.close()
    print(f"\nLog generado: {log_name}")