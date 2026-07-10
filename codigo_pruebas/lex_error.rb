# ==========================================
# 2. ERROR LEXICO
# ==========================================

precio = 100
descuento = 10

# El simbolo ~ no pertenece a los tokens definidos
total = precio ~ descuento

# El simbolo ? no esta definido en tu lexer
es_valido = true ? false

puts total