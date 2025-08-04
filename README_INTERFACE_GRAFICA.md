# 🖥️ Interface Gráfica - PLMXML Reporter

## Visão Geral

A interface gráfica do PLMXML Reporter oferece uma experiência moderna e intuitiva para processamento de arquivos PLMXML, eliminando a necessidade de comandos de linha.

## 🚀 Como Executar

### Método 1: Script Principal
```bash
python gui_runner.py
```

### Método 2: Execução Direta
```bash
python src/gui/interface_grafica.py
```

## 📋 Funcionalidades

### 🎯 Principais Recursos

1. **Seleção de Arquivos**
   - Seleção múltipla de arquivos PLMXML
   - Interface drag-and-drop (futuro)
   - Visualização da lista de arquivos selecionados

2. **Configurações Flexíveis**
   - Escolha entre parser básico ou avançado
   - Opção de gerar relatórios HTML
   - Configuração de pasta de saída personalizada

3. **Processamento em Tempo Real**
   - Barra de progresso visual
   - Logs em tempo real
   - Possibilidade de interromper processamento
   - Status detalhado do processamento

4. **Visualização de Resultados**
   - Lista organizada de arquivos gerados
   - Abertura direta de arquivos (HTML, XML, JSON)
   - Acesso rápido à pasta de resultados

### 🎨 Interface Moderna

- **Design Responsivo**: Interface adaptável a diferentes tamanhos de tela
- **Tema Claro**: Interface limpa e profissional
- **Ícones Intuitivos**: Uso de emojis para melhor identificação
- **Menu Completo**: Acesso rápido a todas as funcionalidades

## 📖 Guia de Uso

### 1. Seleção de Arquivos
1. Clique em "Selecionar Arquivos PLMXML"
2. Escolha um ou mais arquivos `.xml` ou `.plmxml`
3. Os arquivos aparecerão na lista de seleção

### 2. Configuração
1. **Tipo de Parser**: Escolha entre "básico" ou "avançado"
2. **Gerar HTML**: Marque para criar relatórios HTML
3. **Pasta de Saída**: Configure onde salvar os resultados

### 3. Processamento
1. Clique em "🚀 Processar Arquivos"
2. Acompanhe o progresso na barra de progresso
3. Monitore os logs em tempo real
4. Use "⏹️ Parar Processamento" se necessário

### 4. Visualização de Resultados
1. Após o processamento, os resultados aparecem na lista
2. Clique em "Abrir Arquivo" para visualizar um arquivo específico
3. Use "Abrir Pasta" para acessar todos os resultados

## 🛠️ Menu Principal

### 📁 Menu Arquivo
- **Selecionar Arquivos**: Abre diálogo de seleção
- **Limpar Seleção**: Remove todos os arquivos selecionados
- **Sair**: Fecha a aplicação

### 🔄 Menu Processamento
- **Processar Arquivos**: Inicia o processamento
- **Parar Processamento**: Interrompe o processamento

### 🔧 Menu Ferramentas
- **Abrir Pasta de Resultados**: Abre a pasta com os arquivos gerados
- **Limpar Logs**: Limpa a área de logs

### ❓ Menu Ajuda
- **Sobre**: Informações sobre a aplicação

## 📊 Logs em Tempo Real

A interface exibe logs detalhados incluindo:
- ✅ Processos bem-sucedidos
- ❌ Erros encontrados
- 📄 Arquivos gerados
- ⏱️ Tempo de processamento
- 📁 Operações de arquivo

## 🎯 Tipos de Parser

### Parser Básico
- Processamento rápido
- Extração de dados essenciais
- Ideal para arquivos simples

### Parser Avançado
- Análise detalhada
- Extração de metadados complexos
- Relatórios mais completos

## 📁 Estrutura de Saída

```
data/output/
├── arquivo_dados_YYYYMMDD_HHMMSS.json
├── arquivo_dados_YYYYMMDD_HHMMSS_para_xslt.xml
└── arquivo_dados_YYYYMMDD_HHMMSS_para_xslt_relatorio.html
```

## 🔧 Requisitos

- Python 3.7+
- tkinter (incluído na maioria das instalações Python)
- Módulos do PLMXML Reporter

## 🚨 Solução de Problemas

### Erro: "tkinter não encontrado"
```bash
# Ubuntu/Debian
sudo apt-get install python3-tk

# Windows
# tkinter geralmente já está incluído
```

### Erro: "Módulos não encontrados"
```bash
# Execute a partir da raiz do projeto
python gui_runner.py
```

### Interface não responde
- Verifique se o processamento não está em andamento
- Use "Parar Processamento" se necessário
- Reinicie a aplicação se necessário

## 🎨 Personalização

### Alterando o Tema
```python
# No arquivo interface_grafica.py
style.theme_use('clam')  # ou 'alt', 'default', 'classic'
```

### Modificando Cores
```python
# Adicione no método main()
root.configure(bg='#f0f0f0')  # Cor de fundo
```

## 📈 Próximas Melhorias

- [ ] Suporte a drag-and-drop
- [ ] Temas escuro/claro
- [ ] Configurações salvas automaticamente
- [ ] Preview de arquivos
- [ ] Processamento em lote avançado
- [ ] Relatórios de estatísticas detalhados

## 🤝 Contribuição

Para contribuir com melhorias na interface gráfica:

1. Fork o projeto
2. Crie uma branch para sua feature
3. Implemente as melhorias
4. Teste extensivamente
5. Envie um pull request

---

**Desenvolvido com ❤️ para facilitar o processamento de arquivos PLMXML** 