# -*- coding: utf-8 -*-
"""
Parser Básico para PLMXML - Versão Melhorada
Este arquivo lê um arquivo PLMXML e extrai informações básicas com logs e tratamento de erros
"""

import xml.etree.ElementTree as ET
import json
import os
import sys
from datetime import datetime

# Adiciona o diretório pai ao path para importar módulos locais
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from src.utils.logger import configurar_logger

class PLMXMLParserBasico:
    def __init__(self, arquivo_log=None):
        """
        Inicializa o parser com sistema de logs
        """
        self.logger = configurar_logger(arquivo_log)
        self.logger.info("✅ Parser PLMXML inicializado")
        
        # Namespace do PLMXML
        self.namespace = {'plm': 'http://www.plmxml.org/Schemas/PLMXMLSchema'}
        
        # Estatísticas
        self.stats = {
            'arquivos_processados': 0,
            'itens_extraidos': 0,
            'linhas_bom_extraidas': 0,
            'erros': 0,
            'tempo_processamento': 0
        }
    
    def ler_arquivo_plmxml(self, caminho_arquivo):
        """
        Lê o arquivo PLMXML e retorna informações básicas
        
        Args:
            caminho_arquivo (str): Caminho completo para o arquivo PLMXML
        
        Returns:
            dict: Dicionário com os dados extraídos
        """
        inicio_processamento = datetime.now()
        self.logger.info(f"📂 Iniciando processamento: {caminho_arquivo}")
        
        # Validações iniciais
        if not self._validar_arquivo(caminho_arquivo):
            return None
        
        try:
            # Lê o arquivo XML
            tree = ET.parse(caminho_arquivo)
            root = tree.getroot()
            
            self.logger.info(f"✅ Arquivo lido com sucesso!")
            self.logger.info(f"📊 Elemento raiz: {root.tag}")
            
            # Estrutura para armazenar os dados
            dados_extraidos = {
                'info_arquivo': self._extrair_info_arquivo(caminho_arquivo, root),
                'itens_encontrados': [],
                'estrutura_bom': [],
                'resumo': {},
                'metadados': self._extrair_metadados(root)
            }
            
            # Extrai itens (peças/produtos)
            self.logger.info("🔍 Procurando por itens...")
            itens = self._extrair_itens(root)
            dados_extraidos['itens_encontrados'] = itens
            
            # Extrai estrutura BOM
            self.logger.info("🔍 Procurando por estrutura BOM...")
            bom = self._extrair_bom(root)
            dados_extraidos['estrutura_bom'] = bom
            
            # Cria resumo
            dados_extraidos['resumo'] = {
                'total_itens': len(itens),
                'total_linhas_bom': len(bom),
                'tempo_processamento': (datetime.now() - inicio_processamento).total_seconds()
            }
            
            # Atualiza estatísticas
            self.stats['arquivos_processados'] += 1
            self.stats['itens_extraidos'] += len(itens)
            self.stats['linhas_bom_extraidas'] += len(bom)
            self.stats['tempo_processamento'] += dados_extraidos['resumo']['tempo_processamento']
            
            self.logger.info(f"📊 Resumo: {dados_extraidos['resumo']['total_itens']} itens, {dados_extraidos['resumo']['total_linhas_bom']} linhas BOM")
            
            return dados_extraidos
            
        except ET.ParseError as e:
            self.stats['erros'] += 1
            self.logger.error(f"❌ ERRO de parsing XML: {str(e)}")
            return None
        except Exception as e:
            self.stats['erros'] += 1
            self.logger.error(f"❌ ERRO inesperado ao ler arquivo: {str(e)}")
            return None
    
    def _validar_arquivo(self, caminho_arquivo):
        """
        Valida se o arquivo existe e pode ser lido
        """
        if not os.path.exists(caminho_arquivo):
            self.logger.error(f"❌ ERRO: Arquivo não encontrado: {caminho_arquivo}")
            return False
        
        if not os.path.isfile(caminho_arquivo):
            self.logger.error(f"❌ ERRO: Caminho não é um arquivo: {caminho_arquivo}")
            return False
        
        # Verifica se é XML (extensão)
        extensao = os.path.splitext(caminho_arquivo)[1].lower()
        if extensao not in ['.xml', '.plmxml']:
            self.logger.warning(f"⚠️  Extensão não reconhecida: {extensao}")
        
        # Verifica tamanho do arquivo
        tamanho_mb = os.path.getsize(caminho_arquivo) / (1024 * 1024)
        self.logger.info(f"📏 Tamanho do arquivo: {tamanho_mb:.2f} MB")
        
        if tamanho_mb > 100:  # Arquivo muito grande
            self.logger.warning("⚠️  Arquivo grande detectado - processamento pode ser lento")
        
        return True
    
    def _extrair_info_arquivo(self, caminho_arquivo, root):
        """
        Extrai informações básicas do arquivo
        """
        return {
            'nome_arquivo': os.path.basename(caminho_arquivo),
            'caminho_completo': os.path.abspath(caminho_arquivo),
            'data_processamento': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'elemento_raiz': root.tag,
            'tamanho_bytes': os.path.getsize(caminho_arquivo),
            'data_modificacao': datetime.fromtimestamp(
                os.path.getmtime(caminho_arquivo)
            ).strftime('%Y-%m-%d %H:%M:%S')
        }
    
    def _extrair_metadados(self, root):
        """
        Extrai metadados do XML
        """
        metadados = {
            'namespaces': {},
            'aplicacao': {},
            'total_elementos': len(list(root.iter()))
        }
        
        # Extrai namespaces
        for prefixo, uri in root.attrib.items():
            if prefixo.startswith('xmlns'):
                if ':' in prefixo:
                    nome_ns = prefixo.split(':')[1]
                else:
                    nome_ns = 'default'
                metadados['namespaces'][nome_ns] = uri
        
        # Procura por informações da aplicação (Teamcenter)
        for elem in root.iter():
            if 'Application' in elem.tag:
                for attr, valor in elem.attrib.items():
                    metadados['aplicacao'][attr] = valor
                break
        
        return metadados
    
    def _extrair_itens(self, root):
        """
        Extrai itens/peças do arquivo PLMXML
        """
        itens = []
        ids_processados = set()  # Para evitar duplicatas
        
        # Procura por diferentes tipos de elementos que representam itens
        elementos_item = [
            './/plm:ProductRevision',
            './/plm:Product', 
            './/plm:Part',
            './/plm:Item',
            './/plm:Design',
            './/plm:DesignRevision'
        ]
        
        for elemento_xpath in elementos_item:
            try:
                elementos_encontrados = root.findall(elemento_xpath, self.namespace)
                self.logger.info(f"   🔍 Busca '{elemento_xpath}': {len(elementos_encontrados)} elementos")
                
                for elemento in elementos_encontrados:
                    # Cria ID único para evitar duplicatas
                    id_elemento = elemento.get('id', elemento.get('itemId', f"{elemento.tag}_{len(itens)}"))
                    
                    if id_elemento in ids_processados:
                        continue
                    
                    ids_processados.add(id_elemento)
                    
                    item = {
                        'id': id_elemento,
                        'nome': elemento.get('name', 'N/A'),
                        'tipo': elemento.tag.replace('{http://www.plmxml.org/Schemas/PLMXMLSchema}', ''),
                        'atributos': {},
                        'propriedades': {}
                    }
                    
                    # Extrai todos os atributos do elemento
                    for atributo, valor in elemento.attrib.items():
                        item['atributos'][atributo] = valor
                    
                    # Procura por propriedades filhas
                    for child in elemento:
                        if 'Property' in child.tag or 'UserValue' in child.tag:
                            nome_prop = child.get('title', child.get('name', child.tag))
                            valor_prop = child.get('value', child.text or 'N/A')
                            item['propriedades'][nome_prop] = valor_prop
                    
                    itens.append(item)
                    
            except Exception as e:
                self.logger.warning(f"⚠️  Erro ao processar elementos '{elemento_xpath}': {str(e)}")
                continue
        
        self.logger.info(f"   ✅ Encontrados {len(itens)} itens únicos")
        return itens
    
    def _extrair_bom(self, root):
        """
        Extrai estrutura BOM (Bill of Materials)
        """
        linhas_bom = []
        
        # Procura por elementos que representam relações BOM
        elementos_bom = [
            './/plm:ProductInstance',
            './/plm:PartInstance',
            './/plm:BOMLine',
            './/plm:Instance',
            './/plm:Occurrence'
        ]
        
        for elemento_xpath in elementos_bom:
            try:
                elementos_encontrados = root.findall(elemento_xpath, self.namespace)
                self.logger.info(f"   🔍 Busca BOM '{elemento_xpath}': {len(elementos_encontrados)} elementos")
                
                for elemento in elementos_encontrados:
                    linha_bom = {
                        'id': elemento.get('id', 'N/A'),
                        'pai': elemento.get('parentRef', elemento.get('partOf', 'N/A')),
                        'filho': elemento.get('instancedRef', elemento.get('ref', 'N/A')),
                        'quantidade': elemento.get('quantity', '1'),
                        'numero_find': elemento.get('findNumber', 'N/A'),
                        'tipo': elemento.tag.replace('{http://www.plmxml.org/Schemas/PLMXMLSchema}', ''),
                        'atributos': {},
                        'propriedades': {}
                    }
                    
                    # Extrai todos os atributos
                    for atributo, valor in elemento.attrib.items():
                        linha_bom['atributos'][atributo] = valor
                    
                    # Propriedades filhas
                    for child in elemento:
                        if 'Property' in child.tag or 'UserValue' in child.tag:
                            nome_prop = child.get('title', child.get('name', child.tag))
                            valor_prop = child.get('value', child.text or 'N/A')
                            linha_bom['propriedades'][nome_prop] = valor_prop
                    
                    linhas_bom.append(linha_bom)
                    
            except Exception as e:
                self.logger.warning(f"⚠️  Erro ao processar BOM '{elemento_xpath}': {str(e)}")
                continue
        
        self.logger.info(f"   ✅ Encontradas {len(linhas_bom)} linhas BOM")
        return linhas_bom
    
    def salvar_resultado_json(self, dados, caminho_saida):
        """
        Salva os dados extraídos em formato JSON
        """
        try:
            # Cria pasta se não existir
            pasta_saida = os.path.dirname(caminho_saida)
            if pasta_saida and not os.path.exists(pasta_saida):
                os.makedirs(pasta_saida)
            
            with open(caminho_saida, 'w', encoding='utf-8') as arquivo:
                json.dump(dados, arquivo, indent=2, ensure_ascii=False)
            
            self.logger.info(f"💾 Dados salvos em: {caminho_saida}")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ ERRO ao salvar: {str(e)}")
            return False
    
    def imprimir_estatisticas(self):
        """
        Imprime estatísticas do processamento
        """
        print("\n" + "="*50)
        print("📊 ESTATÍSTICAS DO PROCESSAMENTO")
        print("="*50)
        for chave, valor in self.stats.items():
            if chave == 'tempo_processamento':
                print(f"{chave.replace('_', ' ').title()}: {valor:.2f} segundos")
            else:
                print(f"{chave.replace('_', ' ').title()}: {valor}")
        print("="*50)

# Função de teste melhorada
def testar_parser():
    """
    Função para testar o parser com logs
    """
    print("🧪 INICIANDO TESTE DO PARSER MELHORADO")
    print("=" * 50)
    
    # Cria pasta de logs se não existir
    if not os.path.exists("logs"):
        os.makedirs("logs")
    
    parser = PLMXMLParserBasico()
    
    # SUBSTITUA este caminho pelo caminho do seu arquivo PLMXML
    arquivo_teste = r"data\input\meu_arquivo.plmxml"
    
    # Se não tiver um arquivo real, cria um exemplo
    if not os.path.exists(arquivo_teste):
        parser.logger.warning("⚠️  Arquivo de teste não encontrado.")
        parser.logger.info("   Coloque um arquivo PLMXML na pasta 'data\\input\\'")
        parser.logger.info("   Ou modifique a variável 'arquivo_teste' com o caminho correto")
        return
    
    # Processa o arquivo
    resultado = parser.ler_arquivo_plmxml(arquivo_teste)
    
    if resultado:
        # Salva o resultado
        arquivo_saida = "data\\output\\resultado_parser_basico.json"
        parser.salvar_resultado_json(resultado, arquivo_saida)
        
        # Mostra estatísticas
        parser.imprimir_estatisticas()
        
        print("\n🎉 TESTE CONCLUÍDO COM SUCESSO!")
        print(f"📄 Verifique o arquivo: {arquivo_saida}")
        print("📋 Logs salvos na pasta 'logs'")
    else:
        print("\n❌ TESTE FALHOU!")
        parser.imprimir_estatisticas()

if __name__ == "__main__":
    testar_parser()