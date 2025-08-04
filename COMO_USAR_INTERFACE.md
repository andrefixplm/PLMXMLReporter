# 🚀 Como Usar a Interface Gráfica

## ⚡ Inicialização Rápida

### Windows
```bash
# Método 1: Script batch
iniciar_interface.bat

# Método 2: Python direto
python gui_runner.py

# Método 3: Duplo clique no arquivo
iniciar_interface.bat
```

### Linux/Mac
```bash
# Método 1: Script shell
./iniciar_interface.sh

# Método 2: Python direto
python3 gui_runner.py
```

## 📋 Passo a Passo

### 1. Selecionar Arquivos
- Clique em "Selecionar Arquivos PLMXML"
- Escolha um ou mais arquivos `.xml` ou `.plmxml`
- Os arquivos aparecerão na lista

### 2. Configurar Processamento
- **Tipo de Parser**: Escolha "básico" ou "avançado"
- **Gerar HTML**: Marque para criar relatórios HTML
- **Pasta de Saída**: Configure onde salvar (padrão: `data/output`)

### 3. Processar
- Clique em "🚀 Processar Arquivos"
- Acompanhe o progresso na barra
- Monitore os logs em tempo real

### 4. Visualizar Resultados
- Após processamento, clique em "Abrir Arquivo" para ver um arquivo específico
- Use "Abrir Pasta" para acessar todos os resultados

## 🎯 Dicas de Uso

### Para Arquivos Grandes
- Use o parser "básico" para processamento mais rápido
- Monitore os logs para acompanhar o progresso

### Para Relatórios Detalhados
- Use o parser "avançado"
- Marque "Gerar HTML" para relatórios visuais

### Para Múltiplos Arquivos
- Selecione vários arquivos de uma vez
- Configure a pasta de saída adequadamente
- Use "Parar Processamento" se necessário

## 🛠️ Solução de Problemas

### Interface não abre
```bash
# Verifique se Python está instalado
python --version

# Execute o teste
python test_gui.py
```

### Erro de módulos
```bash
# Execute a partir da raiz do projeto
cd /caminho/para/PLMXMLReporter
python gui_runner.py
```

### Arquivos não processam
- Verifique se os arquivos são PLMXML válidos
- Confirme se a pasta de saída existe
- Monitore os logs para detalhes do erro

## 📊 Estrutura de Saída

```
data/output/
├── arquivo_dados_20250804_091635.json
├── arquivo_dados_20250804_091635_para_xslt.xml
└── arquivo_dados_20250804_091635_para_xslt_relatorio.html
```

## 🎨 Personalização

### Alterar Tema
Edite `src/gui/interface_grafica.py`:
```python
style.theme_use('clam')  # ou 'alt', 'default', 'classic'
```

### Alterar Tamanho da Janela
```python
self.root.geometry("1200x800")  # Largura x Altura
```

## 📞 Suporte

Se encontrar problemas:
1. Execute `python test_gui.py` para diagnóstico
2. Verifique os logs em `logs/`
3. Consulte `README_INTERFACE_GRAFICA.md` para documentação completa

---

**Interface Gráfica PLMXML Reporter - Versão 1.0** 