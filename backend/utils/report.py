"""
Geração de Relatórios PDF
Cria relatórios detalhados em PDF com os resultados da análise forense
"""

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from datetime import datetime
import os

def generate_report(filename: str, ai_probability: float, 
                   noise_analysis: dict, metadata_analysis: dict, 
                   status: str) -> str:
    """
    Gera relatório PDF completo da análise forense
    
    O relatório inclui:
    - Cabeçalho com identificação
    - Resumo executivo
    - Análise de IA detalhada
    - Análise de metadados
    - Análise de ruído
    - Conclusões e recomendações
    
    Args:
        filename: nome do arquivo analisado
        ai_probability: probabilidade de ser IA
        noise_analysis: resultado da análise de ruído
        metadata_analysis: resultado da análise de metadados
        status: status final ("Suspeita de fraude" ou "Provavelmente real")
    
    Returns:
        str: caminho do arquivo PDF gerado
    """

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_filename = f"reports/analysis_{timestamp}.pdf"

    doc = SimpleDocTemplate(report_filename, pagesize=A4)
    story = []
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1a365d'),
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#2d3748'),
        spaceAfter=12,
        spaceBefore=12,
        fontName='Helvetica-Bold'
    )

    title = Paragraph("AutoShield-AI<br/>Relatório de Análise Forense", title_style)
    story.append(title)
    story.append(Spacer(1, 0.3*inch))

    info_data = [
        ["Data/Hora:", datetime.now().strftime("%d/%m/%Y %H:%M:%S")],
        ["Arquivo Analisado:", filename],
        ["Status:", status],
    ]
    
    info_table = Table(info_data, colWidths=[2*inch, 4*inch])
    info_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#e2e8f0')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey)
    ]))
    
    story.append(info_table)
    story.append(Spacer(1, 0.3*inch))

    story.append(Paragraph("1. RESUMO EXECUTIVO", heading_style))
    
    if status == "Suspeita de fraude":
        summary_text = f"""
        <b>ALERTA DE FRAUDE:</b> A imagem analisada apresenta características suspeitas 
        de ter sido gerada artificialmente por inteligência artificial. 
        Probabilidade de IA: <b>{ai_probability*100:.1f}%</b>.
        Recomenda-se investigação adicional e não aceitação da imagem como evidência válida.
        """
        summary_color = colors.HexColor('#fed7d7')
    else:
        summary_text = f"""
        A imagem analisada apresenta características consistentes com fotografia real.
        Probabilidade de IA: <b>{ai_probability*100:.1f}%</b>.
        Análises de metadados e ruído não indicam manipulação evidente.
        """
        summary_color = colors.HexColor('#c6f6d5')
    
    summary = Paragraph(summary_text, styles['BodyText'])
    summary_table = Table([[summary]], colWidths=[6*inch])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), summary_color),
        ('PADDING', (0, 0), (-1, -1), 12),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ]))
    
    story.append(summary_table)
    story.append(Spacer(1, 0.2*inch))

    story.append(Paragraph("2. ANÁLISE DE INTELIGÊNCIA ARTIFICIAL", heading_style))
    
    ai_interpretation = ""
    if ai_probability >= 0.7:
        ai_interpretation = "ALTA probabilidade de ser imagem gerada por IA"
    elif ai_probability >= 0.4:
        ai_interpretation = "MÉDIA probabilidade de ser imagem gerada por IA"
    else:
        ai_interpretation = "BAIXA probabilidade de ser imagem gerada por IA"
    
    ai_text = f"""
    A análise usando rede neural profunda (ResNet50) identificou:
    <br/><br/>
    <b>Probabilidade de IA:</b> {ai_probability*100:.2f}%<br/>
    <b>Interpretação:</b> {ai_interpretation}<br/><br/>
    O modelo examina padrões de textura, inconsistências em detalhes, 
    artefatos de geração e distribuição de cores não naturais típicas 
    de imagens sintéticas.
    """
    
    story.append(Paragraph(ai_text, styles['BodyText']))
    story.append(Spacer(1, 0.2*inch))

    story.append(Paragraph("3. ANÁLISE DE METADADOS EXIF", heading_style))
    
    metadata_data = [
        ["Possui EXIF:", "Sim" if metadata_analysis["has_exif"] else "Não"],
        ["Modelo Câmera:", metadata_analysis.get("camera_model", "N/A") or "N/A"],
        ["Data/Hora:", metadata_analysis.get("datetime", "N/A") or "N/A"],
        ["Software:", metadata_analysis.get("software", "N/A") or "N/A"],
        ["Classificação:", "SUSPEITO" if metadata_analysis["suspicious"] else "NORMAL"],
    ]
    
    metadata_table = Table(metadata_data, colWidths=[2*inch, 4*inch])
    metadata_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#e2e8f0')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey)
    ]))
    
    story.append(metadata_table)
    story.append(Spacer(1, 0.15*inch))

    if metadata_analysis.get("details"):
        details_text = "<b>Observações:</b><br/>" + "<br/>".join([f"• {d}" for d in metadata_analysis["details"]])
        story.append(Paragraph(details_text, styles['BodyText']))
    
    story.append(Spacer(1, 0.2*inch))

    story.append(Paragraph("4. ANÁLISE DE RUÍDO DIGITAL", heading_style))
    
    noise_data = [
        ["Ruído Médio:", f"{noise_analysis['mean_noise']:.4f}"],
        ["Desvio Padrão:", f"{noise_analysis['std_noise']:.4f}"],
        ["Uniformidade:", f"{noise_analysis['uniformity']:.4f}"],
        ["Var. Artefatos JPEG:", f"{noise_analysis['jpeg_artifacts_variance']:.4f}"],
        ["Classificação:", "SUSPEITO" if noise_analysis["suspicious"] else "NORMAL"],
    ]
    
    noise_table = Table(noise_data, colWidths=[2*inch, 4*inch])
    noise_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#e2e8f0')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey)
    ]))
    
    story.append(noise_table)
    story.append(Spacer(1, 0.15*inch))

    if noise_analysis.get("details"):
        details_text = "<b>Observações:</b><br/>" + "<br/>".join([f"• {d}" for d in noise_analysis["details"]])
        story.append(Paragraph(details_text, styles['BodyText']))
    
    story.append(Spacer(1, 0.3*inch))

    story.append(Paragraph("5. CONCLUSÕES E RECOMENDAÇÕES", heading_style))
    
    if status == "Suspeita de fraude":
        conclusion = """
        <b>CONCLUSÃO:</b> Baseado nas análises de IA, metadados e ruído digital, 
        há evidências significativas de que a imagem pode ter sido gerada 
        artificialmente por inteligência artificial.<br/><br/>
        <b>RECOMENDAÇÕES:</b><br/>
        • Não aceitar a imagem como evidência válida sem verificação adicional<br/>
        • Solicitar imagens originais capturadas por dispositivo físico<br/>
        • Realizar perícia forense completa se necessário<br/>
        • Investigar origem e cadeia de custódia da imagem<br/>
        • Considerar possibilidade de tentativa de fraude
        """
    else:
        conclusion = """
        <b>CONCLUSÃO:</b> As análises realizadas indicam que a imagem é 
        provavelmente autêntica e não apresenta sinais evidentes de manipulação 
        por IA ou ferramentas de edição.<br/><br/>
        <b>RECOMENDAÇÕES:</b><br/>
        • Imagem pode ser considerada para análise no processo<br/>
        • Verificar consistência com outras evidências<br/>
        • Manter análise complementar de contexto e plausibilidade
        """
    
    story.append(Paragraph(conclusion, styles['BodyText']))
    story.append(Spacer(1, 0.3*inch))

    footer_text = """
    <i>Este relatório foi gerado automaticamente pelo sistema AutoShield-AI.
    Os resultados são indicativos e devem ser interpretados por profissional qualificado.
    AutoShield-AI não substitui perícia forense completa.</i>
    """
    story.append(Paragraph(footer_text, styles['Italic']))

    doc.build(story)
    
    return report_filename
