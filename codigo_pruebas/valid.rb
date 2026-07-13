IMPUESTO = 12
precio = 100
estado = true
# Definicion de funcion con 2 parametros
def calcular_total(monto, iva)
    calculo = monto + iva
    return calculo
end
# Estructura condicional y llamada a funcion
if precio > 50 && estado == true
    total = calcular_total(precio, IMPUESTO)
    puts total
else
    puts 0
end
# Bucle while
contador = 0
while contador < 3
    contador += 1
end
# Estructuras de datos (Lista y Hash)
mi_lista = [10, 20, 30]
mi_hash = { 1 => 100, 2 => 200 }