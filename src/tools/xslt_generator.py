# -*- coding: utf-8 -*-
"""
Gerador de Código XSLT para PLMXML
Gera automaticamente código XSLT baseado na estrutura PLMXML
"""

import os
import sys
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from datetime import datetime
import xml.etree.ElementTree as ET
import re

# Adiciona path para imports
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from src.utils.logger import configurar_logger

class XSLTGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("📝 Gerador de Código XSLT - PLMXML")
        self.root.geometry("1400x900")
        self.root.configure(bg='#f0f0f0')
        
        # Configuração do logger
        self.logger = configurar_logger()
        
        # Variáveis de controle
        self.arquivo_plmxml = None
        self.campos_encontrados = []
        self.namespace_plm = {'plm': 'http://www.plmxml.org/Schemas/PLMXMLSchema'}
        
        self.criar_interface()
        
    def criar_interface(self):
        """Cria a interface gráfica principal"""
        
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configuração do grid
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # Título da aplicação
        titulo_frame = ttk.Frame(main_frame)
        titulo_frame.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Título da aplicação
        titulo = ttk.Label(titulo_frame, text="📝 Gerador de Código XSLT - PLMXML", 
                          font=('Arial', 16, 'bold'))
        titulo.grid(row=0, column=0, pady=(0, 5))
        
        # Informações da empresa
        empresa_info = ttk.Label(titulo_frame, text="SmartPLM - Soluções Inteligentes em PLM", 
                               font=('Arial', 10, 'italic'), foreground='#666666')
        empresa_info.grid(row=1, column=0, pady=(0, 5))
        
        # Desenvolvedor
        dev_info = ttk.Label(titulo_frame, text="Desenvolvido por André Luiz", 
                           font=('Arial', 9), foreground='#888888')
        dev_info.grid(row=2, column=0)
        
        # Frame de seleção de arquivo
        self.criar_frame_selecao(main_frame)
        
        # Frame de busca e geração
        self.criar_frame_busca(main_frame)
        
        # Frame de resultados
        self.criar_frame_resultados(main_frame)
        
    def criar_frame_selecao(self, parent):
        """Cria frame para seleção de arquivo"""
        frame = ttk.LabelFrame(parent, text="📁 Seleção de Arquivo PLMXML", padding="10")
        frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        frame.columnconfigure(1, weight=1)
        
        # Botão selecionar arquivo
        btn_selecionar = ttk.Button(frame, text="Selecionar Arquivo PLMXML", 
                                   command=self.selecionar_arquivo)
        btn_selecionar.grid(row=0, column=0, padx=(0, 10))
        
        # Label do arquivo selecionado
        self.lbl_arquivo = ttk.Label(frame, text="Nenhum arquivo selecionado")
        self.lbl_arquivo.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(10, 0))
        
        # Botão extrair campos
        self.btn_extrair = ttk.Button(frame, text="🔍 Extrair Campos", 
                                     command=self.extrair_campos, state=tk.DISABLED)
        self.btn_extrair.grid(row=0, column=2, padx=(10, 0))
        
    def criar_frame_busca(self, parent):
        """Cria frame para busca e geração de código"""
        frame = ttk.LabelFrame(parent, text="🔎 Busca e Geração de Código XSLT", padding="10")
        frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Campo de busca
        ttk.Label(frame, text="Buscar campo:").grid(row=0, column=0, sticky=tk.W)
        self.entry_busca = ttk.Entry(frame, width=40)
        self.entry_busca.grid(row=0, column=1, padx=(10, 10), sticky=tk.W)
        self.entry_busca.bind('<Return>', lambda e: self.buscar_e_gerar())
        
        # Botão buscar e gerar
        btn_buscar = ttk.Button(frame, text="🔍 Buscar e Gerar XSLT", command=self.buscar_e_gerar)
        btn_buscar.grid(row=0, column=2, padx=(0, 10))
        
        # Botão mostrar todos os campos
        btn_todos = ttk.Button(frame, text="📋 Mostrar Todos os Campos", command=self.mostrar_todos_campos)
        btn_todos.grid(row=0, column=2, padx=(0, 5))
        
        # Botão mostrar apenas campos wt9_
        btn_wt9 = ttk.Button(frame, text="🎯 Apenas Campos wt9_", command=self.mostrar_campos_wt9)
        btn_wt9.grid(row=0, column=3, padx=(0, 5))
        
        # Botão gerar HTML completo
        btn_html = ttk.Button(frame, text="🌐 Gerar HTML Completo", command=self.gerar_html_completo)
        btn_html.grid(row=0, column=4)
        
    def criar_frame_resultados(self, parent):
        """Cria frame para exibição de resultados"""
        frame = ttk.LabelFrame(parent, text="📊 Resultados", padding="10")
        frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S))
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(1, weight=1)
        
        # Notebook para abas
        self.notebook = ttk.Notebook(frame)
        self.notebook.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Aba de campos encontrados
        self.criar_aba_campos()
        
        # Aba de código XSLT
        self.criar_aba_xslt()
        
        # Aba de estrutura PLMXML
        self.criar_aba_estrutura()
        
    def criar_aba_campos(self):
        """Cria aba para campos encontrados"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="📋 Campos Encontrados")
        
        # Lista de campos
        self.lista_campos = tk.Listbox(frame, height=15)
        self.lista_campos.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.lista_campos.bind('<Double-Button-1>', self.selecionar_campo_da_lista)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=self.lista_campos.yview)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.lista_campos.configure(yscrollcommand=scrollbar.set)
        
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(0, weight=1)
        
    def criar_aba_xslt(self):
        """Cria aba para código XSLT gerado"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="📝 Código XSLT")
        
        # Área de texto para código XSLT
        self.texto_xslt = scrolledtext.ScrolledText(frame, height=20, width=100)
        self.texto_xslt.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Botões
        btn_frame = ttk.Frame(frame)
        btn_frame.grid(row=1, column=0, pady=(5, 0))
        
        btn_copiar = ttk.Button(btn_frame, text="📋 Copiar Código", command=self.copiar_codigo)
        btn_copiar.grid(row=0, column=0, padx=(0, 5))
        
        btn_salvar = ttk.Button(btn_frame, text="💾 Salvar Arquivo", command=self.salvar_codigo)
        btn_salvar.grid(row=0, column=1, padx=(0, 5))
        
        btn_limpar = ttk.Button(btn_frame, text="🗑️ Limpar", command=self.limpar_codigo)
        btn_limpar.grid(row=0, column=2, padx=(0, 5))
        
        btn_salvar_html = ttk.Button(btn_frame, text="🌐 Salvar HTML", command=self.salvar_html)
        btn_salvar_html.grid(row=0, column=3)
        
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(0, weight=1)
        
    def criar_aba_estrutura(self):
        """Cria aba para visualização da estrutura PLMXML"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="🌳 Estrutura PLMXML")
        
        # Treeview para estrutura
        self.tree_estrutura = ttk.Treeview(frame, columns=('tipo', 'valor'), show='tree headings')
        self.tree_estrutura.heading('#0', text='Elemento')
        self.tree_estrutura.heading('tipo', text='Tipo')
        self.tree_estrutura.heading('valor', text='Valor/Atributo')
        
        # Scrollbars
        scrollbar_v = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=self.tree_estrutura.yview)
        scrollbar_h = ttk.Scrollbar(frame, orient=tk.HORIZONTAL, command=self.tree_estrutura.xview)
        self.tree_estrutura.configure(yscrollcommand=scrollbar_v.set, xscrollcommand=scrollbar_h.set)
        
        # Layout
        self.tree_estrutura.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar_v.grid(row=0, column=1, sticky=(tk.N, tk.S))
        scrollbar_h.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(0, weight=1)
        
    def selecionar_arquivo(self):
        """Seleciona arquivo PLMXML"""
        arquivo = filedialog.askopenfilename(
            title="Selecionar Arquivo PLMXML",
            filetypes=[("Arquivos PLMXML", "*.xml *.plmxml"), ("Todos os arquivos", "*.*")]
        )
        
        if arquivo:
            self.arquivo_plmxml = arquivo
            self.lbl_arquivo.config(text=os.path.basename(arquivo))
            self.btn_extrair.config(state=tk.NORMAL)
            self.log(f"📁 Arquivo selecionado: {os.path.basename(arquivo)}")
            
    def extrair_campos(self):
        """Extrai todos os campos do arquivo PLMXML"""
        if not self.arquivo_plmxml:
            messagebox.showwarning("Aviso", "Selecione um arquivo PLMXML primeiro!")
            return
            
        try:
            self.log("🔍 Extraindo campos do arquivo PLMXML...")
            
            # Parse do XML
            tree = ET.parse(self.arquivo_plmxml)
            root = tree.getroot()
            
            # Extrai campos
            self.campos_encontrados = self.extrair_campos_plmxml(root)
            
            # Popula lista de campos
            self.popular_lista_campos()
            
            # Popula estrutura
            self.popular_estrutura(root)
            
            self.log(f"✅ Extraídos {len(self.campos_encontrados)} campos")
            
        except Exception as e:
            self.log(f"❌ Erro ao extrair campos: {str(e)}")
            messagebox.showerror("Erro", f"Erro ao extrair campos: {str(e)}")
            
    def extrair_campos_plmxml(self, root):
        """Extrai campos específicos do PLMXML"""
        campos = []
        
        # Busca por UserValue (campos personalizados)
        for user_value in root.findall('.//plm:UserValue', self.namespace_plm):
            title = user_value.get('title', '')
            value = user_value.get('value', '')
            if title:
                # Verifica se é um campo wt9_ (padrão do usuário)
                is_wt9_field = title.startswith('wt9_')
                campos.append({
                    'tipo': 'UserValue',
                    'nome': title,
                    'valor': value,
                    'caminho': self.obter_caminho_xpath(user_value),
                    'elemento': user_value,
                    'is_wt9': is_wt9_field
                })
                
        # Busca por outros elementos com atributos
        for elem in root.iter():
            for attr_name, attr_value in elem.attrib.items():
                if attr_name in ['name', 'title', 'id', 'value']:
                    campos.append({
                        'tipo': 'Atributo',
                        'nome': f"{elem.tag}/{attr_name}",
                        'valor': attr_value,
                        'caminho': self.obter_caminho_xpath(elem),
                        'elemento': elem
                    })
                    
        return campos
        
    def obter_caminho_xpath(self, elemento):
        """Obtém caminho XPath de um elemento"""
        caminho = []
        while elemento is not None:
            if elemento.tag:
                # Remove namespace se presente
                tag = elemento.tag.split('}')[-1] if '}' in elemento.tag else elemento.tag
                caminho.append(tag)
            elemento = elemento.getparent() if hasattr(elemento, 'getparent') else None
            
        return "/" + "/".join(reversed(caminho))
        
    def popular_lista_campos(self):
        """Popula a lista de campos encontrados"""
        self.lista_campos.delete(0, tk.END)
        
        for campo in self.campos_encontrados:
            # Destaca campos wt9_ com ícone especial
            if campo.get('is_wt9', False):
                self.lista_campos.insert(tk.END, f"🎯 {campo['tipo']}: {campo['nome']} = '{campo['valor']}'")
            else:
                self.lista_campos.insert(tk.END, f"{campo['tipo']}: {campo['nome']} = '{campo['valor']}'")
            
    def popular_estrutura(self, root):
        """Popula a estrutura PLMXML no treeview"""
        # Limpa treeview
        for item in self.tree_estrutura.get_children():
            self.tree_estrutura.delete(item)
            
        # Adiciona elementos
        self.adicionar_elemento_estrutura("", root)
        
    def adicionar_elemento_estrutura(self, parent, elemento):
        """Adiciona elemento à estrutura"""
        # Remove namespace se presente
        tag = elemento.tag.split('}')[-1] if '}' in elemento.tag else elemento.tag
        
        # Prepara atributos
        atributos = ", ".join([f"{k}='{v}'" for k, v in elemento.attrib.items()])
        
        # Cria item
        item = self.tree_estrutura.insert(parent, 'end', text=tag, 
                                        values=('Elemento', atributos))
        
        # Adiciona texto se houver
        if elemento.text and elemento.text.strip():
            self.tree_estrutura.insert(item, 'end', text=f"Texto: {elemento.text.strip()}", 
                                     values=('Texto', ''))
            
        # Adiciona filhos
        for filho in elemento:
            self.adicionar_elemento_estrutura(item, filho)
            
    def buscar_e_gerar(self):
        """Busca um campo e gera código XSLT"""
        termo = self.entry_busca.get().strip()
        if not termo:
            messagebox.showwarning("Aviso", "Digite um termo para buscar!")
            return
            
        self.log(f"🔍 Buscando por: {termo}")
        
        # Busca campos que correspondem ao termo
        campos_encontrados = []
        for campo in self.campos_encontrados:
            if termo.lower() in campo['nome'].lower() or termo.lower() in campo['valor'].lower():
                campos_encontrados.append(campo)
                
        if campos_encontrados:
            # Gera código XSLT
            codigo_xslt = self.gerar_codigo_xslt_para_campos(campos_encontrados)
            
            # Exibe código
            self.texto_xslt.delete(1.0, tk.END)
            self.texto_xslt.insert(1.0, codigo_xslt)
            
            self.log(f"✅ Encontrados {len(campos_encontrados)} campos, código XSLT gerado")
        else:
            self.log(f"❌ Nenhum campo encontrado para '{termo}'")
            messagebox.showinfo("Info", f"Nenhum campo encontrado para '{termo}'")
            
    def gerar_codigo_xslt_para_campos(self, campos):
        """Gera código XSLT para os campos especificados"""
        codigo = "<!-- Código XSLT Gerado Automaticamente -->\n"
        codigo += "<!-- Baseado na estrutura PLMXML -->\n\n"
        
        for i, campo in enumerate(campos):
            codigo += f"<!-- Campo {i+1}: {campo['nome']} -->\n"
            
            if campo['tipo'] == 'UserValue':
                # Gera código para UserValue
                if campo.get('is_wt9', False):
                    codigo += self.gerar_codigo_wt9_field(campo)
                else:
                    codigo += self.gerar_codigo_user_value(campo)
            else:
                # Gera código para atributos gerais
                codigo += self.gerar_codigo_atributo(campo)
                
            codigo += "\n"
            
        return codigo
        
    def gerar_codigo_user_value(self, campo):
        """Gera código XSLT para UserValue baseado no padrão do usuário"""
        nome_campo = campo['nome']
        
        codigo = f"""<!-- Para campo UserValue: {nome_campo} -->
<xsl:value-of select="$rootProductRevision/plm:UserData/plm:UserValue[@title='{nome_campo}']/@value"/>

<!-- Alternativas baseadas no seu padrão: -->
<xsl:value-of select="$frascoDesign/plm:UserData/plm:UserValue[@title='{nome_campo}']/@value"/>
<xsl:value-of select="$rootMasterForm/plm:UserData/plm:UserValue[@title='{nome_campo}']/@value"/>
<xsl:value-of select="//plm:UserValue[@title='{nome_campo}']/@value"/>

<!-- Para uso em condições (como no seu XSL): -->
<xsl:when test="$rootProductRevision/plm:UserData/plm:UserValue[@title='{nome_campo}']/@value != ''">
    <xsl:value-of select="$rootProductRevision/plm:UserData/plm:UserValue[@title='{nome_campo}']/@value"/>
</xsl:when>"""
        
        return codigo
        
    def gerar_codigo_wt9_field(self, campo):
        """Gera código XSLT específico para campos wt9_ baseado no padrão do usuário"""
        nome_campo = campo['nome']
        
        codigo = f"""<!-- Campo wt9_: {nome_campo} -->
<!-- Uso direto: -->
<xsl:value-of select="$rootProductRevision/plm:UserData/plm:UserValue[@title='{nome_campo}']/@value"/>

<!-- Uso em condições (como no seu XSL): -->
<xsl:choose>
    <xsl:when test="$rootProductRevision/plm:UserData/plm:UserValue[@title='{nome_campo}']/@value != ''">
        <xsl:value-of select="$rootProductRevision/plm:UserData/plm:UserValue[@title='{nome_campo}']/@value"/>
    </xsl:when>
    <xsl:otherwise>Valor padrão</xsl:otherwise>
</xsl:choose>

<!-- Alternativas para diferentes contextos: -->
<xsl:value-of select="$frascoDesign/plm:UserData/plm:UserValue[@title='{nome_campo}']/@value"/>
<xsl:value-of select="$rootMasterForm/plm:UserData/plm:UserValue[@title='{nome_campo}']/@value"/>"""
        
        return codigo
        
    def gerar_codigo_atributo(self, campo):
        """Gera código XSLT para atributos gerais"""
        caminho = campo['caminho']
        nome_atributo = campo['nome'].split('/')[-1]
        
        codigo = f"""<!-- Para atributo: {campo['nome']} -->
<xsl:value-of select="{caminho}/@{nome_atributo}"/>

<!-- Alternativas: -->
<xsl:value-of select="//*[@title='{nome_atributo}']"/>
<xsl:value-of select="//*[@name='{nome_atributo}']"/>"""
        
        return codigo
        
    def mostrar_todos_campos(self):
        """Mostra todos os campos e gera código XSLT"""
        if not self.campos_encontrados:
            messagebox.showwarning("Aviso", "Extraia os campos primeiro!")
            return
            
        # Gera código para todos os campos
        codigo_xslt = self.gerar_codigo_xslt_para_campos(self.campos_encontrados)
        
        # Exibe código
        self.texto_xslt.delete(1.0, tk.END)
        self.texto_xslt.insert(1.0, codigo_xslt)
        
        self.log(f"✅ Gerado código XSLT para todos os {len(self.campos_encontrados)} campos")
        
    def mostrar_campos_wt9(self):
        """Mostra apenas campos wt9_ e gera código XSLT"""
        if not self.campos_encontrados:
            messagebox.showwarning("Aviso", "Extraia os campos primeiro!")
            return
            
        # Filtra apenas campos wt9_
        campos_wt9 = [campo for campo in self.campos_encontrados if campo.get('is_wt9', False)]
        
        if not campos_wt9:
            messagebox.showinfo("Info", "Nenhum campo wt9_ encontrado!")
            return
            
        # Gera código para campos wt9_
        codigo_xslt = self.gerar_codigo_xslt_para_campos(campos_wt9)
        
        # Exibe código
        self.texto_xslt.delete(1.0, tk.END)
        self.texto_xslt.insert(1.0, codigo_xslt)
        
        self.log(f"✅ Gerado código XSLT para {len(campos_wt9)} campos wt9_")
        
    def gerar_html_completo(self):
        """Gera um HTML completo com todos os campos e atributos"""
        if not self.campos_encontrados:
            messagebox.showwarning("Aviso", "Extraia os campos primeiro!")
            return
            
        try:
            self.log("🌐 Gerando HTML completo...")
            
            # Filtra campos wt9_
            campos_wt9 = [campo for campo in self.campos_encontrados if campo.get('is_wt9', False)]
            
            # Gera XSLT completo
            xslt_completo = self.gerar_xslt_completo(campos_wt9)
            
            # Exibe código
            self.texto_xslt.delete(1.0, tk.END)
            self.texto_xslt.insert(1.0, xslt_completo)
            
            self.log(f"✅ HTML completo gerado com {len(campos_wt9)} campos wt9_")
            
        except Exception as e:
            self.log(f"❌ Erro ao gerar HTML: {str(e)}")
            messagebox.showerror("Erro", f"Erro ao gerar HTML: {str(e)}")
            
    def gerar_xslt_completo(self, campos_wt9):
        """Gera XSLT completo para HTML com todos os campos"""
        
        # Cabeçalho do XSLT
        xslt = f"""<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:plm="http://www.plmxml.org/Schemas/PLMXMLSchema"
    exclude-result-prefixes="plm">

    <xsl:output method="html" indent="yes" encoding="UTF-8"/>

    <!-- Parâmetros principais -->
    <xsl:param name="primaryOccRef" select="substring-after(/plm:PLMXML/plm:Header/@traverseRootRefs, '#')"/>
    
    <!-- Keys para acesso rápido aos elementos -->
    <xsl:key name="productById" match="plm:Product" use="@id"/>
    <xsl:key name="productRevisionById" match="plm:ProductRevision" use="@id"/>
    <xsl:key name="designRevisionById" match="plm:DesignRevision" use="@id"/>
    <xsl:key name="formById" match="plm:Form" use="@id"/>
    <xsl:key name="occurrenceById" match="plm:Occurrence" use="@id"/>
    <xsl:key name="siteById" match="plm:Site" use="@id"/>

    <xsl:template match="/">
        <!-- Identificar a ficha de equipamento principal -->
        <xsl:variable name="rootOccurrenceId" select="substring-after(/plm:PLMXML/plm:Header/@traverseRootRefs, '#')"/>
        <xsl:variable name="rootOccurrence" select="key('occurrenceById', $rootOccurrenceId)"/>
        <xsl:variable name="rootProductRevisionId" select="substring-after($rootOccurrence/@instancedRef, '#')"/>
        <xsl:variable name="rootProductRevision" select="key('productRevisionById', $rootProductRevisionId)"/>
        <xsl:variable name="rootProduct" select="key('productById', substring-after($rootProductRevision/@masterRef, '#'))"/>
        <xsl:variable name="rootFormRefId" select="substring-after($rootProductRevision/plm:AssociatedForm[@role='IMAN_master_form']/@formRef, '#')"/>
        <xsl:variable name="rootMasterForm" select="key('formById', $rootFormRefId)"/>
        <xsl:variable name="siteId" select="substring-after($rootProduct/@accessRefs, '#')"/>
        <xsl:variable name="siteElement" select="key('siteById', $siteId)"/>
        
        <!-- Buscar frasco relacionado através das relações -->
        <xsl:variable name="frascoDesign" select="//plm:DesignRevision[@subType='WT9_FrascoRevision'][1]"/>

        <html>
            <head>
                <title>Relatório Completo - <xsl:value-of select="$rootProduct/@productId"/> (<xsl:value-of select="$rootProductRevision/@revision"/>)</title>
                <style>
                    body {{ 
                        font-family: Arial, sans-serif; 
                        font-size: 12pt; 
                        margin: 20px; 
                        background: #f5f5f5;
                    }}
                    
                    .container {{
                        max-width: 1200px;
                        margin: 0 auto;
                        background: white;
                        padding: 20px;
                        border-radius: 8px;
                        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                    }}
                    
                    h1, h2, h3 {{ 
                        color: #333; 
                        border-bottom: 2px solid #007acc;
                        padding-bottom: 10px;
                    }}
                    
                    table {{ 
                        border-collapse: collapse; 
                        width: 100%; 
                        margin: 15px 0; 
                        background: white;
                        border-radius: 5px;
                        overflow: hidden;
                        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
                    }}
                    
                    th, td {{ 
                        border: 1px solid #ddd; 
                        padding: 12px; 
                        text-align: left;
                        vertical-align: top;
                    }}
                    
                    th {{ 
                        background-color: #007acc; 
                        color: white; 
                        font-weight: bold;
                        font-size: 11pt;
                    }}
                    
                    tr:nth-child(even) {{
                        background-color: #f9f9f9;
                    }}
                    
                    tr:hover {{
                        background-color: #f0f0f0;
                    }}
                    
                    .wt9-field {{
                        font-weight: bold;
                        color: #007acc;
                    }}
                    
                    .field-value {{
                        font-family: 'Courier New', monospace;
                        background: #f8f8f8;
                        padding: 4px 8px;
                        border-radius: 3px;
                        border: 1px solid #ddd;
                    }}
                    
                    .section {{
                        margin: 30px 0;
                        padding: 20px;
                        background: white;
                        border-radius: 8px;
                        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
                    }}
                    
                    .info-box {{
                        background: #e8f4fd;
                        border-left: 4px solid #007acc;
                        padding: 15px;
                        margin: 15px 0;
                        border-radius: 5px;
                    }}
                    
                    .stats {{
                        display: flex;
                        justify-content: space-around;
                        margin: 20px 0;
                        flex-wrap: wrap;
                    }}
                    
                    .stat-item {{
                        background: #007acc;
                        color: white;
                        padding: 15px;
                        border-radius: 5px;
                        text-align: center;
                        min-width: 150px;
                        margin: 5px;
                    }}
                    
                    .stat-number {{
                        font-size: 24pt;
                        font-weight: bold;
                    }}
                    
                    .stat-label {{
                        font-size: 10pt;
                        opacity: 0.9;
                    }}
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>📊 Relatório Completo - PLMXML</h1>
                    
                    <!-- Informações básicas -->
                    <div class="info-box">
                        <h3>📋 Informações Gerais</h3>
                        <p><strong>Produto:</strong> <xsl:value-of select="$rootProduct/@productId"/></p>
                        <p><strong>Revisão:</strong> <xsl:value-of select="$rootProductRevision/@revision"/></p>
                        <p><strong>Nome:</strong> <xsl:value-of select="$rootProductRevision/@name"/></p>
                        <p><strong>Data de Geração:</strong> <xsl:value-of select="substring(/plm:PLMXML/@date,1,10)"/></p>
                    </div>
                    
                    <!-- Estatísticas -->
                    <div class="stats">
                        <div class="stat-item">
                            <div class="stat-number">{len(campos_wt9)}</div>
                            <div class="stat-label">Campos wt9_</div>
                        </div>
                        <div class="stat-item">
                            <div class="stat-number">{len(self.campos_encontrados)}</div>
                            <div class="stat-label">Total de Campos</div>
                        </div>
                        <div class="stat-item">
                            <div class="stat-number">{len([c for c in self.campos_encontrados if c['tipo'] == 'UserValue'])}</div>
                            <div class="stat-label">UserValues</div>
                        </div>
                    </div>
                    
                    <!-- Seção de Campos wt9_ -->
                    <div class="section">
                        <h2>🎯 Campos wt9_ Encontrados</h2>
                        <table>
                            <thead>
                                <tr>
                                    <th>Campo</th>
                                    <th>Valor</th>
                                    <th>Código XSLT</th>
                                </tr>
                            </thead>
                            <tbody>"""
        
        # Adiciona cada campo wt9_
        for campo in campos_wt9:
            xslt += f"""
                                <tr>
                                    <td class="wt9-field">{campo['nome']}</td>
                                    <td class="field-value">{campo['valor']}</td>
                                    <td class="field-value">
                                        <xsl:value-of select="$rootProductRevision/plm:UserData/plm:UserValue[@title='{campo['nome']}']/@value"/>
                                    </td>
                                </tr>"""
        
        # Continua o XSLT
        xslt += """
                            </tbody>
                        </table>
                    </div>
                    
                    <!-- Seção de Todos os Campos -->
                    <div class="section">
                        <h2>📋 Todos os Campos Encontrados</h2>
                        <table>
                            <thead>
                                <tr>
                                    <th>Tipo</th>
                                    <th>Campo</th>
                                    <th>Valor</th>
                                    <th>Caminho XPath</th>
                                </tr>
                            </thead>
                            <tbody>"""
        
        # Adiciona todos os campos
        for campo in self.campos_encontrados:
            tipo_icon = "🎯" if campo.get('is_wt9', False) else "📄"
            xslt += f"""
                                <tr>
                                    <td>{tipo_icon} {campo['tipo']}</td>
                                    <td class="wt9-field">{campo['nome']}</td>
                                    <td class="field-value">{campo['valor']}</td>
                                    <td class="field-value">{campo['caminho']}</td>
                                </tr>"""
        
        # Finaliza o XSLT
        xslt += """
                            </tbody>
                        </table>
                    </div>
                    
                    <!-- Seção de Código XSLT -->
                    <div class="section">
                        <h2>📝 Código XSLT Gerado</h2>
                        <div class="info-box">
                            <h3>Para usar em seus templates XSLT:</h3>
                            <pre style="background: #f8f8f8; padding: 15px; border-radius: 5px; overflow-x: auto;">"""
        
        # Adiciona código XSLT para cada campo wt9_
        for campo in campos_wt9:
            xslt += f"""
<!-- Campo: {campo['nome']} -->
<xsl:value-of select="$rootProductRevision/plm:UserData/plm:UserValue[@title='{campo['nome']}']/@value"/>

<!-- Com condição: -->
<xsl:choose>
    <xsl:when test="$rootProductRevision/plm:UserData/plm:UserValue[@title='{campo['nome']}']/@value != ''">
        <xsl:value-of select="$rootProductRevision/plm:UserData/plm:UserValue[@title='{campo['nome']}']/@value"/>
    </xsl:when>
    <xsl:otherwise>Valor padrão</xsl:otherwise>
</xsl:choose>"""
        
        # Finaliza o HTML
        xslt += """
                            </pre>
                        </div>
                    </div>
                    
                                         <!-- Rodapé -->
                     <div class="info-box">
                         <div style="text-align: center; margin: 20px 0;">
                             <div style="font-family: 'Courier New', monospace; font-size: 12px; color: #007acc; margin-bottom: 15px;">
                                 ███████╗███╗   ███╗ █████╗ ██████╗ ████████╗██████╗ 
                                 ██╔════╝████╗ ████║██╔══██╗██╔══██╗╚══██╔══╝██╔══██╗
                                 ███████╗██╔████╔██║███████║██████╔╝   ██║   ██████╔╝
                                 ╚════██║██║╚██╔╝██║██╔══██║██╔═══╝    ██║   ██╔══██╗
                                 ███████║██║ ╚═╝ ██║██║  ██║██║        ██║   ██║  ██║
                                 ╚══════╝╚═╝     ╚═╝╚═╝  ╚═╝╚═╝        ╚═╝   ╚═╝  ╚═╝
                                                     ██████╗ ██╗     ███╗   ██╗
                                                    ██╔═══██╗██║     ████╗  ██║
                                                    ██║   ██║██║     ██╔██╗ ██║
                                                    ██║   ██║██║     ██║╚██╗██║
                                                    ╚██████╔╝███████╗██║ ╚████║
                                                     ╚═════╝ ╚══════╝╚═╝  ╚═══╝
                             </div>
                             <h3 style="color: #007acc; margin: 10px 0;">SmartPLM</h3>
                             <p style="font-style: italic; color: #666;">Soluções Inteligentes em PLM</p>
                             <p style="margin: 15px 0;"><strong>Gerador de Código XSLT - PLMXML Reporter</strong></p>
                             <p style="font-size: 11px; color: #888;">Desenvolvido por André Luiz</p>
                             <hr style="border: 1px solid #ddd; margin: 15px 0;">
                             <p><strong>Data de Geração:</strong> <xsl:value-of select="substring(/plm:PLMXML/@date,1,10)"/></p>
                             <p><strong>Total de campos wt9_:</strong> """ + str(len(campos_wt9)) + """</p>
                             <p style="font-size: 10px; color: #999; margin-top: 20px;">
                                 © 2025 SmartPLM - Todos os direitos reservados
                             </p>
                         </div>
                     </div>
                </div>
            </body>
        </html>
    </xsl:template>

    <!-- Templates vazios para ignorar elementos não processados -->
    <xsl:template match="text()"/>
    <xsl:template match="plm:Header|plm:Product|plm:ProductRevision[not(ancestor::plm:PLMXML)]|plm:Form|plm:AssociatedForm|plm:ApplicationRef|plm:UserData|plm:UserValue|plm:Transform|plm:AttributeContext|plm:ProductView|plm:RevisionRule|plm:AccessIntent|plm:Site|plm:Text|plm:Item"/>

</xsl:stylesheet>"""
        
        return xslt
        
    def selecionar_campo_da_lista(self, event):
        """Seleciona campo da lista e gera código XSLT"""
        selecao = self.lista_campos.curselection()
        if selecao:
            indice = selecao[0]
            if indice < len(self.campos_encontrados):
                campo = self.campos_encontrados[indice]
                
                # Gera código para o campo selecionado
                codigo_xslt = self.gerar_codigo_xslt_para_campos([campo])
                
                # Exibe código
                self.texto_xslt.delete(1.0, tk.END)
                self.texto_xslt.insert(1.0, codigo_xslt)
                
                self.log(f"✅ Gerado código XSLT para campo: {campo['nome']}")
                
    def copiar_codigo(self):
        """Copia código XSLT para clipboard"""
        codigo = self.texto_xslt.get(1.0, tk.END).strip()
        if codigo:
            self.root.clipboard_clear()
            self.root.clipboard_append(codigo)
            self.log("📋 Código XSLT copiado para clipboard")
            messagebox.showinfo("Sucesso", "Código XSLT copiado para clipboard!")
        else:
            messagebox.showwarning("Aviso", "Nenhum código para copiar!")
            
    def salvar_codigo(self):
        """Salva código XSLT em arquivo"""
        codigo = self.texto_xslt.get(1.0, tk.END).strip()
        if not codigo:
            messagebox.showwarning("Aviso", "Nenhum código para salvar!")
            return
            
        arquivo = filedialog.asksaveasfilename(
            title="Salvar Código XSLT",
            defaultextension=".xslt",
            filetypes=[("Arquivos XSLT", "*.xslt"), ("Arquivos XML", "*.xml"), ("Todos os arquivos", "*.*")]
        )
        
        if arquivo:
            try:
                with open(arquivo, 'w', encoding='utf-8') as f:
                    f.write(codigo)
                self.log(f"💾 Código XSLT salvo em: {arquivo}")
                messagebox.showinfo("Sucesso", f"Código XSLT salvo em:\n{arquivo}")
            except Exception as e:
                self.log(f"❌ Erro ao salvar arquivo: {str(e)}")
                messagebox.showerror("Erro", f"Erro ao salvar arquivo: {str(e)}")
                
    def limpar_codigo(self):
        """Limpa área de código XSLT"""
        self.texto_xslt.delete(1.0, tk.END)
        self.log("🗑️ Código XSLT limpo")
        
    def salvar_html(self):
        """Salva o HTML gerado em arquivo"""
        codigo = self.texto_xslt.get(1.0, tk.END).strip()
        if not codigo:
            messagebox.showwarning("Aviso", "Gere o HTML primeiro!")
            return
            
        arquivo = filedialog.asksaveasfilename(
            title="Salvar HTML Completo",
            defaultextension=".html",
            filetypes=[("Arquivos HTML", "*.html"), ("Todos os arquivos", "*.*")]
        )
        
        if arquivo:
            try:
                with open(arquivo, 'w', encoding='utf-8') as f:
                    f.write(codigo)
                self.log(f"💾 HTML salvo em: {arquivo}")
                messagebox.showinfo("Sucesso", f"HTML salvo em:\n{arquivo}")
                
                # Pergunta se quer abrir o arquivo
                if messagebox.askyesno("Abrir Arquivo", "Deseja abrir o arquivo HTML no navegador?"):
                    import webbrowser
                    webbrowser.open(f'file://{os.path.abspath(arquivo)}')
                    
            except Exception as e:
                self.log(f"❌ Erro ao salvar HTML: {str(e)}")
                messagebox.showerror("Erro", f"Erro ao salvar HTML: {str(e)}")
        
    def log(self, mensagem):
        """Adiciona mensagem aos logs"""
        timestamp = datetime.now().strftime('%H:%M:%S')
        print(f"[{timestamp}] {mensagem}")

def main():
    """Função principal"""
    root = tk.Tk()
    app = XSLTGenerator(root)
    
    # Configuração do tema
    style = ttk.Style()
    style.theme_use('clam')
    
    # Centraliza a janela
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (root.winfo_width() // 2)
    y = (root.winfo_screenheight() // 2) - (root.winfo_height() // 2)
    root.geometry(f"+{x}+{y}")
    
    root.mainloop()

if __name__ == "__main__":
    main() 