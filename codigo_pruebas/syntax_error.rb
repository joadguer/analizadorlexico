# ==========================================
# 3. ERROR SINTACTICO
# ==========================================

edad = 20

# Error 1: Falta la expresion izquierda en la comparacion
if >= 18 
    puts "Mayor"
end

# Error 2: Asignacion invertida (La gramatica exige VARIABLE_LOCAL = expresion)
10 = contador

# Error 3: Funcion mal definida (falta la palabra 'end')
def saludar(nombre)
    puts nombre