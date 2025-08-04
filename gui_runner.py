# -*- coding: utf-8 -*-
"""
Script Principal para Interface Gráfica do PLMXML Reporter
Executa a interface gráfica moderna para processamento de arquivos PLMXML
"""

import os
import sys

# Adiciona o diretório src ao path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def main():
    """Função principal para executar a interface gráfica"""
    try:
        from src.gui.interface_grafica import main as gui_main
        
        print("🚀 Iniciando Interface Gráfica do PLMXML Reporter...")
        print("=" * 50)
        print("📋 Funcionalidades disponíveis:")
        print("   • Seleção de múltiplos arquivos PLMXML")
        print("   • Parser básico e avançado")
        print("   • Geração de relatórios HTML")
        print("   • Logs em tempo real")
        print("   • Visualização de resultados")
        print("=" * 50)
        
        gui_main()
        
    except ImportError as e:
        print(f"❌ Erro ao importar módulos: {e}")
        print("💡 Verifique se todas as dependências estão instaladas")
        return 1
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 