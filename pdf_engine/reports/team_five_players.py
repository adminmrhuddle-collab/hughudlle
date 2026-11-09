from reportlab.platypus import SimpleDocTemplate, PageBreak, Table, Paragraph, Spacer, Image
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor, white
from components.layout import header, band, grid, chart, footer, normal, section
from charts.charts import bars, radar
from calculations.team_statistics import stat, total, average, pct, overall
from utils.images import player_photo
from config import PAGE_WIDTH, PAGE_HEIGHT, REPORT_SCALE

u = mm * REPORT_SCALE

def _name(p): return p.get('name') or p.get('displayName') or 'Player'
def _row(p, fields): return [_name(p)] + [str(f(p)) for f in fields]
def _page(story, team, number, name): story.append(Spacer(1,1*u))
def _end(story, team, number): story.extend([Spacer(1,5*u),footer(team,number),PageBreak()])

def build(payload, output):
    team,players=payload['team'],payload['players']; story=[]
    # 1 - Physical profile
    _page(story,team,1,'PHYSICAL PROFILE'); story += [band('SELECTED PLAYERS'),Spacer(1,3*u)]
    cards=[]
    for p in players:
        photo = player_photo(p.get('photoUrl'))
        image = Image(photo, width=25*u, height=38*u, kind='proportional') if photo else Paragraph('<b>NO PHOTO</b>', normal)
        details = Paragraph(f"<b>{_name(p)}</b><br/>#{p.get('number','-')} | {p.get('position','Player')}<br/>Experience: {p.get('experience','n/a')} yrs<br/>Height: {p.get('height','n/a')} cm<br/>Weight: {p.get('weight','n/a')} kg",normal)
        cards.append(Table([[image],[details]], colWidths=[36*u], style=[('ALIGN',(0,0),(-1,0),'CENTER'),('VALIGN',(0,0),(-1,-1),'MIDDLE'),('TOPPADDING',(0,0),(-1,-1),2*u),('BOTTOMPADDING',(0,0),(-1,-1),2*u)]))
    story += [Table([cards],colWidths=[36*u]*5,style=[('BACKGROUND',(0,0),(-1,-1),HexColor('#edf2fa')),('GRID',(0,0),(-1,-1),.4,HexColor('#cdd7e7')),('VALIGN',(0,0),(-1,-1),'TOP'),('TOPPADDING',(0,0),(-1,-1),5*u),('BOTTOMPADDING',(0,0),(-1,-1),5*u)]),Spacer(1,5*u)]
    profile=[['Player','Experience','Height','Weight','40 Yard','Vertical']]+[[_name(p),p.get('experience','n/a'),p.get('height','n/a'),p.get('weight','n/a'),p.get('dash40','n/a'),p.get('verticalJump','n/a')] for p in players]
    story += [grid(profile,[34*u,27*u,27*u,27*u,31*u,34*u]),Spacer(1,5*u)]
    story += [Table([[chart(bars([_name(p) for p in players],[float(p.get('dash40') or 0) for p in players],'40-YARD DASH - RACE VIEW',' s')),chart(radar(['Speed','Jump','Size','Height','Experience'],[(_name(p),[float(p.get('speed') or 0),float(p.get('verticalJump') or 0),float(p.get('weight') or 0)/1.2,float(p.get('height') or 0)/2,float(p.get('experience') or 0)*10]) for p in players],'ATHLETIC PROFILE'))]],colWidths=[90*u,90*u])]
    _end(story,team,1)
    pages=[('PASSING STATISTICS',['passingAttempts','completions','passingYards','passingTDs','interceptionsThrown']),('DEFENSIVE STATISTICS',['flagsPulled','defensiveInterceptions','sacks','sacksAllowed','passBreakups']),('RECEIVING STATISTICS',['receptions','receivingYards','receivingTDs']),('RUSHING STATISTICS',['carries','rushingYards','rushingTDs']),('ALL-PURPOSE PRODUCTION',['passingYards','receivingYards','rushingYards','flagsPulled']),('PLAYER COMPARISON - SCOUTING OVERVIEW',['passingYards','receivingYards','rushingYards','sacks','flagsPulled'])]
    labels={'passingAttempts':'Pass Att','completions':'Completions','passingYards':'Passing Yds','passingTDs':'Passing TDs','interceptionsThrown':'INT Thrown','flagsPulled':'Flags Pulled','defensiveInterceptions':'Def INT','sacks':'Sacks','sacksAllowed':'Sacks Allowed','passBreakups':'Pass Breakups','receptions':'Receptions','receivingYards':'Receiving Yds','receivingTDs':'Receiving TDs','carries':'Carries','rushingYards':'Rushing Yds','rushingTDs':'Rushing TDs'}
    for index,(page_name,keys) in enumerate(pages,start=2):
        _page(story,team,index,page_name); story += [band(page_name),Spacer(1,3*u)]
        rows=[['Player']+[labels.get(k,k) for k in keys]]+[_row(p,[lambda p,k=k:int(stat(p,k)) for k in keys]) for p in players]
        rows.append(['TEAM']+[str(int(total(players,k))) for k in keys]); story += [grid(rows,[36*u]+[(144/len(keys))*u]*len(keys)),Spacer(1,5*u)]
        vals=[stat(p,keys[0]) for p in players]; values2=[stat(p,keys[min(1,len(keys)-1)]) for p in players]
        story += [Table([[chart(bars([_name(p) for p in players],vals,keys[0].replace('Yards',' Yards').title(),'')),chart(bars([_name(p) for p in players],values2,keys[min(1,len(keys)-1)].replace('Yards',' Yards').title(),''))]],colWidths=[90*u,90*u]),Spacer(1,5*u),band('KEY INSIGHTS'),Spacer(1,2*u),Paragraph(f"<b>Team total:</b> {int(sum(vals))}. <b>Leader:</b> {_name(max(players,key=lambda p: stat(p,keys[0])))}. Figures are calculated from the five selected players only.",normal)]
        _end(story,team,index)
    labels = ['PHYSICAL PROFILE','PASSING STATISTICS','DEFENSIVE STATISTICS','RECEIVING STATISTICS','RUSHING STATISTICS','ALL-PURPOSE PRODUCTION','PLAYER COMPARISON']
    def page_header(canvas, doc):
        canvas.saveState(); width, height = PAGE_WIDTH, PAGE_HEIGHT
        canvas.setFillColor(HexColor('#14264f')); canvas.rect(15*u, height-33*u, 180*u, 21*u, fill=1, stroke=0)
        canvas.setFillColor(HexColor('#d0021b')); canvas.rect(15*u, height-33*u, 180*u, 1*u, fill=1, stroke=0)
        canvas.setFillColor(white); canvas.setFont('Helvetica-Bold', 17*REPORT_SCALE); canvas.drawString(22*u, height-23*u, str(team.get('name') or 'MR HUDDLE').upper())
        canvas.setFont('Helvetica-Bold', 10*REPORT_SCALE); canvas.drawRightString(188*u, height-23*u, labels[min(doc.page,7)-1])
        canvas.restoreState()
    doc=SimpleDocTemplate(str(output),pagesize=(PAGE_WIDTH,PAGE_HEIGHT),rightMargin=15*u,leftMargin=15*u,topMargin=39*u,bottomMargin=12*u); doc.build(story, onFirstPage=page_header, onLaterPages=page_header)
