# 01_estructuras_datos.py
# Simulación de extracción de datos de una base de datos o API

registros = [
    {"id": 1, "usuario": "mefp_user1", "monto": 1500.50, "estado": "completado"},
    {"id": 2, "usuario": "mefp_user2", "monto": 0.00, "estado": "pendiente"},
    {"id": 3, "usuario": "mefp_user3", "monto": 3400.75, "estado": "completado"},
]

# 1. Filtrar solo las transacciones completadas (List Comprehension)
completados = [r for r in registros 
                if r["estado"] == "completado"
               ]

# 2. Calcular el total acumulado
total_monto = sum(r["monto"] for r in completados)

print(f"Transacciones completadas: {len(completados)}")
print(f"Monto total procesado: {total_monto} BOB")

# Nueva funcion 
# Agrega una función que reciba esa lista, convierta los nombres de usuario a mayúsculas y 
# aplique un filtro para obtener solo aquellos montos superiores a 2000.

usuario_mayusculas = [r["usuario"].upper() for r in registros]

usuario_filtros = [r["usuario"].upper() for r in registros if r["monto"] > 2000]

print(f"Usuario_mayusculas: {usuario_mayusculas}")
print(f"Usuario_filtros: {usuario_filtros}")                        
                      