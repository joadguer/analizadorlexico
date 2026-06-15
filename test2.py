import os
from datetime import datetime
from lex import lexer

# ============================================================
# CONFIGURACIÓN DEL DESARROLLADOR
# ============================================================
DESARROLLADOR = "CamilaMoran"

# ============================================================
# ARCHIVO DE PRUEBA
# ============================================================
archivo_prueba = "algoritmo_camila.rb"

if not os.path.exists(archivo_prueba):
    print(f"Error: No se encuentra el archivo {archivo_prueba}")
    exit()

with open(archivo_prueba, "r", encoding="utf-8") as f:
    codigo_ruby = f.read()

# ============================================================
# CONFIGURAR NOMBRE DEL LOG
# ============================================================
fecha_hora_actual = datetime.now().strftime("%d-%m-%Y-%Hh%M")

nombre_log = f"lexico-{DESARROLLADOR}-{fecha_hora_actual}.txt"

# ============================================================
# EJECUTAR ANÁLISIS LÉXICO
# ============================================================
print(f"Iniciando análisis léxico de: {archivo_prueba}...")

lexer.lineno = 1
lexer.input(codigo_ruby)

# ============================================================
# GENERAR LOG
# ============================================================
with open(nombre_log, "w", encoding="utf-8") as log:

    log.write("============================================================\n")
    log.write("LOG DE ANÁLISIS LÉXICO - AVANCE 1\n")
    log.write("============================================================\n")
    log.write(f"Desarrollador : {DESARROLLADOR}\n")
    log.write(f"Fecha y Hora  : {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
    log.write(f"Archivo Test  : {archivo_prueba}\n")
    log.write("============================================================\n\n")

    log.write(
        f"{'TIPO TOKEN':<25}"
        f"{'VALOR':<30}"
        f"{'LÍNEA':<10}"
        f"{'POSICIÓN':<10}\n"
    )

    log.write("-" * 80 + "\n")

    while True:

        tok = lexer.token()

        if not tok:
            break

        log.write(
            f"{tok.type:<25}"
            f"{str(tok.value):<30}"
            f"{tok.lineno:<10}"
            f"{tok.lexpos:<10}\n"
        )

print("¡Análisis completado con éxito!")
print(f"Archivo de log generado: {nombre_log}")