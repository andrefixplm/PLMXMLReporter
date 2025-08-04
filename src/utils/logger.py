# -*- coding: utf-8 -*-
"""
Sistema de logs para o projeto
"""

import logging
import os
from datetime import datetime

def configurar_logger(nome_arquivo_log=None):
    """
    Configura o sistema de logs
    """
    if nome_arquivo_log is None:
        # Cria nome do arquivo com data/hora
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        nome_arquivo_log = f"logs\\plmxml_parser_{timestamp}.log"
    
    # Cria pasta de logs se não existir
    pasta_logs = os.path.dirname(nome_arquivo_log)
    if pasta_logs and not os.path.exists(pasta_logs):
        os.makedirs(pasta_logs)
    
    # Configura o logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(nome_arquivo_log, encoding='utf-8'),
            logging.StreamHandler()  # Para mostrar no console também
        ]
    )
    
    logger = logging.getLogger(__name__)
    logger.info(f"Logger configurado. Arquivo de log: {nome_arquivo_log}")
    
    return logger