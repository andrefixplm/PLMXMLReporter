# -*- coding: utf-8 -*-
"""
Script Principal para Gerador de XSLT do PLMXML Reporter
Executa o gerador de código XSLT para arquivos PLMXML
"""

import os
import sys

# Adiciona o diretório src ao path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def main():
    """Função principal para executar o gerador de XSLT"""
    try:
        from src.tools.xslt_generator import main as generator_main
        
        print("📝 Iniciando Gerador de Código XSLT - PLMXML Reporter...")
        print("=" * 60)
        print("📋 Funcionalidades disponíveis:")
        print("   • Análise de estrutura PLMXML")
        print("   • Busca de campos específicos")
        print("   • Geração automática de código XSLT")
        print("   • Visualização hierárquica")
        print("   • Cópia e salvamento de código")
        print("=" * 60)
        
        generator_main()
        
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