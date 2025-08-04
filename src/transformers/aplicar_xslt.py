# -*- coding: utf-8 -*-
"""
Aplicador de Transformações XSLT
Converte arquivos XML em relatórios HTML usando XSLT
"""

import os
import sys
import subprocess
from datetime import datetime

# Adiciona path para imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from src.utils.logger import configurar_logger

class XSLTProcessor:
    def __init__(self):
        """
        Inicializa o processador XSLT
        """
        self.logger = configurar_logger()
        self.logger.info("Processador XSLT inicializado")
    
    def aplicar_xslt(self, arquivo_xml, arquivo_xslt, arquivo_saida=None):
        """
        Aplica transformação XSLT em um arquivo XML
        
        Args:
            arquivo_xml (str): Caminho do arquivo XML
            arquivo_xslt (str): Caminho do arquivo XSLT
            arquivo_saida (str): Caminho do arquivo de saída (opcional)
        
        Returns:
            str: Caminho do arquivo HTML gerado
        """
        self.logger.info(f"Aplicando XSLT: {arquivo_xml} -> {arquivo_xslt}")
        
        # Verifica se os arquivos existem
        if not os.path.exists(arquivo_xml):
            self.logger.error(f"Arquivo XML não encontrado: {arquivo_xml}")
            return None
        
        if not os.path.exists(arquivo_xslt):
            self.logger.error(f"Arquivo XSLT não encontrado: {arquivo_xslt}")
            return None
        
        # Define arquivo de saída se não fornecido
        if arquivo_saida is None:
            nome_base = os.path.splitext(arquivo_xml)[0]
            arquivo_saida = f"{nome_base}_relatorio.html"
        
        try:
            # Tenta usar xsltproc (Linux/Mac)
            resultado = self._usar_xsltproc(arquivo_xml, arquivo_xslt, arquivo_saida)
            if resultado:
                return arquivo_saida
            
            # Se xsltproc falhar, tenta usar saxon (Java)
            resultado = self._usar_saxon(arquivo_xml, arquivo_xslt, arquivo_saida)
            if resultado:
                return arquivo_saida
            
            # Se ambos falharem, usa método Python
            resultado = self._usar_python_xslt(arquivo_xml, arquivo_xslt, arquivo_saida)
            if resultado:
                return arquivo_saida
            
            self.logger.error("Nenhum método XSLT funcionou")
            return None
            
        except Exception as e:
            self.logger.error(f"Erro ao aplicar XSLT: {str(e)}")
            return None
    
    def _usar_xsltproc(self, xml_file, xslt_file, output_file):
        """
        Usa xsltproc para transformação XSLT
        """
        try:
            cmd = ['xsltproc', xslt_file, xml_file]
            with open(output_file, 'w', encoding='utf-8') as f:
                result = subprocess.run(cmd, stdout=f, stderr=subprocess.PIPE, text=True)
            
            if result.returncode == 0:
                self.logger.info(f"XSLT aplicado com xsltproc: {output_file}")
                return True
            else:
                self.logger.warning(f"xsltproc falhou: {result.stderr}")
                return False
                
        except FileNotFoundError:
            self.logger.info("xsltproc não encontrado, tentando outros métodos")
            return False
        except Exception as e:
            self.logger.warning(f"Erro com xsltproc: {str(e)}")
            return False
    
    def _usar_saxon(self, xml_file, xslt_file, output_file):
        """
        Usa Saxon para transformação XSLT
        """
        try:
            cmd = ['java', '-jar', 'saxon-he.jar', xml_file, xslt_file, f'-o:{output_file}']
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                self.logger.info(f"XSLT aplicado com Saxon: {output_file}")
                return True
            else:
                self.logger.warning(f"Saxon falhou: {result.stderr}")
                return False
                
        except FileNotFoundError:
            self.logger.info("Saxon não encontrado, tentando método Python")
            return False
        except Exception as e:
            self.logger.warning(f"Erro com Saxon: {str(e)}")
            return False
    
    def _usar_python_xslt(self, xml_file, xslt_file, output_file):
        """
        Usa lxml para transformação XSLT em Python
        """
        try:
            from lxml import etree
            
            # Carrega XML e XSLT
            xml_doc = etree.parse(xml_file)
            xslt_doc = etree.parse(xslt_file)
            
            # Aplica transformação
            transform = etree.XSLT(xslt_doc)
            result = transform(xml_doc)
            
            # Salva resultado
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(str(result))
            
            self.logger.info(f"XSLT aplicado com lxml: {output_file}")
            return True
            
        except ImportError:
            self.logger.warning("lxml não instalado, criando HTML básico")
            return self._criar_html_basico(xml_file, output_file)
        except Exception as e:
            self.logger.warning(f"Erro com lxml: {str(e)}")
            return self._criar_html_basico(xml_file, output_file)
    
    def _criar_html_basico(self, xml_file, output_file):
        """
        Cria HTML básico quando XSLT não está disponível
        """
        try:
            import xml.etree.ElementTree as ET
            
            # Carrega XML
            tree = ET.parse(xml_file)
            root = tree.getroot()
            
            # Cria HTML básico
            html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Relatório PLMXML - Fallback</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .header {{ background-color: #2c3e50; color: white; padding: 20px; }}
        .content {{ margin: 20px 0; }}
        table {{ border-collapse: collapse; width: 100%; }}
        th, td {{ border: 1px solid #ddd; padding: 8px; }}
        th {{ background-color: #f2f2f2; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>📊 Relatório PLMXML - Fallback</h1>
        <p>Relatório básico gerado sem XSLT</p>
    </div>
    
    <div class="content">
        <h2>📋 Informações do Arquivo</h2>
        <p><strong>Arquivo XML:</strong> {os.path.basename(xml_file)}</p>
        <p><strong>Data de geração:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        <p><strong>Elemento raiz:</strong> {root.tag}</p>
        
        <h2>📦 Estrutura XML</h2>
        <p>Este é um relatório básico. Para relatórios completos, instale lxml ou xsltproc.</p>
        
        <h3>Elementos encontrados:</h3>
        <ul>
"""
            
            # Lista elementos únicos
            elementos = set()
            for elem in root.iter():
                elementos.add(elem.tag)
            
            for elem in sorted(elementos):
                html_content += f"            <li>{elem}</li>\n"
            
            html_content += """
        </ul>
    </div>
</body>
</html>
"""
            
            # Salva HTML
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            self.logger.info(f"HTML básico criado: {output_file}")
            return True
            
        except Exception as e:
            self.logger.error(f"Erro ao criar HTML básico: {str(e)}")
            return False

# Função de teste
def teste_xslt():
    """
    Teste da aplicação de XSLT
    """
    print("🧪 TESTE DE APLICAÇÃO XSLT")
    print("=" * 50)
    
    processador = XSLTProcessor()
    
    # Procura arquivos XML na pasta de saída
    pasta_output = "data\\output"
    pasta_xslt = "templates\\xslt"
    
    if not os.path.exists(pasta_output):
        print(f"❌ Pasta não encontrada: {pasta_output}")
        print("   Execute primeiro o conversor JSON para XML")
        return
    
    if not os.path.exists(pasta_xslt):
        print(f"❌ Pasta XSLT não encontrada: {pasta_xslt}")
        return
    
    # Lista arquivos XML
    arquivos_xml = [f for f in os.listdir(pasta_output) if f.endswith('_para_xslt.xml')]
    
    if not arquivos_xml:
        print("❌ Nenhum arquivo XML encontrado")
        print("   Execute primeiro o conversor JSON para XML")
        return
    
    # Lista arquivos XSLT
    arquivos_xslt = [f for f in os.listdir(pasta_xslt) if f.endswith('.xslt')]
    
    if not arquivos_xslt:
        print("❌ Nenhum arquivo XSLT encontrado")
        return
    
    print(f"📂 Encontrados {len(arquivos_xml)} arquivo(s) XML")
    print(f"📂 Encontrados {len(arquivos_xslt)} arquivo(s) XSLT")
    
    # Aplica XSLT em cada arquivo XML
    for arquivo_xml in arquivos_xml:
        caminho_xml = os.path.join(pasta_output, arquivo_xml)
        print(f"\n🔄 Processando: {arquivo_xml}")
        
        for arquivo_xslt in arquivos_xslt:
            caminho_xslt = os.path.join(pasta_xslt, arquivo_xslt)
            print(f"   📄 Aplicando: {arquivo_xslt}")
            
            resultado = processador.aplicar_xslt(caminho_xml, caminho_xslt)
            
            if resultado:
                print(f"   ✅ HTML criado: {os.path.basename(resultado)}")
            else:
                print(f"   ❌ Erro na transformação com {arquivo_xslt}")
    
    print("\n🎉 TRANSFORMAÇÃO XSLT CONCLUÍDA!")

if __name__ == "__main__":
    teste_xslt() 