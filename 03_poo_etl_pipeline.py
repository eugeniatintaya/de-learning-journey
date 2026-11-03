# 03_poo_etl_pipeline.py
import csv
import json
from pathlib import Path
from typing import List, Dict, Any


class TransaccionesETL:
    """Clase modular para ejecutar procesos ETL sobre archivos de transacciones."""

    def __init__(self, ruta_origen: str, ruta_destino: str):
        self.ruta_origen = Path(ruta_origen)
        self.ruta_destino = Path(ruta_destino)
        self.datos_extraidos: List[Dict[str, Any]] = []
        self.datos_transformados: List[Dict[str, Any]] = []

    def extraer(self) -> bool:
        """Paso E (Extract): Lee el archivo CSV de origen."""
        print(f"📥 [Extract] Leyendo datos desde: {self.ruta_origen}")
        if not self.ruta_origen.exists():
            print(f"❌ Error: El archivo {self.ruta_origen} no existe.")
            return False

        try:
            with open(self.ruta_origen, mode="r", encoding="utf-8") as archivo:
                lector = csv.DictReader(archivo)
                self.datos_extraidos = [fila for fila in lector]
            print(f"✅ Extraccion exitosa: {len(self.datos_extraidos)} registros leidos.")
            return True
        except Exception as e:
            print(f"❌ Error durante la extraccion: {e}")
            return False

    def transformar(self, **kwargs) -> None:
        """
        Paso T (Transform): Limpia datos, filtra y aplica transformaciones dinamicas.
        Soporta parametros extras usando **kwargs.
        """
        monto_minimo = kwargs.get("monto_minimo", 0.0)
        estado_requerido = kwargs.get("estado", "COMPLETADO")

        print(f"⚙️ [Transform] Filtrando transacciones con estado='{estado_requerido}' y monto > {monto_minimo}")
        
        for fila in self.datos_extraidos:
            try:
                monto = float(fila.get("monto", 0))
                estado = fila.get("estado", "").upper()

                if estado == estado_requerido and monto > monto_minimo:
                    self.datos_transformados.append({
                        "id": fila["id_transaccion"],
                        "usuario": fila["usuario"].strip().lower(),
                        "monto": monto,
                        "fecha": fila["fecha"]
                    })
            except ValueError:
                # Ignora registros con montos invalidos
                continue

        print(f"✅ Transformacion exitosa: {len(self.datos_transformados)} registros listos.")
    
    def exportar_txt(self, ruta_txt: str) -> None:
        """Exporta los datos transformados y las métricas a un archivo de texto."""
        print(f"📄 [Export] Guardando reporte en: {ruta_txt}")
        try:
            with open(ruta_txt, mode="w", encoding="utf-8") as archivo:
                archivo.write("REPORTE DE TRANSACCIONES\n")
                archivo.write("=" * 40 + "\n\n")

                for item in self.datos_transformados:
                    archivo.write(
                        f"{item['id']} | {item['usuario']} | "
                        f"{item['monto']:.2f} BOB | {item['fecha']}\n"
                    )

                metricas = self.obtener_metricas()
                archivo.write("\n" + "-" * 40 + "\n")
                archivo.write("RESUMEN\n")
                for clave, valor in metricas.items():
                    archivo.write(f"{clave}: {valor}\n")

            print("✅ Exportación a TXT finalizada con éxito.")
        except Exception as e:
            print(f"❌ Error al exportar a TXT: {e}")
          

    def cargar(self) -> None:
        """Paso L (Load): Exporta el resultado en formato JSON estructurado."""
        print(f"💾 [Load] Guardando datos procesados en: {self.ruta_destino}")
        try:
            with open(self.ruta_destino, mode="w", encoding="utf-8") as archivo:
                json.dump(self.datos_transformados, archivo, indent=4, ensure_ascii=False)
            print("✅ Carga finalizada con exito.")            
        except Exception as e:
            print(f"❌ Error durante la carga: {e}")

    def obtener_metricas(self) -> Dict[str, Any]:
        """Calcula agregaciones basicas sobre los datos transformados."""
        if not self.datos_transformados:
            return {"total_procesado": 0, "monto_total": 0.0, "promedio": 0.0}

        montos = [item["monto"] for item in self.datos_transformados]
        total = sum(montos)
        promedio = total / len(montos)

        return {
            "total_registros": len(montos),
            "monto_total_bob": round(total, 2),
            "monto_promedio_bob": round(promedio, 2)
        }

    
# --- Ejecucion del Pipeline Orientado a Objetos ---
if __name__ == "__main__":
    # Instanciamos nuestra pipeline
    pipeline = TransaccionesETL(
        ruta_origen="transacciones.csv", 
        ruta_destino="transacciones_poo_salida.json"
    )

    # Ejecutamos el flujo modular
    if pipeline.extraer():
        # Pasamos configuraciones flexibles con kwargs
        pipeline.transformar(monto_minimo=1500.0, estado="COMPLETADO")
        pipeline.cargar()
        pipeline.exportar_txt("transacciones_reporte.txt")

        # Obtenemos el reporte analitico
        metricas = pipeline.obtener_metricas()
        print("\n📊 --- RESUMEN DEL PIPELINE ---")
        for clave, valor in metricas.items():
            print(f"  • {clave}: {valor}")