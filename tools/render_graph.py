import html
e=html.escape
nodes=[("Read mail","Gmail read-only","n"),("Clean to raw/","private, clean","n"),("Extract items","IDs, no repeats","n"),("Tier + notes","own-word notes","n"),
("Wiki pages","append only","n"),("Lint gate","4 checks","g"),("Pick stories","last 7 days","n"),("Outline","human approves","h"),
("Write cards","facts cite IDs","n"),("Faithfulness","numbers, names","g"),("Translate MN","same cards","n"),("Consistency","numbers, names","g"),
("Render HTML","EN + MN","n"),("Render gate","phone + desktop","g"),("Deliver","folder, Pages","n")]
COL={'n':('#e8edf3','#6b7a8c'),'g':('#d6f5ee','#1d9e75'),'h':('#fdebc8','#ba7517')}
out=[]
for i,(t,sub,k) in enumerate(nodes):
    r,c=divmod(i,4); x=35+c*160; y=40+r*120
    f,s=COL[k]
    out.append(f'<rect x="{x}" y="{y}" width="130" height="56" rx="8" fill="{f}" stroke="{s}" stroke-width="1"/><text x="{x+65}" y="{y+20}" text-anchor="middle" font-size="14" font-weight="600" fill="#12202f">{e(t)}</text><text x="{x+65}" y="{y+40}" text-anchor="middle" font-size="12" fill="#3b4a5c">{e(sub)}</text>')
def fwd(x1,y,x2): return f'<line x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" stroke="#12202f" stroke-width="1.5" marker-end="url(#a)"/>'
def ret(x1,y,x2,col): return f'<line x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" stroke="{col}" stroke-width="1.4" stroke-dasharray="4 3" marker-end="url(#ar)"/>'
for r in range(4):
    y=40+r*120
    cols=3 if r<3 else 2
    for c in range(cols):
        if r==3 and c>=2: break
        x=35+c*160
        out.append(fwd(x+132,y+20,x+158))
        if (r,c) in [(0,0),(0,1),(0,2),(1,0),(1,2),(2,0),(2,2),(2,1) ] : pass
for r in range(3):
    y=40+r*120
    out.append(f'<path d="M580 {y+58} V{y+88} H100 V{y+118}" fill="none" stroke="#12202f" stroke-width="1.5" marker-end="url(#a)"/>')
rets=[(1,0,'#d85a30'),(1,2,'#ba7517'),(2,0,'#d85a30'),(2,2,'#d85a30'),(3,0,'#d85a30')]
for r,c,col in rets:
    y=40+r*120; x=35+c*160
    out.append(ret(x+158,y+40,x+132,col))
svg=f'<svg viewBox="0 0 680 520" width="100%" role="img" aria-label="Graph with gates and return routes"><defs><marker id="a" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M2 1L8 5L2 9" fill="none" stroke="#12202f" stroke-width="1.5"/></marker><marker id="ar" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M2 1L8 5L2 9" fill="none" stroke="#d85a30" stroke-width="1.5"/></marker></defs>'+''.join(out)+'<rect x="35" y="486" width="14" height="14" rx="3" fill="#e8edf3" stroke="#6b7a8c"/><text x="56" y="498" font-size="12" fill="#12202f">Step</text><rect x="110" y="486" width="14" height="14" rx="3" fill="#d6f5ee" stroke="#1d9e75"/><text x="131" y="498" font-size="12" fill="#12202f">Gate (script)</text><rect x="230" y="486" width="14" height="14" rx="3" fill="#fdebc8" stroke="#ba7517"/><text x="251" y="498" font-size="12" fill="#12202f">Human gate</text><line x1="345" y1="493" x2="375" y2="493" stroke="#d85a30" stroke-width="1.4" stroke-dasharray="4 3" marker-end="url(#ar)"/><text x="384" y="498" font-size="12" fill="#12202f">Return route when a gate fails</text></svg>'
qa=[("Which steps repeat?","The four gates repeat. Lint, Faithfulness, Consistency and Render gate each run again after a fix; Faithfulness and Render are capped at 3 passes. The Outline gate repeats until the owner approves. A failed gate returns to the step just before it, never all the way to the start."),
("Which parts must be checked or regenerated?","Checked by script: wiki citations and links (Lint), numbers and names in each fact against its wiki card (Faithfulness), Mongolian numbers and names against the English cards (Consistency), overflow, broken links, stat values and phone/desktop layout (Render gate). Regenerated: only the cards or the page that failed. Wiki pages are append-only and are not regenerated."),
("Why this design?","Facts must trace to the wiki, so every fact carries an ID and each step sees only its allowed input. Cheap script checks run on every pass; the expensive human check happens once, at the outline, where a wrong direction costs the least. Gates sit right after the step that tends to fail, so an error is found where it was made.")]
css='body{margin:0;background:#070b14;color:#e8eef8;font:17px/1.6 system-ui,sans-serif}.w{max-width:760px;margin:0 auto;padding:22px 16px 60px}h1{font-size:30px;margin:6px 0}h2{font-size:20px;margin:26px 0 6px;color:#4dd0ff}.c{background:#fff;border-radius:14px;padding:10px}p{margin:4px 0}.sub{color:#a9b8cf}a{color:#4dd0ff}'
page=f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Graph and loop design</title><style>{css}</style></head><body><div class="w"><h1>Graph and loop design</h1><p class="sub">How information is acquired, organised, checked and turned into the lesson and briefing.</p><h2>The graph</h2><div class="c">{svg}</div><p class="sub">Course chain: obtain information, consult the wiki, summarise key points, check, generate. Here "obtain" = Read mail to Tier + notes; "consult the wiki" = Wiki pages to Pick stories; "summarise" = Write cards; "check" = the gates; "generate" = Render and Deliver.</p>'+''.join(f'<h2>{e(q)}</h2><p>{e(a)}</p>' for q,a in qa)+'<p class="sub" style="margin-top:24px"><a href="index.html">Back to the briefing</a></p></div></body></html>'
open('graph.html','w').write(page); print('ok')
