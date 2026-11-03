# 04_api_client.py
import requests
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Any

class ClientAPIETL:
    """Cliente para consumir datos económicos desde una API REST pública."""

    def __init__(self, url_api: str):
        self.url_api = url_api
        self.datos_brutos: Dict[str, Any] = {}

    def extraer_de_api(self) -> bool:
        """Realiza una petición GET a la API REST controlando excepciones y códigos HTTP."""
        print(f"🌐 [API Extract] Conectándose a: {self.url_api}")
        
        try:
            # timeout=10 evita que el script se quede colgado indefinidamente si la red falla
            respuesta = requests.get(self.url_api, timeout=10)
            
            # Verificamos si el código de estado es exitoso (200)
            if respuesta.status_code == 200:
                self.datos_brutos = respuesta.json()
                print("✅ Conexión y extracción de API exitosas.")
                return True
            else:
                print(f"⚠️ Advertencia: La API respondió con código de estado: {respuesta.status_code}")
                return False

        except requests.exceptions.Timeout:
            print("❌ Error: La petición a la API excedió el tiempo límite (Timeout).")
            return False
        except requests.exceptions.RequestException as e:
            print(f"❌ Error de red o conexión con la API: {e}")
            return False

    def transformar_tasas(self) -> Dict[str, Any]:
        """Extrae la fecha de actualización y filtra monedas clave de interés."""
        if not self.datos_brutos:
            print("⚠️ No hay datos para transformar.")
            return {}

        meta_info = {
            "moneda_base": self.datos_brutos.get("base_code"),
            "ultima_actualizacion": self.datos_brutos.get("time_last_update_utc"),
            "fecha_consulta": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        # Tasas de interés seleccionadas para el ejemplo
        tasas_completas = self.datos_brutos.get("rates", {})
        monedas_interes = ["BOB", "EUR", "ARS", "BRL", "CLP", "PEN"]
        
        tasas_filtradas = {
            moneda: tasas_completas[moneda] 
            for moneda in monedas_interes 
            if moneda in tasas_completas
        }

        resultado_final = {
            "metadatos": meta_info,
            "tasas_cambio": tasas_filtradas
        }

        return resultado_final

    def guardar_json(self, datos: dict, ruta_salida: str) -> None:
        """Guarda el resultado de la API en un archivo JSON local."""
        ruta = Path(ruta_salida)
        try:
            with open(ruta, mode="w", encoding="utf-8") as archivo:
                json.dump(datos, archivo, indent=4, ensure_ascii=False)
            print(f"💾 [Load] Datos de API guardados exitosamente en: {ruta}")
        except Exception as e:
            print(f"❌ Error al guardar el archivo JSON: {e}")


# --- Ejecución del Pipeline basado en API ---
if __name__ == "__main__":
    # URL de la API pública de tipos de cambio (Base: USD)
    URL_TASA_CAMBIO = "https://open.er-api.com/v6/latest/USD"

    # Instanciamos el cliente
    cliente = ClientAPIETL(URL_TASA_CAMBIO)

    if cliente.extraer_de_api():
        # Transformamos y filtramos los datos
        datos_limpios = cliente.transformar_tasas()
        
        if datos_limpios:
            print("\n📊 --- DATOS TRANSFORMADOS DESDE LA API ---")
            print(json.dumps(datos_limpios, indent=4, ensure_ascii=False))
            
            # Guardamos el archivo JSON resultante
            cliente.guardar_json(datos_limpios, "tasas_cambio_salida.json")