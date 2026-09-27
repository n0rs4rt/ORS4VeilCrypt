import logging
from CORE.RUTAS import logs

def config_log ():
    
    logger = logging.getLogger("LOGS")

    logger.setLevel(logging.INFO)
    
    if not logger.handlers:
        handler = logging.FileHandler(logs / "logs.log")
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
    return logger