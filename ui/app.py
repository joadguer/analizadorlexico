import os
from datetime import datetime
from flask import Flask, render_template, request

# Importamos los analizadores
from lex import lexer, errores_lexicos
from parser import analizar_web
from semantico import SemanticRunner

app = Flask(__name__)

# Configuración de carpetas
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOGS_DIR = os.path.join(BASE_DIR, 'logs')

# Asegurar que las carpetas de logs existan
for fase in ['lexico', 'sintactico', 'semantico']:
    os.makedirs(os.path.join(LOGS_DIR, fase), exist_ok=True)

def calcular_columna(codigo, token):
    ultimo_salto = codigo.rfind('\n', 0, token.lexpos)
    if ultimo_salto < 0:
        return token.lexpos + 1
    return token.lexpos - ultimo_salto

# Función recursiva para aplanar el AST y mostrarlo en la tabla HTML
def aplanar_ast(nodo, lista_salida):
    if isinstance(nodo, tuple):
        # El primer elemento es la regla (ej. 'asignacion_local')
        regla = str(nodo[0]).upper()
        # El resto son los componentes de la expresión
        expresion = str(nodo[1:])
        lista_salida.append({
            "regla": regla,
            "expresion": expresion,
            "estado": "✅ Correcto"
        })
        # Recorremos los hijos por si hay nodos anidados
        for hijo in nodo[1:]:
            aplanar_ast(hijo, lista_salida)
    elif isinstance(nodo, list):
        for hijo in nodo:
            aplanar_ast(hijo, lista_salida)

@app.route('/', methods=['GET', 'POST'])
def index():
    codigo_previo = ""
    tokens_lexico = []
    reglas_sintactico = []
    tabla_semantico = []
    stats = {"lineas": 0, "chars": 0, "tokens": 0, "estado": "Esperando código..."}

    if request.method == 'POST':
        if 'limpiar' in request.form:
            return render_template('index.html', codigo="", lexico=[], sintactico=[], semantico=[], stats=stats)

        codigo_previo = request.form.get('codigo', '')
        stats["chars"] = len(codigo_previo)
        stats["lineas"] = len(codigo_previo.splitlines()) if codigo_previo else 0
        
        if codigo_previo.strip():
            # ==========================================
            # 1. ANÁLISIS LÉXICO
            # ==========================================
            errores_lexicos.clear()  # Limpiar errores de la ejecución anterior
            lexer.lineno = 1
            lexer.input(codigo_previo)
            
            while True:
                tok = lexer.token()
                if not tok:
                    break
                col = calcular_columna(codigo_previo, tok)
                tokens_lexico.append({
                    "token": tok.value, "tipo": tok.type, "valor": tok.value,
                    "linea": tok.lineno, "columna": col
                })
            
            stats["tokens"] = len(tokens_lexico)

            # --- CONTROL DE FLUJO EN CASCADA ---
            if errores_lexicos:
                # Si hay errores léxicos, los agregamos a la tabla, cambiamos estado y DETENEMOS el flujo
                tokens_lexico.extend(errores_lexicos)
                stats["estado"] = "⚠️ Error Léxico"
            else:
                # Si el léxico está totalmente limpio, procedemos con las siguientes fases
                stats["estado"] = "Sin errores"
                
                # ==========================================
                # 2. ANÁLISIS SINTÁCTICO (Solo si el Léxico es OK)
                # ==========================================
                ast, err_sintacticos = analizar_web(codigo_previo)
                
                if err_sintacticos:
                    stats["estado"] = "⚠️ Error Sintáctico"
                    for e in err_sintacticos:
                        reglas_sintactico.append({
                            "regla": f"ERROR (Línea {e['linea']})",
                            "expresion": e['error'],
                            "estado": "❌ Fallido"
                        })
                elif ast:
                    aplanar_ast(ast, reglas_sintactico)
                    
                    # ==========================================
                    # 3. ANÁLISIS SEMÁNTICO (Solo si Sintáctico es OK)
                    # ==========================================
                    runner = SemanticRunner()
                    runner.run(ast)

                    # Agregar la tabla de símbolos a la vista
                    for variable, tipo in runner.sem.table.symbols.items():
                        tabla_semantico.append({
                            "variable": variable,
                            "tipo": tipo.upper(),
                            "valor": "✅ Declarada en Memoria"
                        })

                    # Si hay errores semánticos, los ponemos al principio de la tabla
                    if runner.sem.errors:
                        stats["estado"] = "⚠️ Error Semántico"
                        for error in runner.sem.errors:
                            tabla_semantico.insert(0, {
                                "variable": "ERROR SEMÁNTICO",
                                "tipo": "INCOHERENCIA LÓGICA",
                                "valor": f"❌ {error}"
                            })

            # ==========================================
            # GUARDADO DE LOGS (Modal)
            # ==========================================
            if 'guardar_logs' in request.form:
                usuario_git = request.form.get('usuarioGit')
                fases_seleccionadas = request.form.getlist('fases')
                
                if usuario_git and fases_seleccionadas:
                    fecha_hora = datetime.now().strftime("%d-%m-%Y-%Hh%M")
                    for fase in fases_seleccionadas:
                        nombre_archivo = f"{fase}-{usuario_git}-{fecha_hora}.txt"
                        ruta_archivo = os.path.join(LOGS_DIR, fase, nombre_archivo)
                        
                        with open(ruta_archivo, 'w', encoding='utf-8') as f:
                            f.write(f"=== LOG DE ANÁLISIS {fase.upper()} ===\n")
                            f.write(f"Usuario: {usuario_git}\n")
                            f.write(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                            f.write("=" * 40 + "\n")
                            
                            if fase == 'lexico':
                                for t in tokens_lexico:
                                    f.write(f"Línea {t['linea']}, Col {t['columna']} | {t['tipo']} : {t['valor']}\n")
                            elif fase == 'sintactico':
                                if not reglas_sintactico:
                                    f.write("No se detectaron errores sintácticos o no hay datos cargados.\n")
                                else:
                                    for s in reglas_sintactico:
                                        f.write(f"Regla: {s['regla']} | Estado: {s['estado']}\nDetalle: {s['expresion']}\n{'-'*40}\n")
                            elif fase == 'semantico':
                                if not tabla_semantico:
                                    f.write("No hay datos en la tabla de símbolos o no hay datos cargados.\n")
                                else:
                                    for s in tabla_semantico:
                                        f.write(f"ID: {s['variable']} | Tipo: {s['tipo']} | Valor: {s['valor']}\n")
                    
                    stats["estado"] += " (Logs Guardados)"

        else:
            stats["estado"] = "⚠️ El editor está vacío"

    return render_template('index.html', codigo=codigo_previo, lexico=tokens_lexico, sintactico=reglas_sintactico, semantico=tabla_semantico, stats=stats)

if __name__ == '__main__':
    app.run(debug=True)