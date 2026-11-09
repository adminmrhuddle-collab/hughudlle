import argparse,json,os,sys
from pathlib import Path
from utils.validation import require_report
from reports.team_five_players import build

def main():
    parser=argparse.ArgumentParser(); parser.add_argument('--input',required=True); parser.add_argument('--output',required=True); args=parser.parse_args()
    payload=json.loads(Path(args.input).read_text(encoding='utf-8')); team,players=require_report(payload); payload['team']=team; payload['players']=players
    output=Path(args.output).resolve(); output.parent.mkdir(parents=True,exist_ok=True); build(payload,output)
    if not output.is_file() or output.stat().st_size < 1024: raise RuntimeError('PDF generation failed.')
    print(json.dumps({'status':'ok','output':str(output),'size':output.stat().st_size}))
if __name__=='__main__': main()
