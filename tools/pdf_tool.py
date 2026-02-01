from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
import markdown
import os
import re

OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def header_footer(canvas, doc):
    canvas.saveState()

    # Header
    canvas.setStrokeColor(HexColor('#2E86C1'))
    canvas.setLineWidth(1)
    canvas.line(50, A4[1] - 40, A4[0] - 50, A4[1] - 40)
    
    canvas.setFont('Helvetica-Bold', 12)
    canvas.setFillColor(HexColor('#2E86C1'))
    canvas.drawString(50, A4[1] - 35, "HALIMOZ AI")

    canvas.setFont('Helvetica', 9)
    canvas.setFillColor(HexColor('#7F8C8D'))
    canvas.drawRightString(A4[0] - 50, A4[1] - 35, "Smart Video Summary")
    
    # Footer
    canvas.setFont('Helvetica', 9)
    canvas.setFillColor(HexColor('#7F8C8D'))
    canvas.drawString(A4[0]/2 - 10, 30, f"- {doc.page} -")
    canvas.restoreState()

def md_to_pdf_paragraphs(text, style):
    """transfer markdown text to list of reportlab Paragraphs"""
    #For converting markdown to HTML
    html = markdown.markdown(text)
    
    
    # formatting adjustments
    html = html.replace('<strong>', '<b>').replace('</strong>', '</b>')
    html = html.replace('<em>', '<i>').replace('</em>', '</i>')
    html = html.replace('<ul>', '').replace('</ul>', '')
    html = html.replace('<li>', '• ').replace('</li>', '<br/>')
    html = re.sub(r'<h[1-6]>', '<br/><b>', html) 
    html = re.sub(r'</h[1-6]>', '</b><br/>', html)
    
    paragraphs = []
    lines = html.split('<p>')
    for line in lines:
        line = line.replace('</p>', '').strip()
        if line:
            paragraphs.append(Paragraph(line, style))
    return paragraphs

def generate_pdf_manual(summary: str, script: str = None) -> str:
    path = f"{OUTPUT_DIR}/video_summary.pdf"
    
    doc = SimpleDocTemplate(
        path,
        pagesize=A4,
        rightMargin=50,
        leftMargin=50,
        topMargin=60,
        bottomMargin=50
    )
    
    styles = getSampleStyleSheet()
    main_title_style = ParagraphStyle(
        'MainTitle',
        parent=styles['Heading1'],
        fontSize=24,       
        leading=30,
        spaceAfter=20,
        textColor=HexColor('#2E86C1'),
        alignment=1
    )

    sub_title_style = ParagraphStyle(
        'SubTitle',
        parent=styles['Heading2'],
        fontSize=18,       
        leading=20,
        spaceBefore=15,
        spaceAfter=10,
        textColor=HexColor('#2C3E50'),
        bold=True
    )


    body_style = ParagraphStyle(
        'BodyStyle',
        parent=styles['Normal'],
        fontSize=11,
        leading=16,
        spaceAfter=10,
        alignment=0
    )

    elements = []
    

    elements.append(Paragraph("Analysis Summary", main_title_style))
    for p in summary.split('\n'):
        p = p.strip()
        if not p:
            elements.append(Spacer(1, 0.1 * inch))
            continue
        if "Title" in p or p.startswith("#"):
            clean_text = p.replace("#", "").strip()
            elements.append(Paragraph(clean_text, sub_title_style))
        elif "Main Sections" in p or p.startswith("#"):
            clean_text = p.replace("#", "").strip()
            elements.append(Paragraph(clean_text, sub_title_style))
        elif "Key Takeaways" in p or p.startswith("#"):
            clean_text = p.replace("#", "").strip()
            elements.append(Paragraph(clean_text, sub_title_style))
        elif "Overview" in p or p.startswith("#"):
            clean_text = p.replace("#", "").strip()
            elements.append(Paragraph(clean_text, sub_title_style))
        elif "Conclusion" in p or p.startswith("#"):
            clean_text = p.replace("#", "").strip()
            elements.append(Paragraph(clean_text, sub_title_style))

        elif p.startswith("*") or p.startswith("-"):
            clean_text = "• " + p[1:].strip()
            elements.append(Paragraph(clean_text, body_style))
        else:
            elements.append(Paragraph(p, body_style))


    # Adding full script if available
    if script:
        elements.append(PageBreak())
        elements.append(Paragraph("Full Video Script", sub_title_style))
        elements.append(Spacer(1, 0.1 * inch))
        formatted_script = script.replace(". ", ".\n\n")
        elements.extend(md_to_pdf_paragraphs(formatted_script, body_style))
        
    doc.build(elements, onFirstPage=header_footer, onLaterPages=header_footer)
    return path
