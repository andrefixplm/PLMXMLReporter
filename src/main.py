# -*- coding: utf-8 -*-
"""
Script Principal - PLMXML Reporter
Integra todo o fluxo de processamento: Parser -> JSON -> XML -> XSLT -> HTML
"""

import os
import sys
import time
from datetime import datetime

# Adiciona path para imports
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from src.utils.logger import configurar_logger
from src.parsers.plmxml_parser_avancado import PLMXMLParserAvancado
from src.transformers.json_para_xml import JSONParaXMLConverter
from src.transformers.aplicar_xslt import XSLTProcessor

class PLMXMLReporter:
    def __init__(self):
        """
        Inicializa o sistema completo de relatórios PLMXML
        """
        self.logger = configurar_logger()
        self.logger.info("🚀 PLMXML Reporter inicializado")
        
        # Inicializa componentes
        self.parser = PLMXMLParserAvancado()
        self.conversor = JSONParaXMLConverter()
        self.xslt_processor = XSLTProcessor()
        
        # Estatísticas do processamento
        self.stats = {
            'arquivos_processados': 0,
            'tempo_total': 0,
            'erros': 0
        }
    
    def processar_arquivo_completo(self, arquivo_plmxml, gerar_html=True):
        """
        Processa um arquivo PLMXML completo: Parser -> JSON -> XML -> HTML
        
        Args:
            arquivo_plmxml (str): Caminho do arquivo PLMXML
            gerar_html (bool): Se deve gerar relatório HTML
        
        Returns:
            dict: Resultados do processamento
        """
        inicio_processamento = time.time()
        self.logger.info(f"🎯 Iniciando processamento completo: {arquivo_plmxml}")
        
        resultados = {
            'arquivo_entrada': arquivo_plmxml,
            'arquivos_gerados': {},
            'erros': [],
            'tempo_processamento': 0
        }
        
        try:
            # Etapa 1: Parser PLMXML -> JSON
            self.logger.info("📊 Etapa 1: Parsing PLMXML...")
            dados_json = self.parser.processar_arquivo_completo(arquivo_plmxml)
            
            if not dados_json:
                erro = "Falha no parsing PLMXML"
                self.logger.error(erro)
                resultados['erros'].append(erro)
                return resultados
            
            # Encontra arquivo JSON gerado
            pasta_output = "data\\output"
            arquivos_json = [f for f in os.listdir(pasta_output) 
                           if f.endswith('.json') and 'avancado' in f]
            
            if not arquivos_json:
                erro = "Arquivo JSON não encontrado"
                self.logger.error(erro)
                resultados['erros'].append(erro)
                return resultados
            
            arquivo_json = os.path.join(pasta_output, arquivos_json[-1])  # Mais recente
            resultados['arquivos_gerados']['json'] = arquivo_json
            
            # Etapa 2: JSON -> XML
            self.logger.info("🔄 Etapa 2: Conversão JSON -> XML...")
            arquivo_xml = self.conversor.converter_arquivo_json(arquivo_json)
            
            if not arquivo_xml:
                erro = "Falha na conversão JSON -> XML"
                self.logger.error(erro)
                resultados['erros'].append(erro)
                return resultados
            
            resultados['arquivos_gerados']['xml'] = arquivo_xml
            
            # Etapa 3: XML -> HTML (se solicitado)
            if gerar_html:
                self.logger.info("📄 Etapa 3: Transformação XSLT -> HTML...")
                arquivo_html = self.xslt_processor.aplicar_xslt(arquivo_xml)
                
                if arquivo_html:
                    resultados['arquivos_gerados']['html'] = arquivo_html
                else:
                    erro = "Falha na transformação XSLT"
                    self.logger.warning(erro)
                    resultados['erros'].append(erro)
            
            # Atualiza estatísticas
            self.stats['arquivos_processados'] += 1
            resultados['tempo_processamento'] = time.time() - inicio_processamento
            self.stats['tempo_total'] += resultados['tempo_processamento']
            
            self.logger.info("✅ Processamento completo concluído com sucesso")
            
        except Exception as e:
            erro = f"Erro inesperado: {str(e)}"
            self.logger.error(erro)
            resultados['erros'].append(erro)
            self.stats['erros'] += 1
        
        return resultados
    
    def processar_pasta_completa(self, pasta_entrada="data\\input", gerar_html=True):
        """
        Processa todos os arquivos PLMXML em uma pasta
        
        Args:
            pasta_entrada (str): Pasta com arquivos PLMXML
            gerar_html (bool): Se deve gerar relatórios HTML
        
        Returns:
            list: Lista de resultados
        """
        self.logger.info(f"📁 Processando pasta: {pasta_entrada}")
        
        if not os.path.exists(pasta_entrada):
            self.logger.error(f"Pasta não encontrada: {pasta_entrada}")
            return []
        
        # Lista arquivos PLMXML
        arquivos_plmxml = [f for f in os.listdir(pasta_entrada) 
                          if f.lower().endswith(('.xml', '.plmxml'))]
        
        if not arquivos_plmxml:
            self.logger.warning(f"Nenhum arquivo PLMXML encontrado em: {pasta_entrada}")
            return []
        
        self.logger.info(f"📂 Encontrados {len(arquivos_plmxml)} arquivo(s) PLMXML")
        
        resultados = []
        
        for arquivo in arquivos_plmxml:
            caminho_completo = os.path.join(pasta_entrada, arquivo)
            self.logger.info(f"\n🔄 Processando: {arquivo}")
            
            resultado = self.processar_arquivo_completo(caminho_completo, gerar_html)
            resultados.append(resultado)
        
        return resultados
    
    def imprimir_relatorio_final(self, resultados):
        """
        Imprime relatório final do processamento
        """
        print("\n" + "="*60)
        print("📊 RELATÓRIO FINAL DO PROCESSAMENTO")
        print("="*60)
        
        total_arquivos = len(resultados)
        sucessos = sum(1 for r in resultados if not r['erros'])
        erros = sum(1 for r in resultados if r['erros'])
        
        print(f"📁 Total de arquivos processados: {total_arquivos}")
        print(f"✅ Processamentos com sucesso: {sucessos}")
        print(f"❌ Processamentos com erro: {erros}")
        print(f"⏱️  Tempo total: {self.stats['tempo_total']:.2f} segundos")
        
        if resultados:
            tempo_medio = sum(r['tempo_processamento'] for r in resultados) / len(resultados)
            print(f"⏱️  Tempo médio por arquivo: {tempo_medio:.2f} segundos")
        
        print("\n📄 Arquivos gerados:")
        for resultado in resultados:
            if resultado['arquivos_gerados']:
                print(f"   📂 {os.path.basename(resultado['arquivo_entrada'])}:")
                for tipo, arquivo in resultado['arquivos_gerados'].items():
                    print(f"      • {tipo.upper()}: {os.path.basename(arquivo)}")
        
        if erros > 0:
            print("\n❌ Erros encontrados:")
            for resultado in resultados:
                if resultado['erros']:
                    print(f"   📂 {os.path.basename(resultado['arquivo_entrada'])}:")
                    for erro in resultado['erros']:
                        print(f"      • {erro}")
        
        print("="*60)

# Função principal
def main():
    """
    Função principal do PLMXML Reporter
    """
    print("🚀 PLMXML REPORTER - SISTEMA COMPLETO")
    print("=" * 60)
    print("📋 Fluxo: PLMXML -> JSON -> XML -> HTML")
    print("=" * 60)
    
    # Cria pastas necessárias
    for pasta in ["data\\input", "data\\output", "logs", "templates\\xslt"]:
        if not os.path.exists(pasta):
            os.makedirs(pasta)
            print(f"📁 Pasta criada: {pasta}")
    
    # Inicializa sistema
    reporter = PLMXMLReporter()
    
    # Processa arquivos
    resultados = reporter.processar_pasta_completa()
    
    # Imprime relatório final
    reporter.imprimir_relatorio_final(resultados)
    
    print("\n🎉 PROCESSAMENTO CONCLUÍDO!")
    print("📄 Verifique os resultados na pasta 'data\\output'")
    print("📋 Logs salvos na pasta 'logs'")

if __name__ == "__main__":
    main() 