from reportlab.lib.colors import HexColor, white
from reportlab.lib.units import mm
from reportlab.platypus import Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from config import NAVY, RED, INK, LINE, REPORT_SCALE

u = mm * REPORT_SCALE

styles=getSampleStyleSheet(); title=ParagraphStyle('rtitle', parent=styles['Heading1'], fontName='Helvetica-Bold', fontSize=18*REPORT_SCALE, textColor=white, leading=22*REPORT_SCALE); section=ParagraphStyle('section',parent=styles['Heading2'],fontName='Helvetica-Bold',fontSize=12*REPORT_SCALE,textColor=white,leading=15*REPORT_SCALE); normal=ParagraphStyle('normal',parent=styles['BodyText'],fontName='Helvetica',fontSize=8.5*REPORT_SCALE,textColor=HexColor(INK),leading=11*REPORT_SCALE); footer_text=ParagraphStyle('footer',parent=normal,fontName='Helvetica-Bold',fontSize=7.5*REPORT_SCALE,textColor=white,leading=9*REPORT_SCALE)

def header(team, page, section_name):
    return Table([[Paragraph((team.get('name') or 'MR HUDDLE').upper(), title), Paragraph(section_name, section)]], colWidths=[112*u,68*u], rowHeights=[21*u], style=[('BACKGROUND',(0,0),(-1,-1),HexColor(NAVY)),('VALIGN',(0,0),(-1,-1),'MIDDLE'),('LEFTPADDING',(0,0),(-1,-1),7*u),('RIGHTPADDING',(0,0),(-1,-1),7*u),('LINEBELOW',(0,0),(-1,-1),2,HexColor(RED))])
def band(text): return Table([[Paragraph(text,section)]],colWidths=[180*u],rowHeights=[9*u],style=[('BACKGROUND',(0,0),(-1,-1),HexColor(NAVY)),('LINEBEFORE',(0,0),(0,-1),3,HexColor(RED)),('LEFTPADDING',(0,0),(-1,-1),6*u),('VALIGN',(0,0),(-1,-1),'MIDDLE')])
def grid(rows, widths):
    return Table(rows,colWidths=widths,repeatRows=1,style=[('BACKGROUND',(0,0),(-1,0),HexColor(NAVY)),('TEXTCOLOR',(0,0),(-1,0),white),('FONTNAME',(0,0),(-1,0),'Helvetica-Bold'),('FONTSIZE',(0,0),(-1,-1),7.5*REPORT_SCALE),('GRID',(0,0),(-1,-1),.3*REPORT_SCALE,HexColor(LINE)),('BACKGROUND',(0,1),(-1,-1),HexColor('#f5f8fc')),('VALIGN',(0,0),(-1,-1),'MIDDLE'),('TOPPADDING',(0,0),(-1,-1),3*u),('BOTTOMPADDING',(0,0),(-1,-1),3*u)])
def chart(image): return Image(image,width=88*u,height=51*u)
def footer(team, page): return Table([[Paragraph('PLAY SMART | PLAY STRONG',section),Paragraph(f"{team.get('name','Mr Huddle')} | FLAG FOOTBALL PERFORMANCE REPORT",footer_text),Paragraph(f'Page {page} / 7',section)]],colWidths=[60*u,76*u,44*u],rowHeights=[11*u],style=[('BACKGROUND',(0,0),(-1,-1),HexColor(NAVY)),('TEXTCOLOR',(0,0),(-1,-1),white),('VALIGN',(0,0),(-1,-1),'MIDDLE'),('ALIGN',(2,0),(2,0),'CENTER'),('LEFTPADDING',(0,0),(-1,-1),4*u)])
