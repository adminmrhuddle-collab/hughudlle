from io import BytesIO
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from config import PLAYER_COLORS, NAVY, RED

def _image(fig):
    out = BytesIO(); fig.savefig(out, format='png', dpi=170, bbox_inches='tight', transparent=False); plt.close(fig); out.seek(0); return out

def bars(labels, values, title, unit=''):
    fig, ax = plt.subplots(figsize=(6,3.1)); ax.bar(range(len(values)), values, color=PLAYER_COLORS[:len(values)])
    ax.set_xticks(range(len(labels)), labels, rotation=18, ha='right', fontsize=8); ax.set_title(title, loc='left', fontweight='bold', color=NAVY); ax.grid(axis='y', alpha=.22)
    for i,v in enumerate(values): ax.text(i, v, f'{v:g}{unit}', ha='center', va='bottom', fontsize=8, fontweight='bold')
    fig.tight_layout(); return _image(fig)

def radar(labels, datasets, title):
    angles=np.linspace(0,2*np.pi,len(labels),endpoint=False).tolist(); angles+=angles[:1]
    fig,ax=plt.subplots(figsize=(5.6,3.4),subplot_kw={'polar':True}); ax.set_title(title, loc='left', fontweight='bold', color=NAVY, pad=18)
    ax.set_xticks(angles[:-1],labels,fontsize=8); ax.set_yticklabels([]); ax.set_ylim(0,100)
    for i,(name,values) in enumerate(datasets):
        data=list(values)+[values[0]]; ax.plot(angles,data,color=PLAYER_COLORS[i],linewidth=2,label=name); ax.fill(angles,data,color=PLAYER_COLORS[i],alpha=.08)
    ax.legend(loc='upper center',bbox_to_anchor=(.5,-.15),ncol=3,fontsize=7,frameon=False); fig.tight_layout(); return _image(fig)
