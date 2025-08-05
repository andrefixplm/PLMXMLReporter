# -*- coding: utf-8 -*-
"""
Configurações da Aplicação SmartPLM
Arquivo de configuração para facilitar a distribuição
"""

# Informações da Empresa
EMPRESA_NOME = "SmartPLM"
EMPRESA_SLOGAN = "Soluções Inteligentes em PLM"
EMPRESA_EMAIL = "contato@smartplm.com"
EMPRESA_WEBSITE = "www.smartplm.com"

# Informações do Desenvolvedor
DESENVOLVEDOR_NOME = "André Luiz"
DESENVOLVEDOR_EMAIL = "andre.luiz@smartplm.com"

# Informações da Aplicação
APP_NOME = "PLMXML Reporter"
APP_VERSAO = "2.0"
APP_DESCRICAO = "Ferramenta completa para processamento e análise de arquivos PLMXML"
APP_COPYRIGHT = "© 2025 SmartPLM - Todos os direitos reservados"

# Configurações de Interface
CORES = {
    'primaria': '#007acc',
    'secundaria': '#005a99',
    'fundo': '#f0f0f0',
    'texto': '#333333',
    'texto_claro': '#666666',
    'destaque': '#ff6b35'
}

# Configurações de Log
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
LOG_FILE_PREFIX = "smartplm_"

# Configurações de Arquivo
EXTENSOES_SUPORTADAS = ['.xml', '.plmxml']
TAMANHO_MAX_ARQUIVO = 100 * 1024 * 1024  # 100MB

# Configurações de Saída
PASTA_SAIDA_PADRAO = "resultados"
FORMATOS_SAIDA = ['html', 'xml', 'json', 'xslt']

# Configurações de Performance
MAX_THREADS = 4
TIMEOUT_PROCESSAMENTO = 300  # 5 minutos

# Configurações de Distribuição
DISTRIBUICAO = {
    'nome_pacote': 'smartplm_plmxml_reporter',
    'versao': '2.0.0',
    'plataformas': ['windows', 'linux', 'macos'],
    'dependencias': [
        'tkinter',
        'xml.etree.ElementTree',
        'datetime',
        'os',
        'sys',
        're'
    ],
    'arquivos_incluir': [
        'src/',
        '*.py',
        '*.bat',
        '*.sh',
        '*.md',
        'README*',
        'LICENSE'
    ],
    'arquivos_excluir': [
        '__pycache__/',
        '*.pyc',
        '*.log',
        'resultados/',
        'temp/'
    ]
}

def get_info_completa():
    """Retorna informações completas da aplicação"""
    return {
        'empresa': {
            'nome': EMPRESA_NOME,
            'slogan': EMPRESA_SLOGAN,
            'email': EMPRESA_EMAIL,
            'website': EMPRESA_WEBSITE
        },
        'desenvolvedor': {
            'nome': DESENVOLVEDOR_NOME,
            'email': DESENVOLVEDOR_EMAIL
        },
        'aplicacao': {
            'nome': APP_NOME,
            'versao': APP_VERSAO,
            'descricao': APP_DESCRICAO,
            'copyright': APP_COPYRIGHT
        },
        'cores': CORES,
        'distribuicao': DISTRIBUICAO
    }

def get_cabecalho_app():
    """Retorna cabeçalho formatado da aplicação"""
    return f"""
{EMPRESA_NOME} - {EMPRESA_SLOGAN}
{APP_NOME} v{APP_VERSAO}
Desenvolvido por {DESENVOLVEDOR_NOME}
{APP_COPYRIGHT}
"""

def get_rodape_app():
    """Retorna rodapé formatado da aplicação"""
    return f"""
{APP_COPYRIGHT}
{EMPRESA_NOME} - {EMPRESA_SLOGAN}
Contato: {EMPRESA_EMAIL} | Website: {EMPRESA_WEBSITE}
Desenvolvido por {DESENVOLVEDOR_NOME}
""" 