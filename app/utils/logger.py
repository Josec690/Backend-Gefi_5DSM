import logging
import json
from datetime import datetime
from pathlib import Path

# Criar diretório de logs
Path("logs").mkdir(exist_ok=True)

class JSONFormatter(logging.Formatter):
    """Formata logs em JSON"""
    def format(self, record):
        log_obj = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno
        }
        
        if record.exc_info:
            log_obj["exception"] = self.formatException(record.exc_info)
        
        return json.dumps(log_obj)

def setup_logger(name):
    """Configura logger"""
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    # Handler para arquivo
    file_handler = logging.FileHandler(
        f'logs/gefi_{datetime.now().strftime("%Y%m%d")}.log'
    )
    file_handler.setFormatter(JSONFormatter())
    
    # Handler para console
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(
        logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    )
    
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger

# Logger global
logger = setup_logger('gefi-backend')