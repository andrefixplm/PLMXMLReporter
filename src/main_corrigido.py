# -*- coding: utf-8 -*-
"""
Script Principal - PLMXML Reporter (VERSÃO CORRIGIDA)
Fluxo correto: PLMXML -> Dados Estruturados -> Relatórios
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

class PLMXMLReporterCorrigido:
    def __init__(self):
        """
        Inicializa o sistema completo de relatórios PLMXML
        """
        self.logger = configurar_logger()
        self.logger.info("🚀 PLMXML Reporter (Corrigido) inicializado")
        
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
        Processa um arquivo PLMXML com fluxo correto:
        PLMXML -> Dados Estruturados -> Relatórios
        
        Args:
            arquivo_plmxml (str): Caminho do arquivo PLMXML
            gerar_html (bool): Se deve gerar relatório HTML
        
        Returns:
            dict: Resultados do processamento
        """
        inicio_processamento = time.time()
        self.logger.info(f"🎯 Iniciando processamento: {arquivo_plmxml}")
        
        resultados = {
            'arquivo_entrada': arquivo_plmxml,
            'arquivos_gerados': {},
            'erros': [],
            'tempo_processamento': 0
        }
        
        try:
            # ETAPA 1: Parser PLMXML -> Dados Estruturados
            self.logger.info("📊 Etapa 1: Parsing PLMXML...")
            dados_estruturados = self.parser.processar_arquivo_completo(arquivo_plmxml)
            
            if not dados_estruturados:
                erro = "Falha no parsing PLMXML"
                self.logger.error(erro)
                resultados['erros'].append(erro)
                return resultados
            
            # Salva dados em JSON para referência
            arquivo_json = self._salvar_dados_json(dados_estruturados, arquivo_plmxml)
            if arquivo_json:
                resultados['arquivos_gerados']['json'] = arquivo_json
            
            # ETAPA 2: Converte para XML estruturado (para XSLT)
            self.logger.info("🔄 Etapa 2: Conversão para XML estruturado...")
            arquivo_xml = self.conversor.converter_arquivo_json(arquivo_json)
            
            if not arquivo_xml:
                erro = "Falha na conversão para XML"
                self.logger.error(erro)
                resultados['erros'].append(erro)
                return resultados
            
            resultados['arquivos_gerados']['xml'] = arquivo_xml
            
            # ETAPA 3: Gera relatório HTML (se solicitado)
            if gerar_html:
                self.logger.info("📄 Etapa 3: Geração de relatório HTML...")
                # Procura por arquivos XSLT disponíveis
                pasta_xslt = "templates\\xslt"
                arquivos_xslt = [f for f in os.listdir(pasta_xslt) if f.endswith('.xslt')] if os.path.exists(pasta_xslt) else []
                
                if arquivos_xslt:
                    arquivo_xslt = os.path.join(pasta_xslt, arquivos_xslt[0])  # Usa o primeiro XSLT encontrado
                    arquivo_html = self.xslt_processor.aplicar_xslt(arquivo_xml, arquivo_xslt)
                else:
                    # Se não há XSLT, usa método sem parâmetro
                    arquivo_html = self.xslt_processor.aplicar_xslt(arquivo_xml)
                
                if arquivo_html:
                    resultados['arquivos_gerados']['html'] = arquivo_html
                else:
                    erro = "Falha na geração do relatório HTML"
                    self.logger.warning(erro)
                    resultados['erros'].append(erro)
            
            # Atualiza estatísticas
            self.stats['arquivos_processados'] += 1
            resultados['tempo_processamento'] = time.time() - inicio_processamento
            self.stats['tempo_total'] += resultados['tempo_processamento']
            
            self.logger.info("✅ Processamento concluído com sucesso")
            
        except Exception as e:
            erro = f"Erro inesperado: {str(e)}"
            self.logger.error(erro)
            resultados['erros'].append(erro)
            self.stats['erros'] += 1
        
        return resultados
    
    def _salvar_dados_json(self, dados, arquivo_original):
        """
        Salva dados estruturados em JSON
        """
        try:
            # Cria pasta se não existir
            pasta_output = "data\\output"
            if not os.path.exists(pasta_output):
                os.makedirs(pasta_output)
            
            # Nome do arquivo baseado no arquivo original
            nome_base = os.path.splitext(os.path.basename(arquivo_original))[0]
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            arquivo_json = os.path.join(pasta_output, f"{nome_base}_dados_{timestamp}.json")
            
            # Salva dados
            import json
            with open(arquivo_json, 'w', encoding='utf-8') as f:
                json.dump(dados, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"💾 Dados salvos em JSON: {arquivo_json}")
            return arquivo_json
            
        except Exception as e:
            self.logger.error(f"Erro ao salvar JSON: {str(e)}")
            return None
    
    def processar_pasta_completa(self, pasta_entrada="data\\input", gerar_html=True):
        """
        Processa todos os arquivos PLMXML em uma pasta
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
    Função principal do PLMXML Reporter (Corrigido)
    """
    print("🚀 PLMXML REPORTER - SISTEMA COMPLETO (CORRIGIDO)")
    print("=" * 60)
    print("📋 Fluxo correto: PLMXML -> Dados -> Relatórios")
    print("=" * 60)
    
    # Cria pastas necessárias
    for pasta in ["data\\input", "data\\output", "logs", "templates\\xslt"]:
        if not os.path.exists(pasta):
            os.makedirs(pasta)
            print(f"📁 Pasta criada: {pasta}")
    
    # Inicializa sistema
    reporter = PLMXMLReporterCorrigido()
    
    # Processa arquivos
    resultados = reporter.processar_pasta_completa()
    
    # Imprime relatório final
    reporter.imprimir_relatorio_final(resultados)
    
    print("\n🎉 PROCESSAMENTO CONCLUÍDO!")
    print("📄 Verifique os resultados na pasta 'data\\output'")
    print("📋 Logs salvos na pasta 'logs'")

if __name__ == "__main__":
    main() 