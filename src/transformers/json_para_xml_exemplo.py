# -*- coding: utf-8 -*-
"""
Conversor de JSON (resultado do parser) para XML compatível com XSLT
"""

import json
import xml.etree.ElementTree as ET
from xml.dom import minidom
import os
import sys

# Adiciona path para imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from src.utils.logger import configurar_logger

class JSONParaXMLConverter:
    def __init__(self):
        """
        Inicializa o conversor
        """
        self.logger = configurar_logger()
        self.logger.info("Conversor JSON para XML inicializado")
    
    def converter_arquivo_json(self, caminho_json, caminho_xml_saida=None):
        """
        Converte arquivo JSON para XML
        
        Args:
            caminho_json (str): Caminho do arquivo JSON
            caminho_xml_saida (str): Caminho do XML de saída (opcional)
        
        Returns:
            str: Caminho do arquivo XML criado
        """
        self.logger.info(f"Convertendo JSON para XML: {caminho_json}")
        
        # Carrega dados JSON
        try:
            with open(caminho_json, 'r', encoding='utf-8') as f:
                dados = json.load(f)
        except Exception as e:
            self.logger.error(f"Erro ao carregar JSON: {str(e)}")
            return None
        
        # Converte para XML
        xml_root = self._criar_xml_estruturado(dados)
        
        # Define arquivo de saída se não fornecido
        if caminho_xml_saida is None:
            nome_base = os.path.splitext(caminho_json)[0]
            caminho_xml_saida = f"{nome_base}_para_xslt.xml"
        
        # Salva XML
        if self._salvar_xml(xml_root, caminho_xml_saida):
            self.logger.info(f"XML salvo: {caminho_xml_saida}")
            return caminho_xml_saida
        else:
            return None
    
    def _criar_xml_estruturado(self, dados):
        """
        Cria estrutura XML otimizada para XSLT
        """
        # Elemento raiz
        root = ET.Element("TeamcenterData")
        
        # Metadados
        if 'metadados' in dados:
            metadados_elem = ET.SubElement(root, "Metadados")
            self._adicionar_dados_recursivo(metadados_elem, dados['metadados'])
        
        # Itens
        if 'itens' in dados and dados['itens']:
            itens_elem = ET.SubElement(root, "Itens")
            itens_elem.set("total", str(len(dados['itens'])))
            
            for item in dados['itens']:
                item_elem = ET.SubElement(itens_elem, "Item")
                
                # Atributos principais como attributes do XML
                item_elem.set("id", str(item.get('id', 'N/A')))
                item_elem.set("nome", str(item.get('nome', 'N/A')))
                item_elem.set("tipo", str(item.get('tipo_elemento', 'N/A')))
                
                # Atributos básicos
                if 'atributos_basicos' in item:
                    attrs_elem = ET.SubElement(item_elem, "AtributosBasicos")
                    for attr, valor in item['atributos_basicos'].items():
                        attr_elem = ET.SubElement(attrs_elem, "Atributo")
                        attr_elem.set("nome", str(attr))
                        attr_elem.set("valor", str(valor))
                
                # Propriedades
                if 'propriedades' in item:
                    props_elem = ET.SubElement(item_elem, "Propriedades")
                    for prop, valor in item['propriedades'].items():
                        prop_elem = ET.SubElement(props_elem, "Propriedade")
                        prop_elem.set("nome", str(prop))
                        prop_elem.set("valor", str(valor))
        
        # BOM
        if 'bom' in dados and dados['bom']:
            bom_elem = ET.SubElement(root, "EstruturaBOM")
            bom_elem.set("total", str(len(dados['bom'])))
            
            for linha in dados['bom']:
                linha_elem = ET.SubElement(bom_elem, "LinhaBOM")
                
                # Atributos principais
                linha_elem.set("id", str(linha.get('id', 'N/A')))
                linha_elem.set("pai", str(linha.get('pai', 'N/A')))
                linha_elem.set("filho", str(linha.get('filho', 'N/A')))
                linha_elem.set("quantidade", str(linha.get('quantidade', '1')))
                linha_elem.set("findNumber", str(linha.get('find_number', 'N/A')))
                
                # Atributos adicionais
                if 'atributos' in linha:
                    attrs_elem = ET.SubElement(linha_elem, "Atributos")
                    for attr, valor in linha['atributos'].items():
                        attr_elem = ET.SubElement(attrs_elem, "Atributo")
                        attr_elem.set("nome", str(attr))
                        attr_elem.set("valor", str(valor))
        
        # Estatísticas resumo
        resumo_elem = ET.SubElement(root, "Resumo")
        resumo_elem.set("totalItens", str(len(dados.get('itens', []))))
        resumo_elem.set("totalLinhasBOM", str(len(dados.get('bom', []))))
        
        return root
    
    def _adicionar_dados_recursivo(self, parent_elem, dados):
        """
        Adiciona dados de forma recursiva ao XML
        """
        if isinstance(dados, dict):
            for chave, valor in dados.items():
                if isinstance(valor, (dict, list)):
                    sub_elem = ET.SubElement(parent_elem, self._limpar_nome_elemento(chave))
                    self._adicionar_dados_recursivo(sub_elem, valor)
                else:
                    sub_elem = ET.SubElement(parent_elem, self._limpar_nome_elemento(chave))
                    sub_elem.text = str(valor)
        
        elif isinstance(dados, list):
            for i, item in enumerate(dados):
                item_elem = ET.SubElement(parent_elem, "Item")
                item_elem.set("indice", str(i))
                self._adicionar_dados_recursivo(item_elem, item)
    
    def _limpar_nome_elemento(self, nome):
        """
        Limpa nome para ser válido como elemento XML
        """
        # Remove caracteres inválidos e substitui espaços por underscores
        nome_limpo = ''.join(c if c.isalnum() or c == '_' else '_' for c in str(nome))
        
        # Garante que não comece com número
        if nome_limpo and nome_limpo[0].isdigit():
            nome_limpo = 'elem_' + nome_limpo
        
        return nome_limpo or 'elemento'
    
    def _salvar_xml(self, root, caminho_saida):
        """
        Salva XML formatado
        """
        try:
            # Cria pasta se não existir
            pasta = os.path.dirname(caminho_saida)
            if pasta and not os.path.exists(pasta):
                os.makedirs(pasta)
            
            # Converte para string formatada
            rough_string = ET.tostring(root, encoding='utf-8')
            reparsed = minidom.parseString(rough_string)
            pretty_xml = reparsed.toprettyxml(indent="  ", encoding='utf-8')
            
            # Salva arquivo
            with open(caminho_saida, 'wb') as f:
                f.write(pretty_xml)
            
            return True
            
        except Exception as e:
            self.logger.error(f"Erro ao salvar XML: {str(e)}")
            return False

# Função de teste
def teste_conversao():
    """
    Teste da conversão JSON para XML
    """
    print("🧪 TESTE DE CONVERSÃO JSON PARA XML")
    print("=" * 50)
    
    conversor = JSONParaXMLConverter()
    
    # Procura arquivos JSON na pasta de saída
    pasta_output = "data\\output"
    
    if not os.path.exists(pasta_output):
        print(f"❌ Pasta não encontrada: {pasta_output}")
        print("   Execute primeiro o parser para gerar arquivos JSON")
        return
    
    arquivos_json = [f for f in os.listdir(pasta_output) if f.endswith('.json')]
    
    if not arquivos_json:
        print("❌ Nenhum arquivo JSON encontrado")
        print("   Execute primeiro o parser para gerar arquivos JSON")
        return
    
    print(f"📂 Encontrados {len(arquivos_json)} arquivo(s) JSON")
    
    for arquivo_json in arquivos_json:
        caminho_json = os.path.join(pasta_output, arquivo_json)
        print(f"\n🔄 Convertendo: {arquivo_json}")
        
        resultado = conversor.converter_arquivo_json(caminho_json)
        
        if resultado:
            print(f"✅ XML criado: {os.path.basename(resultado)}")
        else:
            print(f"❌ Erro na conversão de {arquivo_json}")
    
    print("\n🎉 CONVERSÃO CONCLUÍDA!")

if __name__ == "__main__":
    teste_conversao()