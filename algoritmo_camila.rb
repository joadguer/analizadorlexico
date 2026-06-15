# ============================================================
# Algoritmo de Gestión de Inventario y Ventas
# Aporte: Camila Morán
# ============================================================

IVA = 0.15
LIMITE_STOCK = 20

def calcular_total(precio, cantidad)

    @subtotal = precio * cantidad

    if @subtotal >= 100
        @subtotal += 10

    elsif @subtotal == 50
        @subtotal += 5

    else
        @subtotal -= 2

    end

    return @subtotal

end

producto = "Laptop"
precio = 25.5
cantidad = 4

total = calcular_total(precio, cantidad)

stock = 30
ventas = 0

while stock > LIMITE_STOCK

    stock -= 2
    ventas += 1

    puts stock

end

descuento = total % 3

estado_activo = true
cliente = nil

if stock >= 10 && estado_activo == true

    puts "Stock disponible"

elsif stock <= 5

    puts "Inventario critico"

else

    puts "Inventario estable"

end

productos = [10,20,30,40]

puts producto
puts total
puts productos