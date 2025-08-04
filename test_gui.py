# -*- coding: utf-8 -*-
"""
Script de Teste para Interface Gráfica do PLMXML Reporter
Verifica se todos os componentes estão funcionando corretamente
"""

import os
import sys
import tkinter as tk
from tkinter import messagebox

def testar_imports():
    """Testa se todos os imports necessários estão funcionando"""
    print("🔍 Testando imports...")
    
    try:
        # Testa imports básicos
        import threading
        import webbrowser
        import subprocess
        print("✅ Imports básicos OK")
        
        # Testa tkinter
        import tkinter as tk
        from tkinter import ttk, filedialog, messagebox, scrolledtext
        print("✅ Tkinter OK")
        
        # Testa imports do projeto
        sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
        
        from src.utils.logger import configurar_logger
        print("✅ Logger OK")
        
        from src.parsers.plmxml_parser_basico import PLMXMLParserBasico
        print("✅ Parser Básico OK")
        
        from src.parsers.plmxml_parser_avancado import PLMXMLParserAvancado
        print("✅ Parser Avançado OK")
        
        from src.transformers.json_para_xml import JSONParaXMLConverter
        print("✅ Conversor JSON->XML OK")
        
        from src.transformers.aplicar_xslt import XSLTProcessor
        print("✅ Processador XSLT OK")
        
        return True
        
    except ImportError as e:
        print(f"❌ Erro de import: {e}")
        return False
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        return False

def testar_interface():
    """Testa se a interface gráfica pode ser criada"""
    print("🔍 Testando interface gráfica...")
    
    try:
        # Cria janela de teste
        root = tk.Tk()
        root.withdraw()  # Esconde a janela
        
        # Testa criação de componentes básicos
        frame = tk.Frame(root)
        label = tk.Label(frame, text="Teste")
        button = tk.Button(frame, text="Teste")
        
        print("✅ Componentes básicos OK")
        
        # Testa criação da interface completa
        from src.gui.interface_grafica import PLMXMLReporterGUI
        
        # Cria uma instância da interface (sem mostrar)
        app = PLMXMLReporterGUI(root)
        print("✅ Interface criada com sucesso")
        
        root.destroy()
        return True
        
    except Exception as e:
        print(f"❌ Erro na interface: {e}")
        return False

def testar_arquivos():
    """Testa se os arquivos necessários existem"""
    print("🔍 Testando arquivos...")
    
    arquivos_necessarios = [
        'src/gui/interface_grafica.py',
        'src/gui/__init__.py',
        'gui_runner.py',
        'src/utils/logger.py',
        'src/parsers/plmxml_parser_basico.py',
        'src/parsers/plmxml_parser_avancado.py',
        'src/transformers/json_para_xml.py',
        'src/transformers/aplicar_xslt.py'
    ]
    
    todos_existem = True
    for arquivo in arquivos_necessarios:
        if os.path.exists(arquivo):
            print(f"✅ {arquivo}")
        else:
            print(f"❌ {arquivo} - NÃO ENCONTRADO")
            todos_existem = False
    
    return todos_existem

def testar_pastas():
    """Testa se as pastas necessárias existem"""
    print("🔍 Testando pastas...")
    
    pastas_necessarias = [
        'data/input',
        'data/output',
        'logs',
        'templates/xslt'
    ]
    
    todas_existem = True
    for pasta in pastas_necessarias:
        if os.path.exists(pasta):
            print(f"✅ {pasta}")
        else:
            print(f"⚠️  {pasta} - Criando...")
            try:
                os.makedirs(pasta, exist_ok=True)
                print(f"✅ {pasta} - Criada")
            except Exception as e:
                print(f"❌ Erro ao criar {pasta}: {e}")
                todas_existem = False
    
    return todas_existem

def main():
    """Função principal de teste"""
    print("🚀 TESTE DA INTERFACE GRÁFICA - PLMXML REPORTER")
    print("=" * 50)
    
    # Executa todos os testes
    testes = [
        ("Arquivos", testar_arquivos),
        ("Pastas", testar_pastas),
        ("Imports", testar_imports),
        ("Interface", testar_interface)
    ]
    
    resultados = []
    for nome, teste in testes:
        print(f"\n📋 Testando {nome}...")
        resultado = teste()
        resultados.append((nome, resultado))
    
    # Relatório final
    print("\n" + "=" * 50)
    print("📊 RELATÓRIO DE TESTES")
    print("=" * 50)
    
    sucessos = 0
    for nome, resultado in resultados:
        status = "✅ PASSOU" if resultado else "❌ FALHOU"
        print(f"{nome}: {status}")
        if resultado:
            sucessos += 1
    
    print(f"\n🎯 Resultado: {sucessos}/{len(resultados)} testes passaram")
    
    if sucessos == len(resultados):
        print("🎉 Todos os testes passaram! Interface pronta para uso.")
        print("\n💡 Para executar a interface gráfica:")
        print("   python gui_runner.py")
    else:
        print("⚠️  Alguns testes falharam. Verifique os erros acima.")
    
    return sucessos == len(resultados)

if __name__ == "__main__":
    sucesso = main()
    sys.exit(0 if sucesso else 1) 