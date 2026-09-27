import logging, shutil
from CORE.RUTAS import *

logger = logging.getLogger("LOGS")

def limpiar_tmp ():
    
    try:
        if ruta_tmp.exists(): #SI EXISTE LA CARPETA TEMPORAL LA ELIMINAMOS
            shutil.rmtree(ruta_tmp)
            ruta_tmp.mkdir(exist_ok=True, parents=True)
            return True
        return False
    except Exception as e:
        logger.error(f"Error al limpiar la carpeta temporal: {e}")
        return False
        