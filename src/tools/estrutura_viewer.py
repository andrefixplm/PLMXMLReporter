# -*- coding: utf-8 -*-
"""
Visualizador de Estrutura PLMXML
Ferramenta para analisar estrutura de arquivos PLMXML e gerar código XSLT
"""

import os
import sys
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from datetime import datetime
import xml.etree.ElementTree as ET

# Adiciona path para imports
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from src.utils.logger import configurar_logger
from src.parsers.plmxml_parser_avancado import PLMXMLParserAvancado

class EstruturaPLMXMLViewer:
    def __init__(self, root):
        self.root = root
        self.root.title("🔍 Visualizador de Estrutura PLMXML")
        self.root.geometry("1200x800")
        self.root.configure(bg='#f0f0f0')
        
        # Configuração do logger
        self.logger = configurar_logger()
        
        # Variáveis de controle
        self.arquivo_plmxml = None
        self.estrutura_completa = {}
        self.elementos_encontrados = []
        
        # Inicializa parser
        self.parser = PLMXMLParserAvancado()
        
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
        main_frame.rowconfigure(1, weight=1)
        
        # Título
        titulo = ttk.Label(main_frame, text="🔍 Visualizador de Estrutura PLMXML", 
                          font=('Arial', 16, 'bold'))
        titulo.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Frame de seleção de arquivo
        self.criar_frame_selecao(main_frame)
        
        # Frame de busca
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
        
        # Botão analisar estrutura
        self.btn_analisar = ttk.Button(frame, text="🔍 Analisar Estrutura", 
                                      command=self.analisar_estrutura, state=tk.DISABLED)
        self.btn_analisar.grid(row=0, column=2, padx=(10, 0))
        
    def criar_frame_busca(self, parent):
        """Cria frame para busca de campos"""
        frame = ttk.LabelFrame(parent, text="🔎 Busca de Campos", padding="10")
        frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Campo de busca
        ttk.Label(frame, text="Buscar campo:").grid(row=0, column=0, sticky=tk.W)
        self.entry_busca = ttk.Entry(frame, width=40)
        self.entry_busca.grid(row=0, column=1, padx=(10, 10), sticky=tk.W)
        self.entry_busca.bind('<Return>', lambda e: self.buscar_campo())
        
        # Botão buscar
        btn_buscar = ttk.Button(frame, text="🔍 Buscar", command=self.buscar_campo)
        btn_buscar.grid(row=0, column=2, padx=(0, 10))
        
        # Botão mostrar todos
        btn_todos = ttk.Button(frame, text="📋 Mostrar Todos", command=self.mostrar_todos_campos)
        btn_todos.grid(row=0, column=3)
        
    def criar_frame_resultados(self, parent):
        """Cria frame para exibição de resultados"""
        frame = ttk.LabelFrame(parent, text="📊 Resultados", padding="10")
        frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S))
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(1, weight=1)
        
        # Notebook para abas
        self.notebook = ttk.Notebook(frame)
        self.notebook.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Aba de estrutura
        self.criar_aba_estrutura()
        
        # Aba de busca
        self.criar_aba_busca()
        
        # Aba de código XSLT
        self.criar_aba_xslt()
        
    def criar_aba_estrutura(self):
        """Cria aba para visualização da estrutura"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="🌳 Estrutura Completa")
        
        # Treeview para estrutura
        self.tree_estrutura = ttk.Treeview(frame, columns=('tipo', 'atributos'), show='tree headings')
        self.tree_estrutura.heading('#0', text='Elemento')
        self.tree_estrutura.heading('tipo', text='Tipo')
        self.tree_estrutura.heading('atributos', text='Atributos')
        
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
        
    def criar_aba_busca(self):
        """Cria aba para resultados de busca"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="🔍 Resultados da Busca")
        
        # Lista de resultados
        self.lista_resultados = tk.Listbox(frame, height=15)
        self.lista_resultados.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=self.lista_resultados.yview)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.lista_resultados.configure(yscrollcommand=scrollbar.set)
        
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(0, weight=1)
        
    def criar_aba_xslt(self):
        """Cria aba para código XSLT gerado"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="📝 Código XSLT")
        
        # Área de texto para código XSLT
        self.texto_xslt = scrolledtext.ScrolledText(frame, height=15, width=80)
        self.texto_xslt.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Botões
        btn_frame = ttk.Frame(frame)
        btn_frame.grid(row=1, column=0, pady=(5, 0))
        
        btn_copiar = ttk.Button(btn_frame, text="📋 Copiar Código", command=self.copiar_codigo)
        btn_copiar.grid(row=0, column=0, padx=(0, 5))
        
        btn_limpar = ttk.Button(btn_frame, text="🗑️ Limpar", command=self.limpar_codigo)
        btn_limpar.grid(row=0, column=1)
        
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
            self.btn_analisar.config(state=tk.NORMAL)
            self.log(f"📁 Arquivo selecionado: {os.path.basename(arquivo)}")
            
    def analisar_estrutura(self):
        """Analisa a estrutura do arquivo PLMXML"""
        if not self.arquivo_plmxml:
            messagebox.showwarning("Aviso", "Selecione um arquivo PLMXML primeiro!")
            return
            
        try:
            self.log("🔍 Analisando estrutura do arquivo...")
            
            # Parse do XML
            tree = ET.parse(self.arquivo_plmxml)
            root = tree.getroot()
            
            # Analisa estrutura
            self.estrutura_completa = self.analisar_elemento(root, "")
            
            # Popula treeview
            self.popular_treeview()
            
            self.log("✅ Estrutura analisada com sucesso!")
            
        except Exception as e:
            self.log(f"❌ Erro ao analisar estrutura: {str(e)}")
            messagebox.showerror("Erro", f"Erro ao analisar arquivo: {str(e)}")
            
    def analisar_elemento(self, elemento, caminho):
        """Analisa um elemento XML recursivamente"""
        resultado = {
            'tag': elemento.tag,
            'atributos': dict(elemento.attrib),
            'texto': elemento.text.strip() if elemento.text and elemento.text.strip() else None,
            'filhos': []
        }
        
        # Processa filhos
        for filho in elemento:
            caminho_filho = f"{caminho}/{filho.tag}" if caminho else filho.tag
            resultado['filhos'].append(self.analisar_elemento(filho, caminho_filho))
            
        return resultado
        
    def popular_treeview(self):
        """Popula o treeview com a estrutura"""
        # Limpa treeview
        for item in self.tree_estrutura.get_children():
            self.tree_estrutura.delete(item)
            
        # Adiciona elementos
        self.adicionar_elemento_treeview("", self.estrutura_completa)
        
    def adicionar_elemento_treeview(self, parent, elemento):
        """Adiciona elemento ao treeview"""
        # Prepara informações
        tag = elemento['tag']
        atributos = ", ".join([f"{k}='{v}'" for k, v in elemento['atributos'].items()])
        texto = elemento['texto'] if elemento['texto'] else ""
        
        # Cria item
        item = self.tree_estrutura.insert(parent, 'end', text=tag, 
                                        values=('Elemento', atributos))
        
        # Adiciona texto se houver
        if texto:
            self.tree_estrutura.insert(item, 'end', text=f"Texto: {texto}", 
                                     values=('Texto', ''))
            
        # Adiciona filhos
        for filho in elemento['filhos']:
            self.adicionar_elemento_treeview(item, filho)
            
    def buscar_campo(self):
        """Busca um campo específico"""
        termo = self.entry_busca.get().strip()
        if not termo:
            messagebox.showwarning("Aviso", "Digite um termo para buscar!")
            return
            
        self.log(f"🔍 Buscando por: {termo}")
        
        # Limpa lista de resultados
        self.lista_resultados.delete(0, tk.END)
        
        # Busca no arquivo
        resultados = self.buscar_no_xml(termo)
        
        if resultados:
            for resultado in resultados:
                self.lista_resultados.insert(tk.END, resultado)
            self.log(f"✅ Encontrados {len(resultados)} resultados")
        else:
            self.lista_resultados.insert(tk.END, f"Nenhum resultado encontrado para '{termo}'")
            self.log(f"❌ Nenhum resultado encontrado para '{termo}'")
            
    def buscar_no_xml(self, termo):
        """Busca termo no XML e retorna caminhos XPath"""
        if not self.arquivo_plmxml:
            return []
            
        try:
            tree = ET.parse(self.arquivo_plmxml)
            root = tree.getroot()
            
            resultados = []
            
            # Busca por atributos
            for elem in root.iter():
                for attr_name, attr_value in elem.attrib.items():
                    if termo.lower() in attr_name.lower() or termo.lower() in attr_value.lower():
                        caminho = self.obter_caminho_xpath(elem)
                        resultados.append(f"Atributo: {caminho}/@{attr_name}='{attr_value}'")
                        
                # Busca por texto
                if elem.text and termo.lower() in elem.text.lower():
                    caminho = self.obter_caminho_xpath(elem)
                    resultados.append(f"Texto: {caminho} = '{elem.text.strip()}'")
                    
            return resultados
            
        except Exception as e:
            self.log(f"❌ Erro na busca: {str(e)}")
            return []
            
    def obter_caminho_xpath(self, elemento):
        """Obtém caminho XPath de um elemento"""
        caminho = []
        while elemento is not None:
            if elemento.tag:
                caminho.append(elemento.tag)
            elemento = elemento.getparent() if hasattr(elemento, 'getparent') else None
            
        return "/" + "/".join(reversed(caminho))
        
    def mostrar_todos_campos(self):
        """Mostra todos os campos encontrados"""
        if not self.arquivo_plmxml:
            messagebox.showwarning("Aviso", "Selecione um arquivo PLMXML primeiro!")
            return
            
        self.log("📋 Extraindo todos os campos...")
        
        # Limpa lista
        self.lista_resultados.delete(0, tk.END)
        
        # Extrai campos
        campos = self.extrair_todos_campos()
        
        for campo in campos:
            self.lista_resultados.insert(tk.END, campo)
            
        self.log(f"✅ Extraídos {len(campos)} campos")
        
    def extrair_todos_campos(self):
        """Extrai todos os campos do XML"""
        if not self.arquivo_plmxml:
            return []
            
        try:
            tree = ET.parse(self.arquivo_plmxml)
            root = tree.getroot()
            
            campos = []
            
            for elem in root.iter():
                # Atributos
                for attr_name, attr_value in elem.attrib.items():
                    campos.append(f"{elem.tag}/@{attr_name} = '{attr_value}'")
                    
                # Texto
                if elem.text and elem.text.strip():
                    campos.append(f"{elem.tag} = '{elem.text.strip()}'")
                    
            return campos
            
        except Exception as e:
            self.log(f"❌ Erro ao extrair campos: {str(e)}")
            return []
            
    def gerar_codigo_xslt(self, campo):
        """Gera código XSLT para um campo específico"""
        # Remove namespace se presente
        if ':' in campo:
            tag = campo.split(':')[-1]
        else:
            tag = campo
            
        # Gera código XSLT
        codigo = f"""<!-- Código XSLT para {campo} -->
<xsl:value-of select="$rootProductRevision/plm:UserData/plm:UserValue[@title='{tag}']/@value"/>

<!-- Alternativas: -->
<xsl:value-of select="//plm:UserValue[@title='{tag}']/@value"/>
<xsl:value-of select="//*[@title='{tag}']/@value"/>
<xsl:value-of select="//{tag}"/>"""
        
        return codigo
        
    def copiar_codigo(self):
        """Copia código XSLT para clipboard"""
        codigo = self.texto_xslt.get(1.0, tk.END).strip()
        if codigo:
            self.root.clipboard_clear()
            self.root.clipboard_append(codigo)
            self.log("📋 Código copiado para clipboard")
            messagebox.showinfo("Sucesso", "Código XSLT copiado para clipboard!")
        else:
            messagebox.showwarning("Aviso", "Nenhum código para copiar!")
            
    def limpar_codigo(self):
        """Limpa área de código XSLT"""
        self.texto_xslt.delete(1.0, tk.END)
        self.log("🗑️ Código XSLT limpo")
        
    def log(self, mensagem):
        """Adiciona mensagem aos logs"""
        timestamp = datetime.now().strftime('%H:%M:%S')
        print(f"[{timestamp}] {mensagem}")

def main():
    """Função principal"""
    root = tk.Tk()
    app = EstruturaPLMXMLViewer(root)
    
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