<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:output method="html" version="1.0" encoding="UTF-8" indent="yes"/>
    
    <!-- Template principal -->
    <xsl:template match="/">
        <html>
            <head>
                <title>Relatório PLMXML - Teamcenter Data</title>
                <style>
                    body {
                        font-family: Arial, sans-serif;
                        margin: 20px;
                        background-color: #f5f5f5;
                    }
                    .container {
                        max-width: 1200px;
                        margin: 0 auto;
                        background-color: white;
                        padding: 20px;
                        border-radius: 8px;
                        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                    }
                    .header {
                        background-color: #2c3e50;
                        color: white;
                        padding: 20px;
                        border-radius: 5px;
                        margin-bottom: 20px;
                    }
                    .section {
                        margin-bottom: 30px;
                        border: 1px solid #ddd;
                        border-radius: 5px;
                        overflow: hidden;
                    }
                    .section-header {
                        background-color: #3498db;
                        color: white;
                        padding: 10px 15px;
                        font-weight: bold;
                    }
                    .content {
                        padding: 15px;
                    }
                    table {
                        width: 100%;
                        border-collapse: collapse;
                        margin-top: 10px;
                    }
                    th, td {
                        border: 1px solid #ddd;
                        padding: 8px;
                        text-align: left;
                    }
                    th {
                        background-color: #ecf0f1;
                        font-weight: bold;
                    }
                    tr:nth-child(even) {
                        background-color: #f9f9f9;
                    }
                    .stats {
                        display: flex;
                        justify-content: space-around;
                        margin: 20px 0;
                    }
                    .stat-box {
                        background-color: #e8f4fd;
                        padding: 15px;
                        border-radius: 5px;
                        text-align: center;
                        flex: 1;
                        margin: 0 10px;
                    }
                    .stat-number {
                        font-size: 24px;
                        font-weight: bold;
                        color: #2980b9;
                    }
                    .stat-label {
                        color: #7f8c8d;
                        font-size: 14px;
                    }
                    .item-card {
                        border: 1px solid #ddd;
                        border-radius: 5px;
                        padding: 15px;
                        margin: 10px 0;
                        background-color: #fafafa;
                    }
                    .item-title {
                        font-weight: bold;
                        color: #2c3e50;
                        margin-bottom: 10px;
                    }
                    .item-details {
                        color: #7f8c8d;
                        font-size: 14px;
                    }
                    .bom-tree {
                        margin-left: 20px;
                    }
                    .bom-item {
                        padding: 5px 0;
                        border-left: 2px solid #3498db;
                        padding-left: 10px;
                        margin: 5px 0;
                    }
                </style>
            </head>
            <body>
                <div class="container">
                    <!-- Cabeçalho -->
                    <div class="header">
                        <h1>📊 Relatório PLMXML - Teamcenter Data</h1>
                        <p>Relatório gerado automaticamente a partir dos dados extraídos</p>
                    </div>
                    
                    <!-- Estatísticas Gerais -->
                    <div class="section">
                        <div class="section-header">
                            📈 Estatísticas Gerais
                        </div>
                        <div class="content">
                            <div class="stats">
                                <div class="stat-box">
                                    <div class="stat-number">
                                        <xsl:value-of select="TeamcenterData/Resumo/@totalItens"/>
                                    </div>
                                    <div class="stat-label">Total de Itens</div>
                                </div>
                                <div class="stat-box">
                                    <div class="stat-number">
                                        <xsl:value-of select="TeamcenterData/Resumo/@totalLinhasBOM"/>
                                    </div>
                                    <div class="stat-label">Linhas BOM</div>
                                </div>
                                <div class="stat-box">
                                    <div class="stat-number">
                                        <xsl:value-of select="TeamcenterData/Metadados/xml/total_elementos"/>
                                    </div>
                                    <div class="stat-label">Elementos XML</div>
                                </div>
                            </div>
                        </div>
                    </div>
                    
                    <!-- Metadados -->
                    <xsl:if test="TeamcenterData/Metadados">
                        <div class="section">
                            <div class="section-header">
                                📋 Metadados do Arquivo
                            </div>
                            <div class="content">
                                <table>
                                    <tr>
                                        <th>Propriedade</th>
                                        <th>Valor</th>
                                    </tr>
                                    <tr>
                                        <td>Nome do Arquivo</td>
                                        <td><xsl:value-of select="TeamcenterData/Metadados/arquivo/nome"/></td>
                                    </tr>
                                    <tr>
                                        <td>Tamanho</td>
                                        <td><xsl:value-of select="format-number(TeamcenterData/Metadados/arquivo/tamanho_mb, '#.##')"/> MB</td>
                                    </tr>
                                    <tr>
                                        <td>Data de Modificação</td>
                                        <td><xsl:value-of select="TeamcenterData/Metadados/arquivo/data_modificacao"/></td>
                                    </tr>
                                    <tr>
                                        <td>Elemento Raiz</td>
                                        <td><xsl:value-of select="TeamcenterData/Metadados/xml/elemento_raiz"/></td>
                                    </tr>
                                    <tr>
                                        <td>Profundidade Máxima</td>
                                        <td><xsl:value-of select="TeamcenterData/Metadados/xml/profundidade_maxima"/> níveis</td>
                                    </tr>
                                </table>
                            </div>
                        </div>
                    </xsl:if>
                    
                    <!-- Itens -->
                    <xsl:if test="TeamcenterData/Itens/Item">
                        <div class="section">
                            <div class="section-header">
                                📦 Itens Encontrados (<xsl:value-of select="count(TeamcenterData/Itens/Item)"/>)
                            </div>
                            <div class="content">
                                <xsl:for-each select="TeamcenterData/Itens/Item">
                                    <div class="item-card">
                                        <div class="item-title">
                                            <xsl:value-of select="@nome"/> 
                                            <span style="color: #7f8c8d; font-size: 12px;">
                                                (ID: <xsl:value-of select="@id"/>)
                                            </span>
                                        </div>
                                        <div class="item-details">
                                            <strong>Tipo:</strong> <xsl:value-of select="@tipo"/><br/>
                                            <xsl:if test="AtributosBasicos/Atributo">
                                                <strong>Atributos:</strong><br/>
                                                <xsl:for-each select="AtributosBasicos/Atributo">
                                                    • <xsl:value-of select="@nome"/>: <xsl:value-of select="@valor"/><br/>
                                                </xsl:for-each>
                                            </xsl:if>
                                            <xsl:if test="Propriedades/Propriedade">
                                                <strong>Propriedades:</strong><br/>
                                                <xsl:for-each select="Propriedades/Propriedade">
                                                    • <xsl:value-of select="@nome"/>: <xsl:value-of select="@valor"/><br/>
                                                </xsl:for-each>
                                            </xsl:if>
                                        </div>
                                    </div>
                                </xsl:for-each>
                            </div>
                        </div>
                    </xsl:if>
                    
                    <!-- Estrutura BOM -->
                    <xsl:if test="TeamcenterData/EstruturaBOM/LinhaBOM">
                        <div class="section">
                            <div class="section-header">
                                🔗 Estrutura BOM (<xsl:value-of select="count(TeamcenterData/EstruturaBOM/LinhaBOM)"/> linhas)
                            </div>
                            <div class="content">
                                <table>
                                    <tr>
                                        <th>ID</th>
                                        <th>Pai</th>
                                        <th>Filho</th>
                                        <th>Quantidade</th>
                                        <th>Find Number</th>
                                    </tr>
                                    <xsl:for-each select="TeamcenterData/EstruturaBOM/LinhaBOM">
                                        <tr>
                                            <td><xsl:value-of select="@id"/></td>
                                            <td><xsl:value-of select="@pai"/></td>
                                            <td><xsl:value-of select="@filho"/></td>
                                            <td><xsl:value-of select="@quantidade"/></td>
                                            <td><xsl:value-of select="@findNumber"/></td>
                                        </tr>
                                    </xsl:for-each>
                                </table>
                            </div>
                        </div>
                    </xsl:if>
                    
                    <!-- Tipos de Elementos -->
                    <xsl:if test="TeamcenterData/Metadados/estrutura/tipos_elementos">
                        <div class="section">
                            <div class="section-header">
                                🏗️ Tipos de Elementos XML
                            </div>
                            <div class="content">
                                <table>
                                    <tr>
                                        <th>Tipo de Elemento</th>
                                        <th>Quantidade</th>
                                    </tr>
                                    <xsl:for-each select="TeamcenterData/Metadados/estrutura/tipos_elementos/*">
                                        <xsl:sort select="." data-type="number" order="descending"/>
                                        <tr>
                                            <td><xsl:value-of select="name()"/></td>
                                            <td><xsl:value-of select="."/></td>
                                        </tr>
                                    </xsl:for-each>
                                </table>
                            </div>
                        </div>
                    </xsl:if>
                    
                    <!-- Rodapé -->
                    <div style="text-align: center; margin-top: 30px; color: #7f8c8d; font-size: 12px;">
                        <p>Relatório gerado automaticamente pelo PLMXML Reporter</p>
                        <p>Data de geração: <xsl:value-of select="TeamcenterData/Metadados/xml/data_processamento"/></p>
                    </div>
                </div>
            </body>
        </html>
    </xsl:template>
</xsl:stylesheet> 