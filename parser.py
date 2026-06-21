import ply.yacc as yacc
import datetime
from lex import lexer, tokens

# ============================================================
# CONFIGURACIÓN DEL LOG
# ============================================================

USUARIO = "JosueGuerrero"

# Formato exigido: sintactico-usuarioGit-fecha-hora.txt
fecha = datetime.datetime.now().strftime("%d%m%Y-%Hh%M")
log_name = f"sintactico-{USUARIO}-{fecha}.txt"

log = open(log_name, "w", encoding="utf-8")

log.write("============================================================\n")
log.write("LOG DE ANÁLISIS SINTÁCTICO - AVANCE 2\n")
log.write("============================================================\n")
log.write(f"Usuario: {USUARIO}\n")
log.write(f"Fecha  : {fecha}\n")
log.write("============================================================\n\n")

# ============================================================
# PRECEDENCIA DE OPERADORES (Josue)
# ============================================================
precedence = (
    ('left', 'MAS', 'MENOS'), # Nivel 1: Menor prioridad (se ejecuta al final)
    ('left', 'PRODUCTO', 'DIVISION'), # Nivel 2: Mayor prioridad (se ejecuta primero)
)

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
# IMPRESIÓN E INGRESO DE DATOS
# ============================================================

def p_print(p):
    'instruccion : PUTS expresion'
    p[0] = ("print", p[2])

def p_input(p):    
    'instruccion : VARIABLE_LOCAL ASIGNACION GETS'    
    p[0] = ("input", p[1])

# ============================================================
# ASIGNACIÓN DE VARIABLES (Josue)
# ============================================================

def p_asignacion_local(p):
    'instruccion : VARIABLE_LOCAL ASIGNACION expresion'
    p[0] = ("asignacion_local", p[1], p[3])

def p_asignacion_instancia(p):
    'instruccion : VARIABLE_INSTANCIA ASIGNACION expresion'
    p[0] = ("asignacion_instancia", p[1], p[3])

def p_asignacion_constante(p):
    'instruccion : CONSTANTE ASIGNACION expresion'
    p[0] = ("asignacion_constante", p[1], p[3])

# ============================================================
# EXPRESIONES ARITMÉTICAS (Josue)
# ============================================================

def p_expr_arit(p):
    '''expresion : expresion MAS expresion
                 | expresion MENOS expresion
                 | expresion PRODUCTO expresion
                 | expresion DIVISION expresion'''
    p[0] = ("arith", p[2], p[1], p[3])

def p_expr_agrupada(p):
    'expresion : LPAREN expresion RPAREN'
    p[0] = p[2]

def p_expr_termino(p):
    '''expresion : ENTERO
                 | FLOTANTE
                 | CADENA
                 | TRUE
                 | FALSE
                 | VARIABLE_LOCAL
                 | VARIABLE_INSTANCIA
                 | CONSTANTE'''
    p[0] = p[1]

# ============================================================
# EXPRESIONES LÓGICAS (Camila Morán)
# ============================================================

def p_expr_logica(p):
    '''expresion : expresion AND expresion
                 | expresion OR expresion'''
    p[0] = ("logic", p[2], p[1], p[3])

def p_expr_relacional(p):
    '''expresion : expresion MAYOR expresion
                 | expresion MENOR expresion
                 | expresion MAYORIGUAL expresion
                 | expresion MENORIGUAL expresion
                 | expresion IGUALDAD expresion
                 | expresion DIFERENTE expresion'''
    p[0] = ("rel", p[2], p[1], p[3])

# ============================================================
# ESTRUCTURAS DE DATOS (Josue: Hash / Camila: Lista)
# ============================================================

def p_lista(p):
    'expresion : LBRACKET elementos RBRACKET'
    p[0] = ("list", p[2])

def p_elementos_lista(p):
    '''elementos : elementos COMA expresion
                 | expresion'''
    if len(p) == 4:
        p[0] = p[1] + [p[3]]
    else:
        p[0] = [p[1]]

def p_hash(p):
    'expresion : LBRACE lista_pares RBRACE'
    p[0] = ("hash", p[2])

def p_lista_pares(p):
    '''lista_pares : lista_pares COMA par
                   | par'''
    if len(p) == 4:
        p[0] = p[1] + [p[3]]
    else:
        p[0] = [p[1]]

# Nota: Asume que => puede estar definido como una asignación o tokens separados en tu lexer.
def p_par(p):
    'par : expresion ASIGNACION MAYOR expresion' 
    p[0] = ("par", p[1], p[4])

# ============================================================
# ESTRUCTURAS DE CONTROL (Josue: if/else / Camila: if/while)
# ============================================================

def p_if(p):
    'instruccion : IF expresion instrucciones END'
    p[0] = ("if", p[2], p[3])

def p_if_else(p):
    'instruccion : IF expresion instrucciones ELSE instrucciones END'
    p[0] = ("if_else", p[2], p[3], p[5])

def p_while(p):
    'instruccion : WHILE expresion instrucciones END'
    p[0] = ("while", p[2], p[3])

# ============================================================
# FUNCIONES (Josue: Función con params y Llamada / Camila: Función simple)
# ============================================================

def p_function_simple(p):
    'instruccion : DEF VARIABLE_LOCAL instrucciones END'
    p[0] = ("function", p[2], p[3])

def p_function_params(p):
    'instruccion : DEF VARIABLE_LOCAL LPAREN parametros RPAREN instrucciones END'
    p[0] = ("function_params", p[2], p[4], p[6])

def p_parametros(p):
    '''parametros : parametros COMA VARIABLE_LOCAL
                  | VARIABLE_LOCAL'''
    if len(p) == 4:
        p[0] = p[1] + [p[3]]
    else:
        p[0] = [p[1]]

def p_llamada_funcion_instruccion(p):
    'instruccion : VARIABLE_LOCAL LPAREN argumentos RPAREN'
    p[0] = ("call_function", p[1], p[3])

def p_llamada_funcion_expresion(p):
    'expresion : VARIABLE_LOCAL LPAREN argumentos RPAREN'
    p[0] = ("call_function_expr", p[1], p[3])

def p_argumentos(p):
    '''argumentos : argumentos COMA expresion
                  | expresion'''
    if len(p) == 4:
        p[0] = p[1] + [p[3]]
    else:
        p[0] = [p[1]]

def p_return(p):
    'instruccion : RETURN expresion'
    p[0] = ("return", p[2])

# ============================================================
# ERROR SINTÁCTICO (OBLIGATORIO)
# ============================================================

def p_error(p):
    if p:
        msg = f"ERROR SINTACTICO: Token inesperado '{p.value}' (tipo {p.type}) en la línea {p.lineno}\n"
    else:
        msg = "ERROR SINTACTICO: Fin de archivo inesperado\n"

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
    # Asegúrate de tener tu archivo .rb en el mismo directorio
    archivo = "algoritmo_josue.rb" 

    try:
        with open(archivo, "r", encoding="utf-8") as f:
            data = f.read()

        print("Analizando código...\n")
        resultado = analizar(data)

        print("\n=== AST GENERADO ===")
        print(resultado)

    except FileNotFoundError:
        print(f"Archivo '{archivo}' no encontrado. Verifica la ruta.")

    log.close()
    print(f"\nLog generado: {log_name}")