import os
from datetime import datetime
from flask import Flask, render_template, request
from lex import lexer

app = Flask(__name__)


# 1. Configuración de carpetas principales y subcarpetas
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOGS_DIR = os.path.join(BASE_DIR, 'logs')


def calcular_columna(codigo, token):
    """
    Calcula la columna exacta de un token dentro del código fuente.
    """
    ultimo_salto = codigo.rfind('\n', 0, token.lexpos)
    if ultimo_salto < 0:
        columna = token.lexpos + 1
    else:
        columna = token.lexpos - ultimo_salto
    return columna

@app.route('/', methods=['GET', 'POST'])
def index():
    # Valores por defecto cuando la página carga por primera vez
    codigo_previo = ""
    tokens_lexico = []
    reglas_sintactico = []  # Queda listo para cuando acoples el parser (Yacc)
    semantico = [] # Agregado para prever la tabla semántica
    stats = {"lineas": 0, "chars": 0, "tokens": 0, "estado": "Esperando código..."}

    if request.method == 'POST':
        # Si presionaron "Limpiar", vaciamos todo regresando a los valores por defecto
        if 'limpiar' in request.form:
            return render_template('index.html', codigo="", lexico=[], sintactico=[], stats=stats)

        # Si presionaron "Analizar Código"
        codigo_previo = request.form.get('codigo', '')
        
        # Calcular estadísticas básicas iniciales
        stats["chars"] = len(codigo_previo)
        stats["lineas"] = len(codigo_previo.splitlines()) if codigo_previo else 0
        
        if codigo_previo.strip():
            # 1. Reiniciar y alimentar el lexer de PLY con el código del formulario
            lexer.lineno = 1
            lexer.input(codigo_previo)
            
            # 2. Ciclo para extraer tokens y mapearlos al formato de tu tabla HTML
            while True:
                tok = lexer.token()
                if not tok:
                    break  # Fin del código fuente
                
                col = calcular_columna(codigo_previo, tok)
                
                # Insertamos el token estructurado en la lista
                tokens_lexico.append({
                    "token": tok.value,
                    "tipo": tok.type,
                    "valor": tok.value,
                    "linea": tok.lineno,
                    "columna": col
                })
            
            # 3. Actualizar estadísticas finales
            stats["tokens"] = len(tokens_lexico)
            stats["estado"] = "Sin errores"
            # 2. Lógica para procesar el modal de "Guardar Logs"
            if 'guardar_logs' in request.form:
                usuario_git = request.form.get('usuarioGit')
                fases_seleccionadas = request.form.getlist('fases') # Captura los checkboxes seleccionados
                
                if not usuario_git or not fases_seleccionadas:
                    stats["estado"] = "⚠️ Selecciona un usuario y al menos una fase para guardar."
                else:
                    # formato con guiones: DD-MM-YYYY-HHhMM
                    fecha_hora = datetime.now().strftime("%d-%m-%Y-%Hh%M")
                    rutas_exitosas = []
                    
                    for fase in fases_seleccionadas:
                        # Nombre con formato: fase-usuarioGit-fecha-hora.txt
                        nombre_archivo = f"{fase}-{usuario_git}-{fecha_hora}.txt"
                        ruta_archivo = os.path.join(LOGS_DIR, fase, nombre_archivo)
                        
                        try:
                            with open(ruta_archivo, 'w', encoding='utf-8') as f:
                                f.write(f"=== LOG DE ANÁLISIS {fase.upper()} ===\n")
                                f.write(f"Usuario: {usuario_git}\n")
                                f.write(f"Fecha de ejecución: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                                f.write("-" * 40 + "\n")
                                
                                if fase == 'lexico':
                                    for t in tokens_lexico:
                                        f.write(f"Línea {t['linea']}, Col {t['columna']} | {t['tipo']} : {t['valor']}\n")
                                elif fase == 'sintactico':
                                    if not reglas_sintactico:
                                        f.write("No se detectaron errores sintácticos o no hay datos cargados.\n")
                                    else:
                                        for s in reglas_sintactico:
                                            f.write(f"{s}\n") # Ajusta esto según el formato de tu diccionario sintáctico
                                elif fase == 'semantico':
                                    f.write("Fase en desarrollo: Aún no se han integrado reglas semánticas.\n")
                                    
                            rutas_exitosas.append(fase.capitalize())
                        except Exception as e:
                            stats["estado"] = f"Error al guardar {fase}: {str(e)}"
                            
                    if rutas_exitosas:
                        stats["estado"] = f"Logs guardados ({', '.join(rutas_exitosas)})"
        else:
            stats["estado"] = "⚠️ El editor está vacío"

    return render_template(
        'index.html', 
        codigo=codigo_previo, 
        lexico=tokens_lexico, 
        sintactico=reglas_sintactico, 
        stats=stats
    )

if __name__ == '__main__':
    app.run(debug=True)