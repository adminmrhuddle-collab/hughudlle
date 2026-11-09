from reportlab.lib.colors import HexColor, white
from reportlab.lib.units import mm
from reportlab.platypus import Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from config import NAVY, RED, INK, LINE

styles=getSampleStyleSheet(); title=ParagraphStyle('rtitle', parent=styles['Heading1'], fontName='Helvetica-Bold', fontSize=18, textColor=white, leading=22); section=ParagraphStyle('section',parent=styles['Heading2'],fontName='Helvetica-Bold',fontSize=12,textColor=white,leading=15); normal=ParagraphStyle('normal',parent=styles['BodyText'],fontName='Helvetica',fontSize=8.5,textColor=HexColor(INK),leading=11); footer_text=ParagraphStyle('footer',parent=normal,fontName='Helvetica-Bold',fontSize=7.5,textColor=white,leading=9)

def header(team, page, section_name):
    return Table([[Paragraph((team.get('name') or 'MR HUDDLE').upper(), title), Paragraph(section_name, section)]], colWidths=[112*mm,68*mm], rowHeights=[21*mm], style=[('BACKGROUND',(0,0),(-1,-1),HexColor(NAVY)),('VALIGN',(0,0),(-1,-1),'MIDDLE'),('LEFTPADDING',(0,0),(-1,-1),7*mm),('RIGHTPADDING',(0,0),(-1,-1),7*mm),('LINEBELOW',(0,0),(-1,-1),2,HexColor(RED))])
def band(text): return Table([[Paragraph(text,section)]],colWidths=[180*mm],rowHeights=[9*mm],style=[('BACKGROUND',(0,0),(-1,-1),HexColor(NAVY)),('LINEBEFORE',(0,0),(0,-1),3,HexColor(RED)),('LEFTPADDING',(0,0),(-1,-1),6*mm),('VALIGN',(0,0),(-1,-1),'MIDDLE')])
def grid(rows, widths):
    return Table(rows,colWidths=widths,repeatRows=1,style=[('BACKGROUND',(0,0),(-1,0),HexColor(NAVY)),('TEXTCOLOR',(0,0),(-1,0),white),('FONTNAME',(0,0),(-1,0),'Helvetica-Bold'),('FONTSIZE',(0,0),(-1,-1),7.5),('GRID',(0,0),(-1,-1),.3,HexColor(LINE)),('BACKGROUND',(0,1),(-1,-1),HexColor('#f5f8fc')),('VALIGN',(0,0),(-1,-1),'MIDDLE'),('TOPPADDING',(0,0),(-1,-1),3*mm),('BOTTOMPADDING',(0,0),(-1,-1),3*mm)])
def chart(image): return Image(image,width=88*mm,height=51*mm)
def footer(team, page): return Table([[Paragraph('PLAY SMART | PLAY STRONG',section),Paragraph(f"{team.get('name','Mr Huddle')} | FLAG FOOTBALL PERFORMANCE REPORT",footer_text),Paragraph(f'Page {page} / 7',section)]],colWidths=[60*mm,76*mm,44*mm],rowHeights=[11*mm],style=[('BACKGROUND',(0,0),(-1,-1),HexColor(NAVY)),('TEXTCOLOR',(0,0),(-1,-1),white),('VALIGN',(0,0),(-1,-1),'MIDDLE'),('ALIGN',(2,0),(2,0),'CENTER'),('LEFTPADDING',(0,0),(-1,-1),4*mm)])
