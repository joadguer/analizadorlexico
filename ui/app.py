from flask import Flask, render_template, request
from lex import lexer

app = Flask(__name__)

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