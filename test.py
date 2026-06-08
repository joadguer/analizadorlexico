import os
from datetime import datetime
from lex import lexer  

# =======# =====================================================
# CONFIGURACIÓN DEL DESARROLLADOR
# ============================================================
DESARROLLADOR = "josueguerrero"  

# ============================================================
# 1. LEER EL ARCHIVO DE PRUEBA (.rb)
# ============================================================
archivo_prueba = "algoritmo_ruby.rb"

if not os.path.exists(archivo_prueba):
    print(f"Error: No se encuentra el archivo {archivo_prueba}")
    exit()

with open(archivo_prueba, "r", encoding="utf-8") as f:
    codigo_ruby = f.read()

# ============================================================
# 2. CONFIGURAR EL NOMBRE DEL LOG (Formato requerido)
# ============================================================
# Formato: lexico-desarrollador-DD-MM-YYYY-HH:MM.txt
fecha_hora_actual = datetime.now().strftime("%d-%m-%Y-%H_%M")
nombre_log = f"lexico-{DESARROLLADOR}-{fecha_hora_actual}.txt"

# ============================================================
# 3. EJECUTAR EL ANÁLISIS LÉXICO Y ESCRIBIR EL LOG
# ============================================================
print(f"Iniciando análisis léxico de: {archivo_prueba}...")
lexer.lineno = 1
lexer.input(codigo_ruby)

# Abrimos el archivo de log para ir escribiendo los resultados
with open(nombre_log, "w", encoding="utf-8") as log:
    # Encabezado del Log institucional
    log.write("============================================================\n")
    log.write(f"LOG DE ANÁLISIS LÉXICO - AVANCE 1\n")
    log.write("============================================================\n")
    log.write(f"Desarrollador : {DESARROLLADOR}\n")
    log.write(f"Fecha y Hora  : {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
    log.write(f"Archivo Test  : {archivo_prueba}\n")
    log.write("============================================================\n\n")
    log.write(f"{'TIPO TOKEN':<25}{'VALOR':<30}{'LÍNEA':<10}{'POSICIÓN':<10}\n")
    log.write("-" * 75 + "\n")

    # Ciclo de extracción de tokens
    while True:
        tok = lexer.token()
        if not tok:
            break  # Fin del archivo
        
        # Escribir cada token formateado en columnas legibles
        log.write(f"{tok.type:<25}{str(tok.value):<30}{tok.lineno:<10}{tok.lexpos:<10}\n")

print(f"¡Análisis completado con éxito!")
print(f"Archivo de log generado: {nombre_log}")