# 02_procesador_archivos.py
import csv
import json
from pathlib import Path

# Definición de rutas
RUTA_CSV = Path("transacciones.csv")
RUTA_JSON_SALIDA = Path("transacciones_validas.json")

def procesar_transacciones_csv(ruta_archivo: Path):
    transacciones_validas = []
    registros_con_error = 0

    print(f"--- Iniciando lectura de: {ruta_archivo} ---")

    try:
        with open(ruta_archivo, mode="r", encoding="utf-8") as archivo:
            lector = csv.DictReader(archivo)
            
            for fila in lector:
                try:
                    # Intentamos convertir el monto a float (falla si viene texto invalido)
                    monto = float(fila["monto"])
                    print(f"Monto:  {monto}")
                    # Filtramos transacciones completadas con monto mayor a 0
                    if fila["estado"] == "COMPLETADO" and monto > 0:
                        transaccion_limpia = {
                            "id": fila["id_transaccion"],
                            "usuario": fila["usuario"].strip().lower(),
                            "monto": monto,
                            "fecha": fila["fecha"]
                        }
                        transacciones_validas.append(transaccion_limpia)
                        # Creando promedio

                        promedio = sum(t["monto"] for t in transacciones_validas) / len(transacciones_validas)
                        
                except ValueError as ve:
                    print(f"⚠️ Error de conversion en fila {fila['id_transaccion']}: {ve}")
                    registros_con_error += 1

    except FileNotFoundError:
        print(f"❌ Error: El archivo {ruta_archivo} no existe.")
        return []

    print(f"✅ Procesamiento finalizado. Validos: {len(transacciones_validas)} | Errores: {registros_con_error}")
    print(f"Promedio: {promedio}")
    return transacciones_validas


def guardar_en_json(datos: list, ruta_salida: Path):
    """Guarda la lista de diccionarios procesados en un archivo JSON."""
    try:
        with open(ruta_salida, mode="w", encoding="utf-8") as archivo:
            json.dump(datos, archivo, indent=4, ensure_ascii=False)
        print(f"💾 Datos exportados exitosamente a: {ruta_salida}")
    except Exception as e:
        print(f"❌ Error al escribir el archivo JSON: {e}")


# --- Ejecucion del Pipeline ---
if __name__ == "__main__":
    datos_limpios = procesar_transacciones_csv(RUTA_CSV)
    if datos_limpios:
        guardar_en_json(datos_limpios, RUTA_JSON_SALIDA)