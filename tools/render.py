import json,html,collections
items={i['id']:i for i in json.load(open('tools/items.json'))}
notes=json.load(open('tools/notes.json'))
slides=json.load(open('tools/slides.json'))
uniq=[i for i in items.values() if 'repeat' not in i]
tc=collections.Counter(str(notes[i["id"]][0]) for i in uniq)
def date(i): return f"2026-{i[4:6]}-{i[6:8]}"
e=html.escape
def diagram():
    nodes=["Read email","Extract items","Tier by relevance","Evidence card","OUTLINE (human)","Draft per card","Faithfulness check","Render HTML","Render check","Deliver"]
    x=20;y=40;w=112;h=52;g=16;out=[]
    pos=[]
    for i,n in enumerate(nodes):
        row=i//5; col=i%5
        px=20+col*(w+g+60); py=30+row*150
        pos.append((px,py))
        cls="human" if "human" in n else ("gate" if "check" in n else "node")
        out.append(f'<g class="{cls}"><rect x="{px}" y="{py}" width="{w+40}" height="{h}" rx="8"/><text x="{px+(w+40)/2}" y="{py+31}" text-anchor="middle">{e(n)}</text></g>')
    for i in range(len(nodes)-1):
        (ax,ay),(bx,by)=pos[i],pos[i+1]
        if i==4: # wrap to row 2
            out.append(f'<path d="M{ax+76} {ay+52} V{ay+95} H{bx+76} V{by}" class="edge"/>')
        else: out.append(f'<line x1="{ax+152}" y1="{ay+26}" x2="{bx}" y2="{by+26}" class="edge"/>')
    # loops
    gx,gy=pos[6]; out.append(f'<path d="M{gx+30} {gy+52} q-40 40 0 40 h-60" class="loop" fill="none"/><text x="{gx-20}" y="{gy+110}" class="small">fail: back to draft (max 3)</text>')
    rx,ry=pos[8]; out.append(f'<path d="M{rx+30} {ry+52} q-40 40 0 40 h-60" class="loop" fill="none"/><text x="{rx-20}" y="{ry+110}" class="small">fail: back to render (max 3)</text>')
    return '<svg viewBox="0 0 960 290" class="dia">'+''.join(out)+'</svg>'
parts=[]
for s in slides:
    b=[]
    for x in s['bullets']:
        k=x['k']
        if k=='fact': b.append(f'<li class="fact">{e(x["t"])}</li>')
        elif k=='basics': b.append(f'<li class="basics"><span class="tag">Explainer</span>{e(x["t"])}</li>')
        elif k=='hyp': b.append(f'<li class="hyp"><span class="tag">AI hypothesis, not a fact</span>{e(x["t"])}</li>')
        else: b.append(f'<li class="meta">{e(x["t"])}</li>')
    extra=''
    if s.get('diagram'): extra=diagram()
    if s.get('stats'):
        extra=('<div class="stats">'
         f'<div><b>7</b><span>newsletter issues<br>Nov 12-20</span></div><div><b>{len(uniq)}</b><span>unique items<br>(repeats removed)</span></div>'
         f'<div><b>{tc["1"]}</b><span>Tier 1<br>IC design</span></div><div><b>{tc["2"]}</b><span>Tier 2<br>process, packaging</span></div><div><b>{tc["3"]}</b><span>Tier 3<br>market, policy</span></div></div>')
    cites=[]
    for x in s['bullets']:
        for c in x.get('c',[]):
            if c not in cites: cites.append(c)
    foot=''
    if cites:
        foot='Sources (wiki IDs): '+' · '.join(f'<a href="{e(items[c]["url"])}" target="_blank" rel="noopener">[{c}, {date(c)}] {e(items[c]["outlet"])}</a>' for c in cites)
    elif s['tier']=='meta': foot='Source: project wiki (AGENTS.md rules) · no external claims on this slide'
    tier=f'<span class="tier t{s["tier"]}">{"Tier "+s["tier"] if s["tier"]!="meta" else "Method"}</span>'
    parts.append(f'<section class="slide" id="s{s["n"]}"><header>{tier}<span class="num">{s["n"]} / {len(slides)}</span></header><h1>{e(s["title"])}</h1><p class="sub">{e(s["sub"])}</p>{extra}<ul>{"".join(b)}</ul><footer>{foot}</footer></section>')
css='''
:root{--bg:#0f1720;--card:#16222f;--ink:#e8eef5;--mute:#9fb0c3;--acc:#5cc8ff;--warn:#ffc857;--ok:#7be0a4}
*{box-sizing:border-box}html,body{margin:0;background:#070b10;color:var(--ink);font-family:system-ui,-apple-system,"Segoe UI",Roboto,sans-serif}
#stage{width:1280px;height:720px;position:relative;transform-origin:0 0}
.slide{width:1280px;height:720px;background:var(--bg);padding:36px 56px;position:absolute;top:0;left:0;display:none;overflow:hidden}
.slide.on{display:block}
body.all #stage{height:auto;transform:none!important}body.all .slide{position:relative;display:block;margin:0 0 24px}
header{display:flex;justify-content:space-between;align-items:center;height:28px}
.tier{font-size:14px;padding:3px 12px;border-radius:99px;background:#223244;color:var(--acc)}.t1{background:#12384d}.t3{color:var(--mute)}.num{color:var(--mute);font-size:14px}
h1{font-size:38px;line-height:1.15;margin:14px 0 4px;max-height:90px;overflow:hidden}
.sub{color:var(--mute);margin:0 0 14px;font-size:18px}
ul{list-style:none;padding:0;margin:0;display:flex;flex-direction:column;gap:10px}
li{background:var(--card);border-radius:10px;padding:11px 16px;font-size:21px;line-height:1.3}
li.basics{border-left:5px solid var(--ok)}li.hyp{border-left:5px solid var(--warn);background:#2a2415}li.meta{color:#c9d6e3}
.tag{display:inline-block;font-size:12px;font-weight:700;text-transform:uppercase;letter-spacing:.04em;margin-right:10px;padding:2px 8px;border-radius:5px;background:#0f1720;color:var(--ok)}
li.hyp .tag{color:var(--warn)}
footer{position:absolute;left:56px;right:56px;bottom:18px;font-size:13px;color:var(--mute);line-height:1.35;max-height:52px;overflow:hidden}
footer a{color:var(--acc);text-decoration:none;margin-right:6px}
.stats{display:flex;gap:14px;margin:6px 0 14px}.stats div{flex:1;background:var(--card);border-radius:10px;padding:12px;text-align:center}
.stats b{display:block;font-size:44px;color:var(--acc)}.stats span{font-size:15px;color:var(--mute)}
.dia{width:100%;height:270px;margin:2px 0 10px}.dia rect{fill:#16222f;stroke:#35506b}.dia .human rect{fill:#2a2415;stroke:var(--warn)}.dia .gate rect{stroke:var(--ok)}
.dia text{fill:#e8eef5;font-size:15px}.dia .small{font-size:13px;fill:var(--ok)}.dia .edge{stroke:#6b8aa8;fill:none;stroke-width:2}.dia .loop{stroke:var(--ok);stroke-width:2;stroke-dasharray:5 4}
#hint{position:fixed;right:12px;bottom:8px;font-size:12px;color:#6b8aa8}
'''
js='''
const S=[...document.querySelectorAll('.slide')];let i=0;
const st=document.getElementById('stage');
function fit(){if(document.body.classList.contains('all'))return;const k=Math.min(innerWidth/1280,innerHeight/720);st.style.transform='scale('+k+')';}
function show(n){i=Math.max(0,Math.min(S.length-1,n));S.forEach((s,j)=>s.classList.toggle('on',j==i));location.hash='s'+(i+1)}
addEventListener('keydown',e=>{if(['ArrowRight','PageDown',' '].includes(e.key))show(i+1);if(['ArrowLeft','PageUp'].includes(e.key))show(i-1)});
addEventListener('click',e=>{if(e.target.closest('a'))return;show(e.clientX>innerWidth/2?i+1:i-1)});
addEventListener('resize',fit);
if(location.search.includes('all'))document.body.classList.add('all');
fit();show(parseInt((location.hash||'#s1').slice(2))-1||0);
'''
page=f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Packaging-Aware IC Designer Briefing</title><style>{css}</style></head><body><div id="stage">{"".join(parts)}</div><div id="hint">← → or click to navigate</div><script>{js}</script></body></html>'
open('outputs/briefing-en.html','w').write(page)
print('ok',len(page))
