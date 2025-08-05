# -*- coding: utf-8 -*-
"""
Script de Distribuição - SmartPLM PLMXML Reporter
Facilita a criação de pacotes para distribuição
"""

import os
import sys
import shutil
import zipfile
from datetime import datetime
from config_app import get_info_completa, DISTRIBUICAO

def criar_pasta_distribuicao():
    """Cria pasta para distribuição"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    pasta_dist = f"distribuicao_{timestamp}"
    
    if not os.path.exists(pasta_dist):
        os.makedirs(pasta_dist)
    
    return pasta_dist

def copiar_arquivos_essenciais(pasta_destino):
    """Copia arquivos essenciais para distribuição"""
    arquivos_essenciais = [
        'src/',
        'gui_runner.py',
        'xslt_generator_runner.py',
        'iniciar_interface.bat',
        'iniciar_xslt_generator.bat',
        'iniciar_interface.sh',
        'README_INTERFACE_GRAFICA.md',
        'README_XSLT_GENERATOR.md',
        'GUIA_XSLT_PERSONALIZADO.md',
        'GUIA_HTML_COMPLETO.md',
        'config_app.py'
    ]
    
    for arquivo in arquivos_essenciais:
        if os.path.exists(arquivo):
            if os.path.isdir(arquivo):
                shutil.copytree(arquivo, os.path.join(pasta_destino, arquivo))
            else:
                shutil.copy2(arquivo, pasta_destino)
            print(f"✅ Copiado: {arquivo}")

def criar_arquivo_instalacao(pasta_destino):
    """Cria arquivo de instalação"""
    info = get_info_completa()
    
    instalacao_content = f"""# SmartPLM PLMXML Reporter - Instalação

## Informações da Aplicação
- **Empresa:** {info['empresa']['nome']}
- **Slogan:** {info['empresa']['slogan']}
- **Aplicação:** {info['aplicacao']['nome']} v{info['aplicacao']['versao']}
- **Desenvolvedor:** {info['desenvolvedor']['nome']}
- **Copyright:** {info['aplicacao']['copyright']}

## Requisitos do Sistema
- Python 3.7 ou superior
- Tkinter (geralmente incluído com Python)
- Bibliotecas padrão do Python

## Instalação

### Windows
1. Certifique-se de ter Python instalado
2. Execute `iniciar_interface.bat` para a interface principal
3. Execute `iniciar_xslt_generator.bat` para o gerador XSLT

### Linux/Mac
1. Certifique-se de ter Python 3 instalado
2. Execute: `python3 gui_runner.py` para a interface principal
3. Execute: `python3 xslt_generator_runner.py` para o gerador XSLT

## Funcionalidades

### Interface Principal
- Processamento de múltiplos arquivos PLMXML
- Parsers básico e avançado
- Geração de relatórios HTML
- Logs em tempo real

### Gerador XSLT
- Análise de estrutura PLMXML
- Busca de campos específicos
- Geração automática de código XSLT
- Geração de HTML completo
- Suporte a campos wt9_

## Suporte
- **Email:** {info['empresa']['email']}
- **Website:** {info['empresa']['website']}
- **Desenvolvedor:** {info['desenvolvedor']['nome']}

## Licença
{info['aplicacao']['copyright']}
"""
    
    with open(os.path.join(pasta_destino, 'INSTALACAO.md'), 'w', encoding='utf-8') as f:
        f.write(instalacao_content)
    
    print("✅ Criado: INSTALACAO.md")

def criar_arquivo_licenca(pasta_destino):
    """Cria arquivo de licença"""
    licenca_content = f"""# Licença SmartPLM

## {get_info_completa()['aplicacao']['copyright']}

### Termos de Uso

1. **Licença de Uso:** Esta aplicação é fornecida "como está" para uso comercial e não comercial.

2. **Redistribuição:** É permitida a redistribuição da aplicação, desde que:
   - Mantenha todos os arquivos originais
   - Inclua este arquivo de licença
   - Não remova os créditos da SmartPLM e do desenvolvedor

3. **Modificações:** É permitido modificar a aplicação para uso interno, desde que:
   - Mantenha os créditos originais
   - Não distribua versões modificadas sem autorização

4. **Responsabilidade:** A SmartPLM não se responsabiliza por:
   - Perda de dados durante o uso
   - Problemas de compatibilidade
   - Danos indiretos causados pelo uso

5. **Suporte:** O suporte técnico está disponível através de:
   - Email: {get_info_completa()['empresa']['email']}
   - Website: {get_info_completa()['empresa']['website']}

### Informações do Desenvolvedor
- **Nome:** {get_info_completa()['desenvolvedor']['nome']}
- **Email:** {get_info_completa()['desenvolvedor']['email']}

### Versão da Aplicação
- **Nome:** {get_info_completa()['aplicacao']['nome']}
- **Versão:** {get_info_completa()['aplicacao']['versao']}
- **Descrição:** {get_info_completa()['aplicacao']['descricao']}

Data de Criação: {datetime.now().strftime('%d/%m/%Y')}
"""
    
    with open(os.path.join(pasta_destino, 'LICENSE'), 'w', encoding='utf-8') as f:
        f.write(licenca_content)
    
    print("✅ Criado: LICENSE")

def criar_zip_distribuicao(pasta_destino):
    """Cria arquivo ZIP para distribuição"""
    info = get_info_completa()
    nome_zip = f"{info['distribuicao']['nome_pacote']}_v{info['distribuicao']['versao']}.zip"
    
    with zipfile.ZipFile(nome_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(pasta_destino):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, pasta_destino)
                zipf.write(file_path, arcname)
    
    print(f"✅ Criado: {nome_zip}")
    return nome_zip

def main():
    """Função principal de distribuição"""
    print("🚀 Iniciando criação do pacote de distribuição...")
    print("=" * 60)
    
    # Informações da aplicação
    info = get_info_completa()
    print(f"📦 Empresa: {info['empresa']['nome']}")
    print(f"📦 Aplicação: {info['aplicacao']['nome']} v{info['aplicacao']['versao']}")
    print(f"📦 Desenvolvedor: {info['desenvolvedor']['nome']}")
    print("=" * 60)
    
    # Criar pasta de distribuição
    pasta_dist = criar_pasta_distribuicao()
    print(f"📁 Pasta criada: {pasta_dist}")
    
    # Copiar arquivos essenciais
    print("\n📋 Copiando arquivos essenciais...")
    copiar_arquivos_essenciais(pasta_dist)
    
    # Criar arquivos de documentação
    print("\n📝 Criando documentação...")
    criar_arquivo_instalacao(pasta_dist)
    criar_arquivo_licenca(pasta_dist)
    
    # Criar ZIP de distribuição
    print("\n🗜️ Criando arquivo ZIP...")
    nome_zip = criar_zip_distribuicao(pasta_dist)
    
    print("\n" + "=" * 60)
    print("✅ Distribuição criada com sucesso!")
    print(f"📦 Arquivo: {nome_zip}")
    print(f"📁 Pasta: {pasta_dist}")
    print("=" * 60)
    
    print("\n📋 Próximos passos para distribuição:")
    print("1. Teste o pacote em um ambiente limpo")
    print("2. Verifique se todos os arquivos estão incluídos")
    print("3. Compartilhe o arquivo ZIP com os usuários")
    print("4. Forneça instruções de instalação")
    
    return nome_zip

if __name__ == "__main__":
    main() 