# ============================================================
# Algoritmo de Validación de Nómina y Descuentos en Ruby
# ============================================================

TASA_IMPUESTO = 0.12
LIMITE_BONO = 500.0

def calcular_neto(sueldo_base, horas_extra)
    @bonificacion = horas_extra * 25.5
    $total_ingresos = sueldo_base + @bonificacion
    
    if $total_ingresos >= LIMITE_BONO && sueldo_base != nil
        $total_ingresos += 50.0
    else
        $total_ingresos -= 10.0
    end
    
    # Aplicar impuesto de ley
    descuento = $total_ingresos * TASA_IMPUESTO
    salario_final = $total_ingresos - descuento
    
    return salario_final
end

# Pruebas de impresión y tipos de datos
nombre_empleado = "Adrian Guerrero"
edad = 21
status_activo = true

puts nombre_empleado
puts calcular_neto(450, 4)