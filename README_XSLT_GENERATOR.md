# 📝 Gerador de Código XSLT - PLMXML Reporter

## 🎯 Visão Geral

O **Gerador de Código XSLT** é uma ferramenta especializada para analisar arquivos PLMXML e gerar automaticamente código XSLT para mapeamento de campos. Ideal para desenvolvedores que precisam criar relatórios HTML a partir de dados PLMXML.

## 🚀 Como Executar

### Windows
```bash
# Método 1: Script batch
iniciar_xslt_generator.bat

# Método 2: Python direto
python xslt_generator_runner.py
```

### Linux/Mac
```bash
# Python direto
python3 xslt_generator_runner.py
```

## 📋 Funcionalidades Principais

### 🔍 Análise de Estrutura PLMXML
- **Parse completo** do arquivo PLMXML
- **Detecção automática** de campos UserValue
- **Visualização hierárquica** da estrutura XML
- **Extração de atributos** e valores

### 🔎 Busca Inteligente
- **Busca por nome** de campo (ex: `wt9_UnidadeNegocio`)
- **Busca por valor** de atributo
- **Filtros automáticos** para campos relevantes
- **Resultados organizados** por tipo

### 📝 Geração Automática de Código XSLT
- **Código pronto para uso** no formato que você especificou
- **Múltiplas alternativas** de seletores XPath
- **Comentários explicativos** para cada campo
- **Suporte a namespace** PLMXML

### 💾 Gerenciamento de Código
- **Cópia para clipboard** com um clique
- **Salvamento em arquivo** .xslt
- **Organização por campos** encontrados
- **Exportação completa** de todos os campos

## 📖 Guia de Uso

### 1. Selecionar Arquivo PLMXML
1. Clique em "Selecionar Arquivo PLMXML"
2. Escolha seu arquivo `.xml` ou `.plmxml`
3. Clique em "🔍 Extrair Campos"

### 2. Buscar Campo Específico
1. Digite o nome do campo (ex: `wt9_UnidadeNegocio`)
2. Clique em "🔍 Buscar e Gerar XSLT"
3. O código XSLT será gerado automaticamente

### 3. Visualizar Todos os Campos
1. Clique em "📋 Mostrar Todos os Campos"
2. Veja todos os campos encontrados na lista
3. Dê duplo clique em qualquer campo para gerar código

### 4. Copiar/Salvar Código
1. Use "📋 Copiar Código" para clipboard
2. Use "💾 Salvar Arquivo" para salvar em .xslt

## 🎯 Exemplo de Uso

### Busca por: `wt9_UnidadeNegocio`

**Código XSLT Gerado:**
```xml
<!-- Campo 1: wt9_UnidadeNegocio -->
<xsl:value-of select="$rootProductRevision/plm:UserData/plm:UserValue[@title='wt9_UnidadeNegocio']/@value"/>

<!-- Alternativas: -->
<xsl:value-of select="//plm:UserValue[@title='wt9_UnidadeNegocio']/@value"/>
<xsl:value-of select="//*[@title='wt9_UnidadeNegocio']/@value"/>

<!-- Se precisar do elemento completo: -->
<xsl:copy-of select="//plm:UserValue[@title='wt9_UnidadeNegocio']"/>
```

## 📊 Abas da Interface

### 📋 Campos Encontrados
- Lista todos os campos extraídos do PLMXML
- Organizados por tipo (UserValue, Atributo)
- Duplo clique gera código XSLT
- Mostra valores e caminhos

### 📝 Código XSLT
- Área de texto para código gerado
- Botões para copiar e salvar
- Formatação automática
- Comentários explicativos

### 🌳 Estrutura PLMXML
- Visualização hierárquica completa
- Atributos e valores de cada elemento
- Navegação em árvore
- Busca visual na estrutura

## 🔧 Tipos de Campos Suportados

### UserValue (Campos Personalizados)
```xml
<plm:UserValue title="wt9_UnidadeNegocio" value="Engenharia"/>
```
**Código gerado:**
```xml
<xsl:value-of select="$rootProductRevision/plm:UserData/plm:UserValue[@title='wt9_UnidadeNegocio']/@value"/>
```

### Atributos Gerais
```xml
<plm:ProductRevision name="PROD-001" id="12345"/>
```
**Código gerado:**
```xml
<xsl:value-of select="//plm:ProductRevision/@name"/>
<xsl:value-of select="//plm:ProductRevision/@id"/>
```

## 🎨 Recursos Avançados

### Busca Inteligente
- **Case-insensitive**: Não diferencia maiúsculas/minúsculas
- **Busca parcial**: Encontra campos que contenham o termo
- **Múltiplos resultados**: Lista todos os campos encontrados
- **Filtros automáticos**: Foca em campos relevantes

### Geração de Código
- **Múltiplas alternativas**: Diferentes formas de acessar o campo
- **Namespace correto**: Usa namespace PLMXML adequado
- **Comentários explicativos**: Cada campo tem comentário
- **Código pronto**: Pode ser usado diretamente no XSLT

### Exportação
- **Clipboard**: Copia para área de transferência
- **Arquivo .xslt**: Salva em arquivo XSLT
- **Arquivo .xml**: Salva em arquivo XML
- **Formatação**: Código bem formatado

## 🚨 Solução de Problemas

### Arquivo não é reconhecido
- Verifique se é um arquivo PLMXML válido
- Confirme se tem extensão `.xml` ou `.plmxml`
- Verifique se o arquivo não está corrompido

### Nenhum campo encontrado
- O arquivo pode não ter campos UserValue
- Verifique se há atributos `title`, `name`, `id`, `value`
- Use "Mostrar Todos os Campos" para ver o que foi extraído

### Código XSLT não funciona
- Verifique se o namespace está correto no seu XSLT
- Confirme se a variável `$rootProductRevision` existe
- Teste as alternativas fornecidas

## 📈 Próximas Melhorias

- [ ] Suporte a templates XSLT
- [ ] Geração de relatórios completos
- [ ] Validação de código XSLT
- [ ] Integração com editores de código
- [ ] Suporte a múltiplos arquivos
- [ ] Histórico de campos utilizados

## 🤝 Contribuição

Para contribuir com melhorias no gerador de XSLT:

1. Fork o projeto
2. Crie uma branch para sua feature
3. Implemente as melhorias
4. Teste com diferentes arquivos PLMXML
5. Envie um pull request

---

**Desenvolvido para facilitar o mapeamento de campos PLMXML para XSLT** 🎯 