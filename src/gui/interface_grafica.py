# -*- coding: utf-8 -*-
"""
Interface Gráfica para PLMXML Reporter
Interface moderna e intuitiva para processamento de arquivos PLMXML
"""

import os
import sys
import threading
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from datetime import datetime
import webbrowser
import subprocess

# Adiciona path para imports
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from src.utils.logger import configurar_logger
from src.parsers.plmxml_parser_basico import PLMXMLParserBasico
from src.parsers.plmxml_parser_avancado import PLMXMLParserAvancado
from src.transformers.json_para_xml import JSONParaXMLConverter
from src.transformers.aplicar_xslt import XSLTProcessor

class PLMXMLReporterGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("PLMXML Reporter - Interface Gráfica - SmartPLM Soluções Inteligentes em PLM")
        self.root.geometry("1000x700")
        self.root.configure(bg='#f0f0f0')
        
        # Configuração do logger
        self.logger = configurar_logger()
        
        # Variáveis de controle
        self.arquivos_selecionados = []
        self.processamento_ativo = False
        self.resultados = []
        
        # Inicializa componentes
        self.parser_basico = PLMXMLParserBasico()
        self.parser_avancado = PLMXMLParserAvancado()
        self.conversor = JSONParaXMLConverter()
        self.xslt_processor = XSLTProcessor()
        
        self.criar_interface()
        
    def criar_menu(self):
        """Cria o menu principal da aplicação"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # Menu Arquivo
        menu_arquivo = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Arquivo", menu=menu_arquivo)
        menu_arquivo.add_command(label="Selecionar Arquivos", command=self.selecionar_arquivos)
        menu_arquivo.add_command(label="Limpar Seleção", command=self.limpar_selecao)
        menu_arquivo.add_separator()
        menu_arquivo.add_command(label="Sair", command=self.root.quit)
        
        # Menu Processamento
        menu_processamento = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Processamento", menu=menu_processamento)
        menu_processamento.add_command(label="Processar Arquivos", command=self.processar_arquivos)
        menu_processamento.add_command(label="Parar Processamento", command=self.parar_processamento)
        
        # Menu Ferramentas
        menu_ferramentas = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Ferramentas", menu=menu_ferramentas)
        menu_ferramentas.add_command(label="Abrir Pasta de Resultados", command=self.abrir_pasta_resultados)
        menu_ferramentas.add_command(label="Limpar Logs", command=self.limpar_logs)
        
        # Menu Ajuda
        menu_ajuda = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Ajuda", menu=menu_ajuda)
        menu_ajuda.add_command(label="Sobre", command=self.mostrar_sobre)
        
    def mostrar_sobre(self):
        """Mostra informações sobre a aplicação"""
        sobre_texto = """
PLMXML Reporter - Interface Gráfica (SmartPLM Soluções Inteligentes em PLM - Andre Luiz)

Versão: 1.0
Desenvolvido para processamento de arquivos PLMXML

Funcionalidades:
• Parser básico e avançado para arquivos PLMXML
• Conversão para JSON estruturado
• Geração de relatórios HTML
• Interface gráfica moderna e intuitiva
• Logs em tempo real
• Visualização de resultados

Para mais informações, consulte a documentação.
        """
        messagebox.showinfo("Sobre", sobre_texto)
        
    def criar_interface(self):
        """Cria a interface gráfica principal"""
        
        # Cria menu
        self.criar_menu()
        
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configuração do grid
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(3, weight=1)
        
        # Título
        titulo = ttk.Label(main_frame, text="🚀 PLMXML Reporter", 
                          font=('Arial', 16, 'bold'))
        titulo.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Frame de seleção de arquivos
        self.criar_frame_selecao_arquivos(main_frame)
        
        # Frame de configurações
        self.criar_frame_configuracoes(main_frame)
        
        # Frame de processamento
        self.criar_frame_processamento(main_frame)
        
        # Frame de logs
        self.criar_frame_logs(main_frame)
        
        # Frame de resultados
        self.criar_frame_resultados(main_frame)
        
    def criar_frame_selecao_arquivos(self, parent):
        """Cria frame para seleção de arquivos"""
        frame = ttk.LabelFrame(parent, text="📁 Seleção de Arquivos", padding="10")
        frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        frame.columnconfigure(1, weight=1)
        
        # Botão selecionar arquivos
        btn_selecionar = ttk.Button(frame, text="Selecionar Arquivos PLMXML", 
                                   command=self.selecionar_arquivos)
        btn_selecionar.grid(row=0, column=0, padx=(0, 10))
        
        # Lista de arquivos selecionados
        self.lista_arquivos = tk.Listbox(frame, height=4, selectmode=tk.MULTIPLE)
        self.lista_arquivos.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(10, 0))
        
        # Scrollbar para lista
        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=self.lista_arquivos.yview)
        scrollbar.grid(row=0, column=2, sticky=(tk.N, tk.S))
        self.lista_arquivos.configure(yscrollcommand=scrollbar.set)
        
        # Botão limpar seleção
        btn_limpar = ttk.Button(frame, text="Limpar Seleção", 
                               command=self.limpar_selecao)
        btn_limpar.grid(row=1, column=0, pady=(10, 0))
        
    def criar_frame_configuracoes(self, parent):
        """Cria frame para configurações de processamento"""
        frame = ttk.LabelFrame(parent, text="⚙️ Configurações", padding="10")
        frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Tipo de parser
        ttk.Label(frame, text="Tipo de Parser:").grid(row=0, column=0, sticky=tk.W)
        self.parser_var = tk.StringVar(value="avancado")
        parser_combo = ttk.Combobox(frame, textvariable=self.parser_var, 
                                   values=["basico", "avancado"], state="readonly")
        parser_combo.grid(row=0, column=1, padx=(10, 20), sticky=tk.W)
        
        # Gerar HTML
        self.gerar_html_var = tk.BooleanVar(value=True)
        chk_html = ttk.Checkbutton(frame, text="Gerar Relatório HTML", 
                                  variable=self.gerar_html_var)
        chk_html.grid(row=0, column=2, padx=(20, 0))
        
        # Pasta de saída
        ttk.Label(frame, text="Pasta de Saída:").grid(row=1, column=0, sticky=tk.W, pady=(10, 0))
        self.pasta_saida_var = tk.StringVar(value="data\\output")
        entry_saida = ttk.Entry(frame, textvariable=self.pasta_saida_var, width=30)
        entry_saida.grid(row=1, column=1, padx=(10, 10), pady=(10, 0), sticky=tk.W)
        
        btn_pasta = ttk.Button(frame, text="Escolher Pasta", 
                              command=self.selecionar_pasta_saida)
        btn_pasta.grid(row=1, column=2, pady=(10, 0))
        
    def criar_frame_processamento(self, parent):
        """Cria frame para controles de processamento"""
        frame = ttk.LabelFrame(parent, text="🔄 Processamento", padding="10")
        frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Botões de processamento
        btn_frame = ttk.Frame(frame)
        btn_frame.grid(row=0, column=0, columnspan=3)
        
        self.btn_processar = ttk.Button(btn_frame, text="🚀 Processar Arquivos", 
                                       command=self.processar_arquivos)
        self.btn_processar.grid(row=0, column=0, padx=(0, 10))
        
        self.btn_parar = ttk.Button(btn_frame, text="⏹️ Parar Processamento", 
                                   command=self.parar_processamento, state=tk.DISABLED)
        self.btn_parar.grid(row=0, column=1, padx=(0, 10))
        
        # Barra de progresso
        self.progresso = ttk.Progressbar(frame, mode='indeterminate')
        self.progresso.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 0))
        
        # Status
        self.status_var = tk.StringVar(value="Pronto para processar")
        lbl_status = ttk.Label(frame, textvariable=self.status_var)
        lbl_status.grid(row=2, column=0, columnspan=3, pady=(5, 0))
        
    def criar_frame_logs(self, parent):
        """Cria frame para exibição de logs"""
        frame = ttk.LabelFrame(parent, text="📋 Logs", padding="10")
        frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 5))
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(0, weight=1)
        
        # Área de logs
        self.area_logs = scrolledtext.ScrolledText(frame, height=8, width=60)
        self.area_logs.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Botão limpar logs
        btn_limpar_logs = ttk.Button(frame, text="Limpar Logs", 
                                    command=self.limpar_logs)
        btn_limpar_logs.grid(row=1, column=0, pady=(5, 0))
        
    def criar_frame_resultados(self, parent):
        """Cria frame para exibição de resultados"""
        frame = ttk.LabelFrame(parent, text="📄 Resultados", padding="10")
        frame.grid(row=4, column=2, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(5, 0))
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(1, weight=1)
        
        # Lista de resultados
        ttk.Label(frame, text="Arquivos Gerados:").grid(row=0, column=0, sticky=tk.W)
        
        self.lista_resultados = tk.Listbox(frame, height=8)
        self.lista_resultados.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Scrollbar para resultados
        scrollbar_resultados = ttk.Scrollbar(frame, orient=tk.VERTICAL, 
                                           command=self.lista_resultados.yview)
        scrollbar_resultados.grid(row=1, column=1, sticky=(tk.N, tk.S))
        self.lista_resultados.configure(yscrollcommand=scrollbar_resultados.set)
        
        # Botões de ação
        btn_frame_resultados = ttk.Frame(frame)
        btn_frame_resultados.grid(row=2, column=0, columnspan=2, pady=(5, 0))
        
        btn_abrir = ttk.Button(btn_frame_resultados, text="Abrir Arquivo", 
                              command=self.abrir_arquivo_selecionado)
        btn_abrir.grid(row=0, column=0, padx=(0, 5))
        
        btn_pasta_resultados = ttk.Button(btn_frame_resultados, text="Abrir Pasta", 
                                        command=self.abrir_pasta_resultados)
        btn_pasta_resultados.grid(row=0, column=1)
        
    def selecionar_arquivos(self):
        """Seleciona arquivos PLMXML"""
        arquivos = filedialog.askopenfilenames(
            title="Selecionar Arquivos PLMXML",
            filetypes=[("Arquivos PLMXML", "*.xml *.plmxml"), ("Todos os arquivos", "*.*")]
        )
        
        if arquivos:
            self.arquivos_selecionados = list(arquivos)
            self.atualizar_lista_arquivos()
            self.log(f"📁 {len(arquivos)} arquivo(s) selecionado(s)")
            
    def atualizar_lista_arquivos(self):
        """Atualiza a lista de arquivos selecionados"""
        self.lista_arquivos.delete(0, tk.END)
        for arquivo in self.arquivos_selecionados:
            self.lista_arquivos.insert(tk.END, os.path.basename(arquivo))
            
    def limpar_selecao(self):
        """Limpa a seleção de arquivos"""
        self.arquivos_selecionados = []
        self.lista_arquivos.delete(0, tk.END)
        self.log("🗑️ Seleção de arquivos limpa")
        
    def selecionar_pasta_saida(self):
        """Seleciona pasta de saída"""
        pasta = filedialog.askdirectory(title="Selecionar Pasta de Saída")
        if pasta:
            self.pasta_saida_var.set(pasta)
            self.log(f"📁 Pasta de saída definida: {pasta}")
            
    def processar_arquivos(self):
        """Inicia o processamento dos arquivos"""
        if not self.arquivos_selecionados:
            messagebox.showwarning("Aviso", "Selecione pelo menos um arquivo PLMXML!")
            return
            
        if self.processamento_ativo:
            messagebox.showwarning("Aviso", "Processamento já está em andamento!")
            return
            
        # Inicia processamento em thread separada
        self.processamento_ativo = True
        self.btn_processar.config(state=tk.DISABLED)
        self.btn_parar.config(state=tk.NORMAL)
        self.progresso.start()
        
        thread = threading.Thread(target=self.executar_processamento)
        thread.daemon = True
        thread.start()
        
    def executar_processamento(self):
        """Executa o processamento em thread separada"""
        try:
            self.log("🚀 Iniciando processamento...")
            self.status_var.set("Processando arquivos...")
            
            resultados = []
            total_arquivos = len(self.arquivos_selecionados)
            
            for i, arquivo in enumerate(self.arquivos_selecionados):
                if not self.processamento_ativo:
                    break
                    
                self.log(f"📄 Processando {i+1}/{total_arquivos}: {os.path.basename(arquivo)}")
                self.status_var.set(f"Processando {i+1}/{total_arquivos}...")
                
                resultado = self.processar_arquivo_individual(arquivo)
                resultados.append(resultado)
                
            self.resultados = resultados
            self.atualizar_resultados()
            self.log("✅ Processamento concluído!")
            
        except Exception as e:
            self.log(f"❌ Erro durante processamento: {str(e)}")
        finally:
            self.finalizar_processamento()
            
    def processar_arquivo_individual(self, arquivo):
        """Processa um arquivo individual"""
        try:
            # Seleciona parser baseado na configuração
            if self.parser_var.get() == "basico":
                parser = self.parser_basico
            else:
                parser = self.parser_avancado
                
            # Processa arquivo
            dados = parser.processar_arquivo_completo(arquivo)
            
            if not dados:
                return {'arquivo': arquivo, 'sucesso': False, 'erro': 'Falha no parsing'}
                
            # Salva JSON
            arquivo_json = self.salvar_json(dados, arquivo)
            
            # Converte para XML
            arquivo_xml = self.conversor.converter_arquivo_json(arquivo_json)
            
            # Gera HTML se solicitado
            arquivo_html = None
            if self.gerar_html_var.get():
                arquivo_html = self.xslt_processor.aplicar_xslt(arquivo_xml)
                
            return {
                'arquivo': arquivo,
                'sucesso': True,
                'json': arquivo_json,
                'xml': arquivo_xml,
                'html': arquivo_html
            }
            
        except Exception as e:
            return {'arquivo': arquivo, 'sucesso': False, 'erro': str(e)}
            
    def salvar_json(self, dados, arquivo_original):
        """Salva dados em JSON"""
        try:
            pasta_output = self.pasta_saida_var.get()
            if not os.path.exists(pasta_output):
                os.makedirs(pasta_output)
                
            nome_base = os.path.splitext(os.path.basename(arquivo_original))[0]
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            arquivo_json = os.path.join(pasta_output, f"{nome_base}_dados_{timestamp}.json")
            
            import json
            with open(arquivo_json, 'w', encoding='utf-8') as f:
                json.dump(dados, f, indent=2, ensure_ascii=False)
                
            return arquivo_json
        except Exception as e:
            self.log(f"❌ Erro ao salvar JSON: {str(e)}")
            return None
            
    def parar_processamento(self):
        """Para o processamento"""
        self.processamento_ativo = False
        self.log("⏹️ Processamento interrompido pelo usuário")
        
    def finalizar_processamento(self):
        """Finaliza o processamento"""
        self.processamento_ativo = False
        self.btn_processar.config(state=tk.NORMAL)
        self.btn_parar.config(state=tk.DISABLED)
        self.progresso.stop()
        self.status_var.set("Processamento finalizado")
        
    def atualizar_resultados(self):
        """Atualiza a lista de resultados"""
        self.lista_resultados.delete(0, tk.END)
        
        for resultado in self.resultados:
            if resultado['sucesso']:
                arquivo_base = os.path.basename(resultado['arquivo'])
                self.lista_resultados.insert(tk.END, f"✅ {arquivo_base}")
                
                if resultado.get('json'):
                    self.lista_resultados.insert(tk.END, f"   📄 JSON: {os.path.basename(resultado['json'])}")
                if resultado.get('xml'):
                    self.lista_resultados.insert(tk.END, f"   📄 XML: {os.path.basename(resultado['xml'])}")
                if resultado.get('html'):
                    self.lista_resultados.insert(tk.END, f"   📄 HTML: {os.path.basename(resultado['html'])}")
            else:
                arquivo_base = os.path.basename(resultado['arquivo'])
                self.lista_resultados.insert(tk.END, f"❌ {arquivo_base} - {resultado['erro']}")
                
    def abrir_arquivo_selecionado(self):
        """Abre o arquivo selecionado na lista de resultados"""
        selecao = self.lista_resultados.curselection()
        if not selecao:
            messagebox.showwarning("Aviso", "Selecione um arquivo na lista!")
            return
            
        # Encontra o arquivo correspondente à seleção
        arquivos_disponiveis = []
        for resultado in self.resultados:
            if resultado['sucesso']:
                arquivos_disponiveis.append(resultado.get('html'))
                arquivos_disponiveis.append(resultado.get('xml'))
                arquivos_disponiveis.append(resultado.get('json'))
        
        # Remove valores None
        arquivos_disponiveis = [f for f in arquivos_disponiveis if f]
        
        if selecao[0] < len(arquivos_disponiveis):
            arquivo_para_abrir = arquivos_disponiveis[selecao[0]]
            
            if os.path.exists(arquivo_para_abrir):
                try:
                    if arquivo_para_abrir.endswith('.html'):
                        # Abre HTML no navegador
                        webbrowser.open(f'file://{os.path.abspath(arquivo_para_abrir)}')
                    else:
                        # Abre outros arquivos com o programa padrão
                        if sys.platform == "win32":
                            os.startfile(arquivo_para_abrir)
                        else:
                            subprocess.run(["xdg-open", arquivo_para_abrir])
                            
                    self.log(f"📂 Arquivo aberto: {os.path.basename(arquivo_para_abrir)}")
                except Exception as e:
                    messagebox.showerror("Erro", f"Erro ao abrir arquivo: {str(e)}")
            else:
                messagebox.showwarning("Aviso", "Arquivo não encontrado!")
        else:
            messagebox.showwarning("Aviso", "Seleção inválida!")
        
    def abrir_pasta_resultados(self):
        """Abre a pasta de resultados"""
        pasta = self.pasta_saida_var.get()
        if os.path.exists(pasta):
            if sys.platform == "win32":
                os.startfile(pasta)
            else:
                subprocess.run(["xdg-open", pasta])
        else:
            messagebox.showwarning("Aviso", "Pasta de resultados não encontrada!")
            
    def limpar_logs(self):
        """Limpa a área de logs"""
        self.area_logs.delete(1.0, tk.END)
        
    def log(self, mensagem):
        """Adiciona mensagem aos logs"""
        timestamp = datetime.now().strftime('%H:%M:%S')
        log_entry = f"[{timestamp}] {mensagem}\n"
        
        # Atualiza logs na thread principal
        self.root.after(0, lambda: self.area_logs.insert(tk.END, log_entry))
        self.root.after(0, lambda: self.area_logs.see(tk.END))

def main():
    """Função principal da interface gráfica"""
    root = tk.Tk()
    app = PLMXMLReporterGUI(root)
    
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