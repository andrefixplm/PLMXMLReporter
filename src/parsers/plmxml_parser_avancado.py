# -*- coding: utf-8 -*-
"""
Parser PLMXML Avançado - Versão Completa
Combina funcionalidades dos parsers básico e melhorado com recursos avançados
"""

import xml.etree.ElementTree as ET
import json
import os
import sys
import time
from datetime import datetime
from typing import Dict, List, Optional, Any

# Adiciona o diretório pai ao path para importar módulos locais
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from src.utils.logger import configurar_logger

class PLMXMLParserAvancado:
    def __init__(self, arquivo_log=None, modo_verbose=True):
        """
        Inicializa o parser avançado
        
        Args:
            arquivo_log (str): Caminho para arquivo de log
            modo_verbose (bool): Se deve mostrar logs detalhados
        """
        self.logger = configurar_logger(arquivo_log)
        self.modo_verbose = modo_verbose
        self.logger.info("🚀 Parser PLMXML Avançado inicializado")
        
        # Namespace do PLMXML
        self.namespace = {'plm': 'http://www.plmxml.org/Schemas/PLMXMLSchema'}
        
        # Estatísticas avançadas
        self.stats = {
            'arquivos_processados': 0,
            'itens_extraidos': 0,
            'linhas_bom_extraidas': 0,
            'erros': 0,
            'tempo_processamento': 0,
            'memoria_utilizada': 0,
            'elementos_processados': 0
        }
        
        # Configurações avançadas
        self.config = {
            'max_tamanho_arquivo_mb': 500,
            'timeout_processamento': 300,  # 5 minutos
            'incluir_propriedades_detalhadas': True,
            'incluir_relacionamentos': True,
            'incluir_metadados': True,
            'remover_duplicatas': True
        }
    
    def processar_arquivo_completo(self, caminho_arquivo: str, 
                                  salvar_json: bool = True, 
                                  pasta_saida: str = None,
                                  incluir_estatisticas: bool = True) -> Optional[Dict[str, Any]]:
        """
        Processa um arquivo PLMXML com todas as funcionalidades
        
        Args:
            caminho_arquivo: Caminho para o arquivo PLMXML
            salvar_json: Se deve salvar resultado em JSON
            pasta_saida: Pasta onde salvar os resultados
            incluir_estatisticas: Se deve incluir estatísticas no resultado
        
        Returns:
            Dicionário com dados extraídos ou None se houver erro
        """
        inicio_processamento = time.time()
        self.logger.info(f"🎯 Iniciando processamento completo: {caminho_arquivo}")
        
        # Validações iniciais
        if not self._validar_arquivo_avancado(caminho_arquivo):
            return None
        
        try:
            # Carrega e parseia o XML
            dados = self._parsear_xml_avancado(caminho_arquivo)
            
            if dados:
                # Adiciona estatísticas se solicitado
                if incluir_estatisticas:
                    dados['estatisticas'] = self._gerar_estatisticas_detalhadas(inicio_processamento)
                
                # Atualiza estatísticas globais
                self._atualizar_estatisticas_globais(dados, time.time() - inicio_processamento)
                
                # Salva resultado se solicitado
                if salvar_json:
                    self._salvar_resultado_avancado(dados, caminho_arquivo, pasta_saida)
                
                self.logger.info("✅ Processamento completo concluído com sucesso")
                return dados
            else:
                return None
                
        except Exception as e:
            self.stats['erros'] += 1
            self.logger.error(f"❌ Erro durante processamento completo: {str(e)}")
            return None
    
    def _validar_arquivo_avancado(self, caminho_arquivo: str) -> bool:
        """
        Validação avançada do arquivo
        """
        if not os.path.exists(caminho_arquivo):
            self.logger.error(f"❌ Arquivo não encontrado: {caminho_arquivo}")
            return False
        
        if not os.path.isfile(caminho_arquivo):
            self.logger.error(f"❌ Caminho não é um arquivo: {caminho_arquivo}")
            return False
        
        # Verifica tamanho do arquivo
        tamanho_mb = os.path.getsize(caminho_arquivo) / (1024 * 1024)
        self.logger.info(f"📏 Tamanho do arquivo: {tamanho_mb:.2f} MB")
        
        if tamanho_mb > self.config['max_tamanho_arquivo_mb']:
            self.logger.error(f"❌ Arquivo muito grande: {tamanho_mb:.2f} MB (máximo: {self.config['max_tamanho_arquivo_mb']} MB)")
            return False
        
        # Verifica extensão
        extensao = os.path.splitext(caminho_arquivo)[1].lower()
        if extensao not in ['.xml', '.plmxml']:
            self.logger.warning(f"⚠️  Extensão não reconhecida: {extensao}")
        
        return True
    
    def _parsear_xml_avancado(self, caminho_arquivo: str) -> Optional[Dict[str, Any]]:
        """
        Parsing avançado do XML
        """
        self.logger.info("🔍 Iniciando parsing XML avançado...")
        
        try:
            # Tenta diferentes encodings
            encodings = ['utf-8', 'utf-16', 'latin-1', 'cp1252']
            
            tree = None
            encoding_usado = None
            
            for encoding in encodings:
                try:
                    with open(caminho_arquivo, 'r', encoding=encoding) as f:
                        conteudo = f.read()
                    
                    tree = ET.fromstring(conteudo)
                    encoding_usado = encoding
                    break
                    
                except (UnicodeDecodeError, ET.ParseError):
                    continue
            
            if tree is None:
                # Tenta parsing direto
                tree = ET.parse(caminho_arquivo)
                root = tree.getroot()
            else:
                root = tree
            
            self.logger.info(f"✅ XML parseado com sucesso (encoding: {encoding_usado})")
            self.logger.info(f"📊 Elemento raiz: {root.tag}")
            
            # Extrai informações completas
            dados = {
                'metadados': self._extrair_metadados_avancados(root, caminho_arquivo),
                'itens': self._extrair_itens_avancados(root),
                'bom': self._extrair_bom_avancado(root),
                'relacionamentos': self._extrair_relacionamentos(root),
                'namespaces': self._extrair_namespaces_avancados(root),
                'aplicacao': self._extrair_info_aplicacao(root)
            }
            
            return dados
            
        except ET.ParseError as e:
            self.logger.error(f"❌ Erro de parsing XML: {str(e)}")
            return None
        except Exception as e:
            self.logger.error(f"❌ Erro inesperado no parsing: {str(e)}")
            return None
    
    def _extrair_metadados_avancados(self, root: ET.Element, caminho_arquivo: str) -> Dict[str, Any]:
        """
        Extrai metadados avançados
        """
        metadados = {
            'arquivo': {
                'nome': os.path.basename(caminho_arquivo),
                'caminho_completo': os.path.abspath(caminho_arquivo),
                'tamanho_bytes': os.path.getsize(caminho_arquivo),
                'tamanho_mb': os.path.getsize(caminho_arquivo) / (1024 * 1024),
                'data_modificacao': datetime.fromtimestamp(
                    os.path.getmtime(caminho_arquivo)
                ).isoformat(),
                'data_criacao': datetime.fromtimestamp(
                    os.path.getctime(caminho_arquivo)
                ).isoformat()
            },
            'xml': {
                'elemento_raiz': root.tag,
                'total_elementos': len(list(root.iter())),
                'profundidade_maxima': self._calcular_profundidade_maxima(root),
                'data_processamento': datetime.now().isoformat()
            },
            'estrutura': {
                'tipos_elementos': self._contar_tipos_elementos(root),
                'atributos_unicos': self._extrair_atributos_unicos(root)
            }
        }
        
        return metadados
    
    def _extrair_itens_avancados(self, root: ET.Element) -> List[Dict[str, Any]]:
        """
        Extrai itens com informações avançadas
        """
        self.logger.info("🔍 Extraindo itens avançados...")
        
        itens = []
        ids_processados = set()
        
        # Padrões de busca mais abrangentes
        padroes_item = [
            ('.//plm:ProductRevision', 'ProductRevision'),
            ('.//plm:Product', 'Product'),
            ('.//plm:Part', 'Part'),
            ('.//plm:Item', 'Item'),
            ('.//plm:Design', 'Design'),
            ('.//plm:DesignRevision', 'DesignRevision'),
            ('.//plm:*[@id]', 'ElementoComID')  # Qualquer elemento com ID
        ]
        
        for xpath, tipo_busca in padroes_item:
            try:
                elementos = root.findall(xpath, self.namespace)
                
                if self.modo_verbose:
                    self.logger.info(f"   🔍 Busca '{tipo_busca}': {len(elementos)} elementos encontrados")
                
                for elem in elementos:
                    # Cria ID único para evitar duplicatas
                    id_elemento = elem.get('id', elem.get('itemId', f"{elem.tag}_{len(itens)}"))
                    
                    if id_elemento in ids_processados and self.config['remover_duplicatas']:
                        continue
                    
                    ids_processados.add(id_elemento)
                    
                    item = {
                        'id': id_elemento,
                        'nome': elem.get('name', elem.get('itemId', 'N/A')),
                        'tipo_elemento': elem.tag.replace('{http://www.plmxml.org/Schemas/PLMXMLSchema}', ''),
                        'tipo_busca': tipo_busca,
                        'atributos_basicos': {},
                        'propriedades': {},
                        'relacionamentos': [],
                        'metadados': {}
                    }
                    
                    # Atributos básicos
                    for attr, valor in elem.attrib.items():
                        item['atributos_basicos'][attr] = valor
                    
                    # Propriedades filhas (se habilitado)
                    if self.config['incluir_propriedades_detalhadas']:
                        for child in elem:
                            if any(palavra in child.tag.lower() for palavra in ['property', 'prop', 'attribute', 'attr', 'uservalue']):
                                nome_prop = child.get('title', child.get('name', child.get('propertyName', child.tag)))
                                valor_prop = child.get('value', child.get('propertyValue', child.text or 'N/A'))
                                item['propriedades'][nome_prop] = valor_prop
                    
                    # Metadados do elemento
                    item['metadados'] = {
                        'posicao': len(itens),
                        'tem_filhos': len(list(elem)) > 0,
                        'total_filhos': len(list(elem)),
                        'tem_atributos': len(elem.attrib) > 0
                    }
                    
                    itens.append(item)
                    
            except Exception as e:
                self.logger.warning(f"⚠️  Erro ao processar elementos '{tipo_busca}': {str(e)}")
                continue
        
        self.logger.info(f"✅ Total de itens únicos extraídos: {len(itens)}")
        return itens
    
    def _extrair_bom_avancado(self, root: ET.Element) -> List[Dict[str, Any]]:
        """
        Extrai estrutura BOM com informações avançadas
        """
        self.logger.info("🔍 Extraindo estrutura BOM avançada...")
        
        linhas_bom = []
        
        # Padrões para relações BOM
        padroes_bom = [
            ('.//plm:ProductInstance', 'ProductInstance'),
            ('.//plm:PartInstance', 'PartInstance'),
            ('.//plm:BOMLine', 'BOMLine'),
            ('.//plm:Instance', 'Instance'),
            ('.//plm:Occurrence', 'Occurrence'),
            ('.//plm:*[@parentRef]', 'RelacaoPai'),
            ('.//plm:*[@instancedRef]', 'RelacaoFilho')
        ]
        
        for xpath, tipo_busca in padroes_bom:
            try:
                elementos = root.findall(xpath, self.namespace)
                
                if self.modo_verbose:
                    self.logger.info(f"   🔍 Busca BOM '{tipo_busca}': {len(elementos)} elementos encontrados")
                
                for elem in elementos:
                    linha = {
                        'id': elem.get('id', f"bom_{len(linhas_bom)}"),
                        'pai': elem.get('parentRef', elem.get('partOf', 'N/A')),
                        'filho': elem.get('instancedRef', elem.get('ref', 'N/A')),
                        'quantidade': elem.get('quantity', '1'),
                        'find_number': elem.get('findNumber', 'N/A'),
                        'tipo_elemento': elem.tag.replace('{http://www.plmxml.org/Schemas/PLMXMLSchema}', ''),
                        'tipo_busca': tipo_busca,
                        'atributos': {},
                        'propriedades': {},
                        'metadados': {}
                    }
                    
                    # Todos os atributos
                    for attr, valor in elem.attrib.items():
                        linha['atributos'][attr] = valor
                    
                    # Propriedades filhas
                    if self.config['incluir_propriedades_detalhadas']:
                        for child in elem:
                            if any(palavra in child.tag.lower() for palavra in ['property', 'prop']):
                                nome_prop = child.get('name', child.tag)
                                valor_prop = child.get('value', child.text or 'N/A')
                                linha['propriedades'][nome_prop] = valor_prop
                    
                    # Metadados da linha BOM
                    linha['metadados'] = {
                        'posicao': len(linhas_bom),
                        'tem_filhos': len(list(elem)) > 0,
                        'total_filhos': len(list(elem)),
                        'tem_atributos': len(elem.attrib) > 0
                    }
                    
                    linhas_bom.append(linha)
                    
            except Exception as e:
                self.logger.warning(f"⚠️  Erro ao processar BOM '{tipo_busca}': {str(e)}")
                continue
        
        self.logger.info(f"✅ Total de linhas BOM extraídas: {len(linhas_bom)}")
        return linhas_bom
    
    def _extrair_relacionamentos(self, root: ET.Element) -> List[Dict[str, Any]]:
        """
        Extrai relacionamentos entre elementos
        """
        if not self.config['incluir_relacionamentos']:
            return []
        
        self.logger.info("🔍 Extraindo relacionamentos...")
        
        relacionamentos = []
        
        # Procura por elementos de relacionamento
        padroes_relacao = [
            './/plm:GeneralRelation',
            './/plm:Relation',
            './/plm:*[@relatedRefs]'
        ]
        
        for xpath in padroes_relacao:
            try:
                elementos = root.findall(xpath, self.namespace)
                
                for elem in elementos:
                    relacao = {
                        'id': elem.get('id', f"rel_{len(relacionamentos)}"),
                        'tipo': elem.get('subType', elem.tag),
                        'elementos_relacionados': elem.get('relatedRefs', ''),
                        'atributos': {},
                        'metadados': {}
                    }
                    
                    # Atributos
                    for attr, valor in elem.attrib.items():
                        relacao['atributos'][attr] = valor
                    
                    # Metadados
                    relacao['metadados'] = {
                        'posicao': len(relacionamentos),
                        'tem_filhos': len(list(elem)) > 0
                    }
                    
                    relacionamentos.append(relacao)
                    
            except Exception as e:
                self.logger.warning(f"⚠️  Erro ao processar relacionamentos: {str(e)}")
                continue
        
        self.logger.info(f"✅ Total de relacionamentos extraídos: {len(relacionamentos)}")
        return relacionamentos
    
    def _extrair_namespaces_avancados(self, root: ET.Element) -> Dict[str, str]:
        """
        Extrai namespaces do XML
        """
        namespaces = {}
        
        # Namespaces no elemento raiz
        for prefixo, uri in root.attrib.items():
            if prefixo.startswith('xmlns'):
                if ':' in prefixo:
                    nome_ns = prefixo.split(':')[1]
                else:
                    nome_ns = 'default'
                namespaces[nome_ns] = uri
        
        return namespaces
    
    def _extrair_info_aplicacao(self, root: ET.Element) -> Dict[str, Any]:
        """
        Extrai informações da aplicação (Teamcenter)
        """
        info_aplicacao = {}
        
        # Procura por elementos de aplicação
        for elem in root.iter():
            if 'Application' in elem.tag:
                for attr, valor in elem.attrib.items():
                    info_aplicacao[attr] = valor
                break
        
        return info_aplicacao
    
    def _calcular_profundidade_maxima(self, root: ET.Element) -> int:
        """
        Calcula a profundidade máxima da árvore XML
        """
        def profundidade_recursiva(elem, nivel_atual):
            max_profundidade = nivel_atual
            for child in elem:
                profundidade = profundidade_recursiva(child, nivel_atual + 1)
                max_profundidade = max(max_profundidade, profundidade)
            return max_profundidade
        
        return profundidade_recursiva(root, 0)
    
    def _contar_tipos_elementos(self, root: ET.Element) -> Dict[str, int]:
        """
        Conta tipos de elementos no XML
        """
        tipos = {}
        for elem in root.iter():
            tipo = elem.tag.replace('{http://www.plmxml.org/Schemas/PLMXMLSchema}', '')
            tipos[tipo] = tipos.get(tipo, 0) + 1
        return tipos
    
    def _extrair_atributos_unicos(self, root: ET.Element) -> Dict[str, int]:
        """
        Extrai atributos únicos e suas frequências
        """
        atributos = {}
        for elem in root.iter():
            for attr in elem.attrib:
                atributos[attr] = atributos.get(attr, 0) + 1
        return atributos
    
    def _gerar_estatisticas_detalhadas(self, inicio_processamento: float) -> Dict[str, Any]:
        """
        Gera estatísticas detalhadas do processamento
        """
        tempo_processamento = time.time() - inicio_processamento
        
        return {
            'tempo_processamento_segundos': tempo_processamento,
            'tempo_processamento_formatado': f"{tempo_processamento:.2f}s",
            'memoria_utilizada_mb': self.stats.get('memoria_utilizada', 0),
            'elementos_processados': self.stats.get('elementos_processados', 0),
            'timestamp_inicio': datetime.fromtimestamp(inicio_processamento).isoformat(),
            'timestamp_fim': datetime.now().isoformat()
        }
    
    def _atualizar_estatisticas_globais(self, dados: Dict[str, Any], tempo_processamento: float):
        """
        Atualiza estatísticas globais
        """
        self.stats['arquivos_processados'] += 1
        self.stats['itens_extraidos'] += len(dados.get('itens', []))
        self.stats['linhas_bom_extraidas'] += len(dados.get('bom', []))
        self.stats['tempo_processamento'] += tempo_processamento
        self.stats['elementos_processados'] += dados.get('metadados', {}).get('xml', {}).get('total_elementos', 0)
    
    def _salvar_resultado_avancado(self, dados: Dict[str, Any], arquivo_original: str, pasta_saida: str = None):
        """
        Salva resultado em JSON com nome avançado
        """
        if pasta_saida is None:
            pasta_saida = "data\\output"
        
        # Cria pasta se não existir
        if not os.path.exists(pasta_saida):
            os.makedirs(pasta_saida)
        
        # Nome do arquivo de saída
        nome_base = os.path.splitext(os.path.basename(arquivo_original))[0]
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        nome_saida = f"{nome_base}_avancado_{timestamp}.json"
        caminho_saida = os.path.join(pasta_saida, nome_saida)
        
        try:
            with open(caminho_saida, 'w', encoding='utf-8') as f:
                json.dump(dados, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"💾 Resultado avançado salvo em: {caminho_saida}")
            
        except Exception as e:
            self.logger.error(f"❌ Erro ao salvar resultado avançado: {str(e)}")
    
    def imprimir_estatisticas_avancadas(self):
        """
        Imprime estatísticas avançadas do processamento
        """
        print("\n" + "="*60)
        print("📊 ESTATÍSTICAS AVANÇADAS DO PROCESSAMENTO")
        print("="*60)
        for chave, valor in self.stats.items():
            if chave == 'tempo_processamento':
                print(f"{chave.replace('_', ' ').title()}: {valor:.2f} segundos")
            elif chave == 'memoria_utilizada':
                print(f"{chave.replace('_', ' ').title()}: {valor:.2f} MB")
            else:
                print(f"{chave.replace('_', ' ').title()}: {valor}")
        print("="*60)

# Função de teste avançada
def teste_avancado():
    """
    Teste avançado do parser
    """
    print("🧪 TESTE AVANÇADO DO PARSER PLMXML")
    print("=" * 60)
    
    # Cria pasta de logs se não existir
    if not os.path.exists("logs"):
        os.makedirs("logs")
    
    # Inicializa parser avançado
    parser = PLMXMLParserAvancado(modo_verbose=True)
    
    # Lista arquivos de teste
    pasta_entrada = "data\\input"
    
    if not os.path.exists(pasta_entrada):
        print(f"⚠️  Pasta de entrada não encontrada: {pasta_entrada}")
        return
    
    # Processa todos os arquivos XML/PLMXML na pasta
    arquivos_processados = 0
    
    for arquivo in os.listdir(pasta_entrada):
        if arquivo.lower().endswith(('.xml', '.plmxml')):
            caminho_completo = os.path.join(pasta_entrada, arquivo)
            print(f"\n📂 Processando: {arquivo}")
            
            resultado = parser.processar_arquivo_completo(caminho_completo)
            
            if resultado:
                print(f"✅ {arquivo} processado com sucesso")
                print(f"   📊 Itens: {len(resultado.get('itens', []))}")
                print(f"   📊 BOM: {len(resultado.get('bom', []))}")
                print(f"   📊 Relacionamentos: {len(resultado.get('relacionamentos', []))}")
                arquivos_processados += 1
            else:
                print(f"❌ Erro ao processar {arquivo}")
    
    # Mostra estatísticas finais
    parser.imprimir_estatisticas_avancadas()
    
    if arquivos_processados > 0:
        print(f"\n🎉 TESTE AVANÇADO CONCLUÍDO! {arquivos_processados} arquivo(s) processado(s)")
        print("📄 Verifique os resultados na pasta 'data\\output'")
        print("📋 Logs salvos na pasta 'logs'")
    else:
        print("\n⚠️  Nenhum arquivo foi processado com sucesso")

if __name__ == "__main__":
    teste_avancado() 