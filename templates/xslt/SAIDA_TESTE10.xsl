<?xml version="1.0" encoding="UTF-8"?>
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
        
        <!-- Status do equipamento da ficha -->
        <xsl:variable name="equipmentStatus" select="normalize-space($rootMasterForm/plm:UserData/plm:UserValue[@title='equipment_status']/@value)"/>

        <html>
            <head>
                <title>Ficha de Equipamento - <xsl:value-of select="$rootProduct/@productId"/> (<xsl:value-of select="$rootProductRevision/@revision"/>)</title>
                <style>
                    body { 
                        font-family: Arial, sans-serif; 
                        font-size: 10pt; 
                        margin: 20px; 
                        background: white;
                    }
                    
                    table { 
                        border-collapse: collapse; 
                        width: 100%; 
                        margin-bottom: 10px; 
                        table-layout: fixed; 
                    }
                    
                    th, td { 
                        border: 1px solid #333; 
                        padding: 4px 6px; 
                        vertical-align: top; 
                        word-wrap: break-word; 
                        font-size: 9pt;
                    }
                    
                    th { 
                        background-color: #E8E8E8; 
                        font-weight: bold; 
                        text-align: center; 
                        font-size: 8pt;
                    }
                    
                    .section-title { 
                        font-size: 12pt; 
                        font-weight: bold; 
                        text-align: center; 
                        background-color: #E8E8E8; 
                        border: 2px solid #333; 
                        padding: 8px; 
                        margin: 15px 0 5px 0;
                        letter-spacing: 2px; 
                    }
                    
                    .header-table td { 
                        border: 1px solid #333; 
                        padding: 3px 5px;
                        height: 18px;
                    }
                    
                    .label { 
                        font-weight: bold; 
                        font-size: 8pt;
                    }
                    
                    .center { 
                        text-align: center; 
                    }
                    
                    .bom-table th { 
                        font-size: 8pt; 
                        padding: 5px 3px;
                    }
                    
                    .bom-table td { 
                        font-size: 8pt; 
                        padding: 3px 5px;
                    }
                    
                    .level-indent { 
                        display: inline-block; 
                    }
                    
                    .dimensions-table td {
                        text-align: center; 
                        font-size: 8pt;
                        padding: 2px 4px;
                    }
                    
                    .checkbox-section td {
                        text-align: center; 
                        font-weight: bold;
                        font-size: 8pt;
                        padding: 5px;
                    }
                    
                    .equipment-variable td {
                        font-size: 8pt; 
                        padding: 3px 5px;
                    }
                    
                    .no-border {
                        border: none !important; 
                    }
                    
                    .thick-border {
                        border: 2px solid #333 !important; 
                    }
                </style>
            </head>
            <body>
                <!-- Cabeçalho com logo e número do pedido -->
                <table style="width: 100%; border: 2px solid #333; margin-bottom: 10px; border-collapse: collapse;">
                    <tr>
                        <td style="width: 20%; text-align: center; padding: 10px; border-right: 1px solid #333;">
						<img src="data:image/png;base64,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" 
     style="width: 180px; height: 60px;" alt="Wheaton Logo"/>
                        </td>
                        <td style="width: 60%; text-align: center; padding: 10px;">
                            <div style="font-size: 14pt; font-weight: bold; margin-bottom: 5px;">
                                FICHA DE EQUIPAMENTO 
                                <xsl:if test="$rootProductRevision/plm:UserData/plm:UserValue[@title='wt9_TipoSolicitacao']/@value != ''">
                                    [<xsl:value-of select="$rootProductRevision/plm:UserData/plm:UserValue[@title='wt9_TipoSolicitacao']/@value"/>]
                                </xsl:if>
                            </div>
                            <div style="font-size: 10pt; font-weight: bold;">FP-DTP-154 Rev 4.0</div>
                        </td>
                        <td style="width: 20%; text-align: center; padding: 10px; border-left: 1px solid #333;">
                            <div style="font-size: 10pt; font-weight: bold;">NÚMERO DO PEDIDO:</div>
                            <div style="font-size: 12pt; font-weight: bold; margin-top: 5px;">
                                <xsl:value-of select="$rootProduct/@productId"/>
                            </div>
                        </td>
                    </tr>
                </table>
                
                <!-- Cabeçalho principal -->
                <table class="header-table">
                    <colgroup>
                        <col style="width:8%"/>
                        <col style="width:12%"/>
                        <col style="width:18%"/>
                        <col style="width:15%"/>
                        <col style="width:10%"/>
                        <col style="width:37%"/>
                    </colgroup>
                    <tr>
                        <td><span class="label">DATA:</span></td>
                        <td><xsl:value-of select="substring(/plm:PLMXML/@date,1,10)"/></td>
                        <td><span class="label">UNIDADE DE NEGÓCIO:</span></td>
                        <td>
                            <xsl:choose>
                                <xsl:when test="$rootProductRevision/plm:UserData/plm:UserValue[@title='wt9_UnidadeNegocio']/@value != ''">
                                    <xsl:value-of select="$rootProductRevision/plm:UserData/plm:UserValue[@title='wt9_UnidadeNegocio']/@value"/>
                                </xsl:when>
                                <xsl:otherwise><xsl:value-of select="$siteElement/@name"/></xsl:otherwise>
                            </xsl:choose>
                        </td>
                        <td><span class="label">PREFIXO:</span></td>
                        <td><xsl:value-of select="$rootProduct/@productId"/></td>
                    </tr>
                    <tr>
                        <td><span class="label">CLIENTE:</span></td>
                        <td>
                            <xsl:choose>
							<xsl:when test="//plm:UserValue[@title='wt9_Cliente']/@value != ''">
								<xsl:value-of select="//plm:UserValue[@title='wt9_Cliente']/@value"/>
							</xsl:when>
                                <xsl:otherwise><xsl:value-of select="$rootMasterForm/plm:UserData/plm:UserValue[@title='project_id']/@value"/></xsl:otherwise>
                            </xsl:choose>
                        </td>
                        <td><span class="label">NOME DO PRODUTO:</span></td>
                        <td colspan="3">
                            <xsl:choose>
                                <xsl:when test="$frascoDesign/@name != ''">
                                    <xsl:value-of select="$frascoDesign/@name"/>
                                </xsl:when>
                                <xsl:otherwise><xsl:value-of select="$rootProductRevision/@name"/></xsl:otherwise>
                            </xsl:choose>
                        </td>
                    </tr>
                    <tr>
                        <td><span class="label">PRAZO:</span></td>
                        <td>
                            <xsl:choose>
                                <xsl:when test="$rootProductRevision/plm:UserData/plm:UserValue[@title='wt9_Prazo']/@value != ''">
                                    <xsl:value-of select="substring($rootProductRevision/plm:UserData/plm:UserValue[@title='wt9_Prazo']/@value,1,10)"/>
                                </xsl:when>
                                <xsl:otherwise>15/01/2024</xsl:otherwise>
                            </xsl:choose>
                        </td>
                        <td><span class="label">PESO (g):</span></td>
                        <td>
                            <xsl:choose>
                                <xsl:when test="$frascoDesign/plm:UserData/plm:UserValue[@title='wt9_Peso']/@value != ''">
                                    <xsl:value-of select="$frascoDesign/plm:UserData/plm:UserValue[@title='wt9_Peso']/@value"/>
                                </xsl:when>
                                <xsl:otherwise>195,0</xsl:otherwise>
                            </xsl:choose>
                        </td>
                        <td><span class="label">Ø GARGALO:</span></td>
                        <td>
                            <xsl:value-of select="$rootProductRevision/plm:UserData/plm:UserValue[@title='wt9_Gargalo']/@value"/>
                        </td>
                    </tr>
                    <tr>
                        <td><span class="label">CAPAC. (cm³):</span></td>
                        <td>
                            <xsl:choose>
                                <xsl:when test="$frascoDesign/plm:UserData/plm:UserValue[@title='wt9_CapacidadePratica']/@value != ''">
                                    <xsl:value-of select="$frascoDesign/plm:UserData/plm:UserValue[@title='wt9_CapacidadePratica']/@value"/>±3,0
                                </xsl:when>
                                <xsl:otherwise>110,0±3,0</xsl:otherwise>
                            </xsl:choose>
                        </td>
                        <td><span class="label">Ø PINÇA:</span></td>
                        <td>
                            <xsl:value-of select="$rootProductRevision/plm:UserData/plm:UserValue[@title='wt9_Pinca']/@value"/>
                        </td>
                        <td><span class="label">FORMATO:</span></td>
                        <td>
                            <xsl:choose>
                                <xsl:when test="$rootProductRevision/plm:UserData/plm:UserValue[@title='wt9_Formato']/@value != ''">
                                    <xsl:value-of select="$rootProductRevision/plm:UserData/plm:UserValue[@title='wt9_Formato']/@value"/>
                                </xsl:when>
                                <xsl:otherwise><xsl:value-of select="$rootMasterForm/plm:UserData/plm:UserValue[@title='user_data_1']/@value"/></xsl:otherwise>
                            </xsl:choose>
                        </td>
                    </tr>
                    <tr>
                        <td colspan="2"></td>
                        <td><span class="label">PROCESSO:</span></td>
                        <td colspan="3">
                            <xsl:choose>
                                <xsl:when test="$rootProductRevision/plm:UserData/plm:UserValue[@title='wt9_Processo']/@value != ''">
                                    <xsl:value-of select="$rootProductRevision/plm:UserData/plm:UserValue[@title='wt9_Processo']/@value"/>
                                </xsl:when>
                                <xsl:otherwise>SG</xsl:otherwise>
                            </xsl:choose>
                        </td>
                    </tr>
                </table>



                <!-- Seção de Dimensões -->
                <div class="section-title">DIMENSÕES</div>
                <table class="dimensions-table">
                    <colgroup>
                        <col style="width:12%"/>
                        <col style="width:12%"/>
                        <col style="width:12%"/>
                        <col style="width:12%"/>
                        <col style="width:12%"/>
                        <col style="width:40%"/>
                    </colgroup>
                    <thead>
                        <tr>
                            <th>DIMENSÕES</th>
                            <th>ALTURA</th>
                            <th>DIÂMETRO</th>
                            <th>LARGURA</th>
                            <th>ESPESSURA</th>
                            <th>OBSERVAÇÃO</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td><strong>MÍNIMA (mm):</strong></td>
                            <td>
                                <xsl:value-of select="$frascoDesign/plm:UserData/plm:UserValue[@title='wt9_AlturaMinima']/@value"/>
                            </td>
                            <td>
                                <xsl:value-of select="$frascoDesign/plm:UserData/plm:UserValue[@title='wt9_DiametroMinimo']/@value"/>
                            </td>
                            <td>
                                <xsl:value-of select="$frascoDesign/plm:UserData/plm:UserValue[@title='wt9_LarguraMinima']/@value"/>
                            </td>
                            <td>
                                <xsl:value-of select="$frascoDesign/plm:UserData/plm:UserValue[@title='wt9_EspessuraMinima']/@value"/>
                            </td>
                            <td><strong>AMOSTRA 1</strong></td>
                        </tr>
                        <tr>
                            <td><strong>MÁXIMA (mm):</strong></td>
                            <td>
                                <xsl:value-of select="$frascoDesign/plm:UserData/plm:UserValue[@title='wt9_AlturaMaxima']/@value"/>
                            </td>
                            <td>
                                <xsl:value-of select="$frascoDesign/plm:UserData/plm:UserValue[@title='wt9_DiametroMaximo']/@value"/>
                            </td>
                            <td>
                                <xsl:value-of select="$frascoDesign/plm:UserData/plm:UserValue[@title='wt9_LarguraMaxima']/@value"/>
                            </td>
                            <td>
                                <xsl:value-of select="$frascoDesign/plm:UserData/plm:UserValue[@title='wt9_EspessuraMaxima']/@value"/>
                            </td>
                            <td></td>
                        </tr>
                        <tr>
                            <td><strong>Somatória Altura</strong></td>
                            <td><strong>Molde</strong></td>
                            <td><strong>Fundo</strong></td>
                            <td><strong>(Neck+Anel)</strong></td>
                            <td><strong>Total</strong></td>
                            <td><strong>Altura Total Ideal do Frasco</strong></td>
                        </tr>
                        <tr>
                            <td><strong>Total Frasco</strong></td>
                            <td><xsl:value-of select="$rootProductRevision/plm:UserData/plm:UserValue[@title='wt9_AlturaMolde']/@value"/></td>
                            <td><xsl:value-of select="$rootProductRevision/plm:UserData/plm:UserValue[@title='wt9_AlturaFundo']/@value"/></td>
                            <td><xsl:value-of select="$rootProductRevision/plm:UserData/plm:UserValue[@title='wt9_AlturaNeckAnel']/@value"/></td>
                            <td><xsl:value-of select="$rootProductRevision/plm:UserData/plm:UserValue[@title='wt9_AlturaTotal']/@value"/></td>
                            <td><xsl:value-of select="$rootProductRevision/plm:UserData/plm:UserValue[@title='wt9_AlturaTotalFrasco']/@value"/></td>
                        </tr>
                    </tbody>
                </table>

                <!-- Linha de desenhos -->
                <table class="header-table">
                    <tr>
                        <td><strong>DES. CORPO:</strong> 
                            <xsl:choose>
                                <xsl:when test="$frascoDesign/@catalogueId != ''">
                                    <xsl:value-of select="$frascoDesign/@catalogueId"/>
                                </xsl:when>
                                <xsl:otherwise>WB-DT-8994-B</xsl:otherwise>
                            </xsl:choose>
                        </td>
                        <td><strong>DES. TERM.:</strong> 
                            <xsl:value-of select="$rootProductRevision/plm:UserData/plm:UserValue[@title='wt9_DesenhoTerminacao']/@value"/>
                        </td>
                        <td><strong>TERMINAÇÃO:</strong> FE-15-CTN</td>
                    </tr>
                </table>

                <!-- Seção de Equipamento (BOM) -->
                <div class="section-title">EQUIPAMENTO</div>
                <table class="bom-table">
                    <colgroup>
                        <col style="width:8%"/>
                        <col style="width:25%"/>
                        <col style="width:20%"/>
                        <col style="width:15%"/>
                        <col style="width:15%"/>
                        <col style="width:12%"/>
                        <col style="width:5%"/>
                    </colgroup>
                    <thead>
                        <tr>
                            <th>QTDE</th>
                            <th>DESCRIÇÃO</th>
                            <th>EQUIPAMENTO</th>
                            <th>TERMINAÇÃO</th>
                            <th>CÓDIGO DA PEÇA</th>
                            <th>OBSERVAÇÃO</th>
                            <th>VERSÃO</th>
                        </tr>
                    </thead>
                    <tbody>
                        <xsl:variable name="roe" select="/plm:PLMXML/plm:ProductView/plm:Occurrence[@id=$primaryOccRef]"/>
                        <xsl:variable name="occRefs" select="$roe/@occurrenceRefs"/>
                        <xsl:call-template name="createCL">
                            <xsl:with-param name="occStr" select="$occRefs"/>
                            <xsl:with-param name="levelID">1</xsl:with-param>
                        </xsl:call-template>
                    </tbody>
                </table>
                
                <!-- Seção de Equipamento Variável e Dados Técnicos -->
                <table class="equipment-variable">
                    <colgroup>
                        <col style="width: 20%"/>
                        <col style="width: 15%"/>
                        <col style="width: 20%"/>
                        <col style="width: 11.25%"/>
                        <col style="width: 11.25%"/>
                        <col style="width: 11.25%"/>
                        <col style="width: 11.25%"/>
                    </colgroup>
                    <tr style="background-color: #E8E8E8;">
                        <th colspan="2">EQUIPAMENTO VARIÁVEL</th>
                        <th colspan="5">DADOS TÉCNICOS</th>
                    </tr>
                    <tr style="background-color: #E8E8E8;">
					    <td colspan="2" style="border-top: 1px solid #333; padding-top: 10px;"></td>
                        <th colspan="5" style="font-size: 7pt; padding: 2px; height: 30px; vertical-align: middle;">GOTA</th>
                    </tr>
                    <tr>
                        <td colspan="2" class="no-border" style="border-bottom: 1px solid #333 !important;"></td>
                        <th style="font-size: 7pt; padding: 2px; height: 25px; vertical-align: middle;">VELOCIDADE EM FRASCOS/MINUTO</th>
                        <th style="font-size: 7pt; padding: 2px; height: 25px; vertical-align: middle;">SIMPLES</th>
                        <th style="font-size: 7pt; padding: 2px; height: 25px; vertical-align: middle;">DUPLA</th>
                        <th style="font-size: 7pt; padding: 2px; height: 25px; vertical-align: middle;">TRIPLA</th>
                        <th style="font-size: 7pt; padding: 2px; height: 25px; vertical-align: middle;">QUÁDRUPLA</th>
                    </tr>
                    <tr>
                        <td><span class="label">SUPORTE DO BLOW MOLD</span></td>
                        <td><xsl:value-of select="$rootProductRevision/plm:UserData/plm:UserValue[@title='wt9_SuporteBlowMold']/@value"/></td>
                        <td><span class="label"><xsl:value-of select="$rootProductRevision/plm:UserData/plm:UserValue[@title='wt9_Secoes']/@value"/> SEÇÕES</span></td>
                        <td><xsl:value-of select="$rootProductRevision/plm:UserData/plm:UserValue[@title='wt9_Velocidade']/@value"/></td>
                        <td></td>
                        <td></td>
                        <td></td>
                    </tr>
                    <tr>
                        <td><span class="label">SUPORTE DO BLANK MOLD</span></td>
                        <td><xsl:value-of select="$rootProductRevision/plm:UserData/plm:UserValue[@title='wt9_SuporteBlankMold']/@value"/></td>
                        <td><span class="label">4 SEÇÕES</span></td>
                        <td></td>
                        <td></td>
                        <td></td>
                        <td></td>
                    </tr>
                    <tr>
                        <td><span class="label">SUPORTE DO NECK RING</span></td>
                        <td><xsl:value-of select="$rootProductRevision/plm:UserData/plm:UserValue[@title='wt9_SuporteNeckRing']/@value"/></td>
                        <td><span class="label">6 SEÇÕES</span></td>
                        <td></td>
                        <td></td>
                        <td></td>
                        <td></td>
                    </tr>
                    <tr>
                        <td><span class="label">SUPORTE DO FUNIL</span></td>
                        <td><xsl:value-of select="$rootProductRevision/plm:UserData/plm:UserValue[@title='wt9_SuporteFunil']/@value"/></td>
                        <td><span class="label">EFICIÊNCIA COTADA(%)</span></td>
                        <td><xsl:value-of select="$rootProductRevision/plm:UserData/plm:UserValue[@title='wt9_Eficiencia']/@value"/></td>
                        <td></td>
                        <td></td>
                        <td></td>
                    </tr>
                    <tr>
                        <td><span class="label">THIMBLE</span></td>
                        <td><xsl:value-of select="$rootProductRevision/plm:UserData/plm:UserValue[@title='wt9_Thimble']/@value"/></td>
                        <td></td>
                        <td></td>
                        <td></td>
                        <td></td>
                        <td></td>
                    </tr>
                    <tr>
                        <td><span class="label">NÍVEL DE QUALIDADE</span></td>
                        <td><xsl:value-of select="$rootProductRevision/plm:UserData/plm:UserValue[@title='wt9_NQI']/@value"/></td>
                        <td></td>
                        <td></td>
                        <td></td>
                        <td></td>
                        <td></td>
                    </tr>
                </table>

            </body>
        </html>
    </xsl:template>

    <!-- Template para processar componentes da BOM -->
    <xsl:template name="createCL">
        <xsl:param name="occStr"/>
        <xsl:param name="levelID"/>
        <xsl:if test="string-length($occStr) > 0">
            <xsl:choose>
                <xsl:when test="contains($occStr,' ')">
                    <xsl:variable name="occid" select="substring-before($occStr,' ')"/>
                    <xsl:call-template name="createCL">
                        <xsl:with-param name="occStr" select="$occid"/>
                        <xsl:with-param name="levelID" select="$levelID"/>
                    </xsl:call-template>
                    <xsl:call-template name="createCL">
                        <xsl:with-param name="occStr" select="substring-after($occStr,' ')"/>
                        <xsl:with-param name="levelID" select="$levelID"/>
                    </xsl:call-template>
                </xsl:when>
                <xsl:otherwise>
                    <xsl:call-template name="creCLext">
                        <xsl:with-param name="occID" select="$occStr"/>
                        <xsl:with-param name="levelid" select="$levelID"/>
                    </xsl:call-template>
                </xsl:otherwise>
            </xsl:choose>
        </xsl:if>
    </xsl:template>

    <xsl:template name="creCLext">
        <xsl:param name="occID"/>
        <xsl:param name="levelid"/>
        <xsl:variable name="occele" select="/plm:PLMXML/plm:ProductView/plm:Occurrence[@id=$occID]"/>
        <xsl:variable name="occRefsId" select="$occele/@occurrenceRefs"/>
        <xsl:variable name="prtid" select="substring-after($occele/@instancedRef,'#')"/>
        <xsl:variable name="prteleProduct" select="/plm:PLMXML/plm:ProductRevision[@id=$prtid]"/>
        <xsl:variable name="prteleDes" select="/plm:PLMXML/plm:DesignRevision[@id=$prtid]"/>
        <xsl:variable name="prtelePart" select="/plm:PLMXML/plm:PartRevision[@id=$prtid]"/>
        
        <xsl:choose>
            <xsl:when test="$prteleProduct">
                <xsl:call-template name="ChildComponentsExt">
                    <xsl:with-param name="occid" select="$occID"/>
                    <xsl:with-param name="level" select="$levelid"/>
                    <xsl:with-param name="prtele" select="$prteleProduct"/>
                    <xsl:with-param name="occRefs" select="$occRefsId"/>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$prteleDes">
                <xsl:call-template name="ChildComponentsExt">
                    <xsl:with-param name="occid" select="$occID"/>
                    <xsl:with-param name="level" select="$levelid"/>
                    <xsl:with-param name="prtele" select="$prteleDes"/>
                    <xsl:with-param name="occRefs" select="$occRefsId"/>
                </xsl:call-template>
            </xsl:when>
            <xsl:when test="$prtelePart">
                <xsl:call-template name="ChildComponentsExt">
                    <xsl:with-param name="occid" select="$occID"/>
                    <xsl:with-param name="level" select="$levelid"/>
                    <xsl:with-param name="prtele" select="$prtelePart"/>
                    <xsl:with-param name="occRefs" select="$occRefsId"/>
                </xsl:call-template>
            </xsl:when>
        </xsl:choose>
    </xsl:template>
    
    <xsl:template name="ChildComponentsExt">
        <xsl:param name="occid"/>
        <xsl:param name="level"/>
        <xsl:param name="prtele"/>
        <xsl:param name="occRefs"/>

        <xsl:variable name="childProduct" select="key('productById', substring-after($prtele/@masterRef, '#'))"/>
        <xsl:variable name="itemID" select="$childProduct/@productId"/>
        <xsl:variable name="itemRev" select="$prtele/@revision"/>
        <xsl:variable name="itemName" select="$prtele/@name"/>
        <xsl:variable name="formRef" select="$prtele/plm:AssociatedForm[@role='IMAN_master_form']/@formRef"/>
        <xsl:variable name="form" select="key('formById',substring-after($formRef,'#'))"/>
        <xsl:variable name="currentOccurrence" select="key('occurrenceById', $occid)"/>
        <xsl:variable name="sequenceNumber" select="$currentOccurrence/plm:UserData/plm:UserValue[@title='SequenceNumber']/@value"/>
         
        <xsl:variable name="quantity">
            <xsl:choose>
                <xsl:when test="$sequenceNumber != ''">
                    <xsl:value-of select="floor($sequenceNumber div 10)"/>
                </xsl:when>
                <xsl:otherwise>1</xsl:otherwise>
            </xsl:choose>
        </xsl:variable>
        
        <tr>
            <td style="text-align: center;">
                <xsl:value-of select="$quantity"/>
            </td>
            <td>
                <xsl:value-of select="$itemName"/>
            </td>
            <td>
                <span class="level-indent" style="padding-left: {($level - 1) * 10}px;"></span>
                <xsl:value-of select="$itemID"/>/<xsl:value-of select="$itemRev"/>
            </td>
            <td>
                <xsl:choose>
                    <xsl:when test="$childProduct/@productId">
                        <xsl:value-of select="$childProduct/@productId"/>
                    </xsl:when>
                    <xsl:otherwise>-</xsl:otherwise>
                </xsl:choose>
            </td>
            <td>
                <xsl:value-of select="$itemID"/>
            </td>
            <td>
                <xsl:choose>
                    <xsl:when test="contains($itemName, 'FAZER')">FAZER</xsl:when>
                    <xsl:when test="contains($itemName, 'STANDARD')">STANDARD</xsl:when>
                    <xsl:otherwise>-</xsl:otherwise>
                </xsl:choose>
            </td>
            <td>
                <xsl:choose>
                    <xsl:when test="contains($itemName, 'V-1.') or contains($itemName, 'V-2.')">
                        <xsl:value-of select="substring-after($itemName, 'V-')"/>
                    </xsl:when>
                    <xsl:otherwise>V-1.0</xsl:otherwise>
                </xsl:choose>
            </td>
        </tr>

        <xsl:if test="$occRefs!=''">
            <xsl:call-template name="createCL">
                <xsl:with-param name="occStr" select="$occRefs"/>
                <xsl:with-param name="levelID" select="$level + 1"/>
            </xsl:call-template>
        </xsl:if>
    </xsl:template>

    <!-- Templates vazios para ignorar elementos não processados -->
    <xsl:template match="text()"/>
    <xsl:template match="plm:Header|plm:Product|plm:ProductRevision[not(ancestor::plm:PLMXML)]|plm:Form|plm:AssociatedForm|plm:ApplicationRef|plm:UserData|plm:UserValue|plm:Transform|plm:AttributeContext|plm:ProductView|plm:RevisionRule|plm:AccessIntent|plm:Site|plm:Text|plm:Item"/>

</xsl:stylesheet>