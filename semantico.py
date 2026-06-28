import os
import datetime
from parser import analizar

# ============================================================
# CONFIGURACIÓN DEL DESARROLLADOR
# ============================================================
DESARROLLADOR = "CamilaMoran"

fecha = datetime.datetime.now().strftime("%d%m%Y-%Hh%M")
nombre_log = f"semantico-{DESARROLLADOR}-{fecha}.txt"

log = open(nombre_log, "w", encoding="utf-8")

log.write("============================================================\n")
log.write("LOG DE ANÁLISIS SEMÁNTICO - AVANCE 3\n")
log.write("============================================================\n")
log.write(f"Desarrollador: {DESARROLLADOR}\n")
log.write(f"Fecha        : {fecha}\n")
log.write("============================================================\n\n")

# ============================================================
# TABLA DE SÍMBOLOS
# ============================================================
class SymbolTable:
    def __init__(self):
        self.symbols = {}
        self.functions = {}

    def declare_var(self, name, vtype="unknown"):
        self.symbols[name] = vtype

    def is_declared(self, name):
        return name in self.symbols

    def declare_function(self, name, params):
        self.functions[name] = params

    def get_function(self, name):
        return self.functions.get(name, None)


# ============================================================
# ANALIZADOR SEMÁNTICO
# ============================================================
class SemanticAnalyzer:
    def __init__(self):
        self.table = SymbolTable()
        self.errors = []

    def error(self, msg):
        self.errors.append(msg)
        log.write("ERROR SEMÁNTICO: " + msg + "\n")

    # --------------------------------------------------------
    # REGLA 1: variables deben declararse antes de uso
    # --------------------------------------------------------
    def check_variable(self, name):
        if not self.table.is_declared(name):
            self.error(f"Variable '{name}' no declarada")

    # --------------------------------------------------------
    # REGLA 2: asignación de variables
    # --------------------------------------------------------
    def assign(self, name):
        self.table.declare_var(name)

    # --------------------------------------------------------
    # REGLA 3: funciones y parámetros
    # --------------------------------------------------------
    def define_function(self, name, params):
        self.table.declare_function(name, params)

    def call_function(self, name, args):
        expected = self.table.get_function(name)
        if expected is None:
            self.error(f"Función '{name}' no definida")
        elif len(expected) != len(args):
            self.error(
                f"Función '{name}' esperaba {len(expected)} args y recibió {len(args)}"
            )

    # --------------------------------------------------------
    # REGLA 4: return dentro de función (simple control)
    # --------------------------------------------------------
    def check_return(self, inside_function):
        if not inside_function:
            self.error("RETURN fuera de función")


# ============================================================
# RECORRIDO DEL AST
# ============================================================
class SemanticRunner:
    def __init__(self):
        self.sem = SemanticAnalyzer()
        self.inside_function = False

    def run(self, ast):
        if ast is None:
            return

        for node in ast:
            self.visit(node)

        log.write("\n============================================================\n")
        log.write("RESUMEN\n")
        log.write(f"Errores semánticos encontrados: {len(self.sem.errors)}\n")

    # --------------------------------------------------------
    def visit(self, node):
        if not isinstance(node, tuple):
            return

        op = node[0]

        # PRINT
        if op == "print":
            self.eval_expr(node[1])

        # ASIGNACIÓN LOCAL
        elif op == "asignacion_local":
            _, _, name, expr = node
            self.sem.assign(name)
            self.eval_expr(expr)

        # VARIABLE USO
        elif op == "var":
            self.sem.check_variable(node[1])

        # IF / WHILE
        elif op in ("if", "if_else", "if_elsif_else", "while"):
            for x in node[2:]:
                self.visit_block(x)

        # FUNCTION
        elif op == "function":
            _, name, body = node
            self.inside_function = True
            self.sem.define_function(name, [])
            self.visit_block(body)
            self.inside_function = False

        elif op == "function_params":
            _, name, params, body = node
            self.inside_function = True
            self.sem.define_function(name, params)
            self.visit_block(body)
            self.inside_function = False

        # CALL FUNCTION
        elif op == "call_function":
            _, name, args = node
            self.sem.call_function(name, args)

        # RETURN
        elif op == "return":
            self.sem.check_return(self.inside_function)
            self.eval_expr(node[1])

        # LIST / HASH
        elif op in ("list", "hash"):
            for x in node[1]:
                self.eval_expr(x)

    # --------------------------------------------------------
    def visit_block(self, block):
        if isinstance(block, list):
            for b in block:
                self.visit(b)
        else:
            self.visit(block)

    # --------------------------------------------------------
    def eval_expr(self, expr):
        if not isinstance(expr, tuple):
            return expr

        op = expr[0]

        if op == "arith":
            self.eval_expr(expr[2])
            self.eval_expr(expr[3])

        elif op == "logic" or op == "rel":
            self.eval_expr(expr[2])
            self.eval_expr(expr[3])

        elif op == "call_function_expr":
            _, name, args = expr
            self.sem.call_function(name, args)

        elif op == "var":
            self.sem.check_variable(expr[1])


# ============================================================
# EJECUCIÓN PRINCIPAL
# ============================================================
if __name__ == "__main__":

    archivo = "algoritmo_camila.rb"

    if not os.path.exists(archivo):
        print("Archivo no encontrado")
        exit()

    with open(archivo, "r", encoding="utf-8") as f:
        codigo = f.read()

    print("Analizando semánticamente...")

    ast = analizar(codigo)

    runner = SemanticRunner()
    runner.run(ast)

    log.close()

    print(f"Log generado: {nombre_log}")