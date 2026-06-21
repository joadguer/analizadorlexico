# 1. Asignaciones y Tipos de Datos
edad = 21
PI = 3.1416
@sistema_activo = true

# 2. Entrada y Salida
puts "Iniciando analisis sintactico"
entrada = gets

# 3. Expresiones aritméticas con precedencia y agrupación
resultado = (5 + 3) * 2 / 4 - 1.5

# 4. Estructuras de Datos (Listas y Hashes)
numeros = [1, 2, 3, 4, 5]
datos = {"id" => 101, "rol" => "admin"}

# 5. Definición de Funciones con parámetros y retorno
def calcular_area(base, altura)
    area = base * altura
    return area
end

# 6. Llamada a Funciones
calculo_final = calcular_area(10, 5)

# 7. Estructuras de Control (If / Else) y Expresiones Lógicas/Relacionales
if edad >= 18 && @sistema_activo == true
    puts "Acceso permitido al sistema"
else
    puts "Acceso denegado"
end

# 8. Estructuras de Control Iterativas (While)
contador = 0
while contador < 5
    puts contador
    contador = contador + 1
end