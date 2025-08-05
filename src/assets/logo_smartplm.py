# -*- coding: utf-8 -*-
"""
Logo ASCII Art para SmartPLM
Logo simples em ASCII para usar na aplicação
"""

LOGO_SMARTPLM = """
SMARTPLM
"""

LOGO_SMARTPLM_SIMPLE = """
SMARTPLM"""

LOGO_SMARTPLM_COMPACT = """
SMARTPLM
"""

def get_logo(style="simple"):
    """Retorna o logo no estilo especificado"""
    if style == "full":
        return LOGO_SMARTPLM
    elif style == "compact":
        return LOGO_SMARTPLM_COMPACT
    else:
        return LOGO_SMARTPLM_SIMPLE 