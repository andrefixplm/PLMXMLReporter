# 🎯 Guia Personalizado - Gerador XSLT para seu Padrão

## 📋 Análise do seu XSL

Baseado no seu arquivo `SAIDA_TESTE10.xsl`, identifiquei o padrão que você usa:

### 🔍 Padrão Principal
```xml
<xsl:value-of select="$rootProductRevision/plm:UserData/plm:UserValue[@title='wt9_UnidadeNegocio']/@value"/>
```

### 🎯 Campos wt9_ Identificados no seu XSL
- `wt9_UnidadeNegocio`
- `wt9_TipoSolicitacao`
- `wt9_Cliente`
- `wt9_Prazo`
- `wt9_Gargalo`
- `wt9_Pinca`
- `wt9_Formato`
- `wt9_Processo`
- `wt9_AlturaMolde`
- `wt9_AlturaFundo`
- `wt9_AlturaNeckAnel`
- `wt9_AlturaTotal`
- `wt9_AlturaTotalFrasco`
- `wt9_DesenhoTerminacao`
- `wt9_SuporteBlowMold`
- `wt9_SuporteBlankMold`
- `wt9_SuporteNeckRing`
- `wt9_SuporteFunil`
- `wt9_Thimble`
- `wt9_NQI`
- `wt9_Secoes`
- `wt9_Velocidade`
- `wt9_Eficiencia`

## 🚀 Como Usar o Gerador Melhorado

### 1. **Executar o Gerador**
```bash
# Windows
iniciar_xslt_generator.bat

# Linux/Mac
python3 xslt_generator_runner.py
```

### 2. **Selecionar seu Arquivo PLMXML**
- Clique em "Selecionar Arquivo PLMXML"
- Escolha o arquivo que contém os dados
- Clique em "🔍 Extrair Campos"

### 3. **Buscar Campo Específico**
- Digite: `wt9_UnidadeNegocio`
- Clique em "🔍 Buscar e Gerar XSLT"

### 4. **Ver Todos os Campos wt9_**
- Clique em "🎯 Apenas Campos wt9_"
- Veja todos os campos que seguem seu padrão

## 📝 Exemplo de Código Gerado

### Para campo `wt9_UnidadeNegocio`:
```xml
<!-- Campo wt9_: wt9_UnidadeNegocio -->
<!-- Uso direto: -->
<xsl:value-of select="$rootProductRevision/plm:UserData/plm:UserValue[@title='wt9_UnidadeNegocio']/@value"/>

<!-- Uso em condições (como no seu XSL): -->
<xsl:choose>
    <xsl:when test="$rootProductRevision/plm:UserData/plm:UserValue[@title='wt9_UnidadeNegocio']/@value != ''">
        <xsl:value-of select="$rootProductRevision/plm:UserData/plm:UserValue[@title='wt9_UnidadeNegocio']/@value"/>
    </xsl:when>
    <xsl:otherwise>Valor padrão</xsl:otherwise>
</xsl:choose>

<!-- Alternativas para diferentes contextos: -->
<xsl:value-of select="$frascoDesign/plm:UserData/plm:UserValue[@title='wt9_UnidadeNegocio']/@value"/>
<xsl:value-of select="$rootMasterForm/plm:UserData/plm:UserValue[@title='wt9_UnidadeNegocio']/@value"/>
```

## 🎯 Funcionalidades Específicas

### ✅ **Detecção Automática de Campos wt9_**
- O gerador identifica automaticamente campos que começam com `wt9_`
- Estes campos são destacados com 🎯 na lista

### ✅ **Geração de Código Específico**
- Código baseado no seu padrão exato
- Inclui condições `<xsl:choose>` como você usa
- Oferece alternativas para diferentes contextos

### ✅ **Múltiplas Variáveis**
- `$rootProductRevision` (principal)
- `$frascoDesign` (para dados do frasco)
- `$rootMasterForm` (para dados do formulário)

## 🔧 Padrões Identificados no seu XSL

### 1. **Acesso Principal**
```xml
$rootProductRevision/plm:UserData/plm:UserValue[@title='CAMPO']/@value
```

### 2. **Uso em Condições**
```xml
<xsl:when test="$rootProductRevision/plm:UserData/plm:UserValue[@title='CAMPO']/@value != ''">
    <xsl:value-of select="$rootProductRevision/plm:UserData/plm:UserValue[@title='CAMPO']/@value"/>
</xsl:when>
<xsl:otherwise>Valor padrão</xsl:otherwise>
```

### 3. **Alternativas por Contexto**
```xml
<!-- Para dados do frasco -->
$frascoDesign/plm:UserData/plm:UserValue[@title='CAMPO']/@value

<!-- Para dados do formulário -->
$rootMasterForm/plm:UserData/plm:UserValue[@title='CAMPO']/@value
```

## 📊 Campos Organizados por Categoria

### 📋 **Informações Básicas**
- `wt9_UnidadeNegocio`
- `wt9_TipoSolicitacao`
- `wt9_Cliente`
- `wt9_Prazo`

### 📏 **Dimensões**
- `wt9_Gargalo`
- `wt9_Pinca`
- `wt9_Formato`
- `wt9_AlturaMolde`
- `wt9_AlturaFundo`
- `wt9_AlturaNeckAnel`
- `wt9_AlturaTotal`
- `wt9_AlturaTotalFrasco`

### ⚙️ **Processo e Equipamento**
- `wt9_Processo`
- `wt9_SuporteBlowMold`
- `wt9_SuporteBlankMold`
- `wt9_SuporteNeckRing`
- `wt9_SuporteFunil`
- `wt9_Thimble`
- `wt9_NQI`
- `wt9_Secoes`
- `wt9_Velocidade`
- `wt9_Eficiencia`

### 📄 **Documentação**
- `wt9_DesenhoTerminacao`

## 🎉 Benefícios do Gerador Personalizado

### ✅ **Código Pronto para Usar**
- Gera exatamente o padrão que você usa
- Inclui condições e alternativas
- Comentários explicativos

### ✅ **Economia de Tempo**
- Não precisa digitar manualmente
- Evita erros de digitação
- Padrão consistente

### ✅ **Flexibilidade**
- Múltiplas formas de acesso
- Adaptável a diferentes contextos
- Fácil de copiar e colar

## 🚀 Próximos Passos

1. **Teste o gerador** com seu arquivo PLMXML
2. **Busque campos específicos** que você precisa
3. **Copie o código gerado** para seu XSL
4. **Ajuste conforme necessário** para seu contexto específico

---

**Desenvolvido especificamente para seu padrão XSL** 🎯 