import json,html,sys
LANG=sys.argv[1] if len(sys.argv)>1 else 'en'
e=html.escape
items={i['id']:i for i in json.load(open('tools/items.json'))}
b=json.load(open('tools/briefing.json' if LANG=='en' else 'tools/briefing_mn.json'))
LS=json.load(open('tools/lesson.json' if LANG=='en' else 'tools/lesson_mn.json'))
L={'en':dict(what='What happened',new='New to this?',ai='AI take · hypothesis, not a fact.',flag='Heads up.',t20='In 20 seconds',sub='Lesson first, then the news · from {r} · semiconductors for a future IC designer',take='This week\'s AI take <small>(hypothesis, not fact)</small>',tiers={'1':'IC design','2':'Process & packaging','3':'Market & policy'},foot='Facts come only from the Semiconductor Packaging News wiki; each fact carries a source tag. Ads and paid press releases are excluded. Explanations and "AI take" boxes are my own labeled background and opinion. Sources link to the original outlets.',deck='Graph and loop design',other='Монгол хувилбар',otherf='index-mn.html',read='Read full',paper='SPN paper page',lang='en',out='index.html'),
'mn':dict(what='Юу болсон',new='Шинээр сурч байна уу?',ai='AI-ийн дүгнэлт · таамаглал, баримт биш.',flag='Анхаар.',t20='20 секундэд',sub='Эхлээд хичээл, дараа нь мэдээ · {r}-ний мэдээ · ирээдүйн IC designer-т зориулсан хагас дамжуулагч',take='Энэ долоо хоногийн AI-ийн дүгнэлт <small>(таамаглал, баримт биш)</small>',tiers={'1':'IC design','2':'Процесс ба packaging','3':'Зах зээл ба бодлого'},foot='Баримт зөвхөн Semiconductor Packaging News wiki-ээс гарсан; баримт бүр эх сурвалжийн tag-тай. Сурталчилгаа болон төлбөртэй press release-ийг оруулаагүй. Тайлбар болон "AI-ийн дүгнэлт" хэсэг нь миний тусгайлан тэмдэглэсэн суурь мэдлэг, санал. Эх сурвалжууд эх хэвлэлүүд рүү холбогдоно.',deck='Граф ба loop-ийн дизайн (англи)',other='English version',otherf='index.html',read='Бүтнийг унших',paper='SPN өгүүллийн хуудас',lang='mn',out='index-mn.html')}[LANG]
def d(i): return f"2026-{i[4:6]}-{i[6:8]}"
T={k:(L['tiers'][k],'t'+k) for k in '123'}
ICON=['chip','gate','binary','robot','wafer','pcb','cpu','litho']
cards=[]
for k,c in enumerate(b['cards'],1):
    lab,cls=T[c['tier']]
    def cite(x):
        o=items[x]['outlet']; name=L['paper'] if o=='Technical Paper' else o
        return f'<span class="tag">[{x}, {d(x)}]</span> <a class="read" href="{e(items[x]["url"])}" target="_blank" rel="noopener">{e(L["read"])}: {e(name)} ↗</a>'
    li=''.join(f'<li>{e(h["t"])} <span class="cite">{" ".join(cite(x) for x in h["c"])}</span></li>' for h in c['happened'])
    basics=f'<div class="box basics"><b>{L["new"]}</b> {e(c["basics"])}</div>' if c.get('basics') else ''
    flag=f'<div class="box flag"><b>{L["flag"]}</b> {e(c["flag"])}</div>' if c.get('flag') else ''
    ct=LS['card_terms'][k-1]
    tn={t['id']:t['term'] for t in LS['terms']}
    chips=''.join(f'<a class="chip" href="#t-{x}">{e(tn[x])}</a>' for x in ct)
    chips=f'<div class="terms"><span>{e(LS["labels"]["wiki"] if False else LS["nav1"])}:</span> {chips}</div>' if chips else ''
    cards.append(f'<article class="card {cls}" id="card-{k}"><img class="ic" src="assets/icon-{ICON[k-1]}.png" alt="" width="64" height="64"><div class="meta"><span class="pill {cls}">{lab}</span><span class="topic">{e(c["topic"])}</span></div><h2>{e(c["head"])}</h2><div class="lbl">{L["what"]}</div><ul>{li}</ul>{basics}{flag}{chips}<div class="box ai"><b>{L["ai"]}</b> {e(c["ai"])}</div></article>')
tl=''.join(f'<li>{e(x)}</li>' for x in b['tldr']); tk=''.join(f'<li>{e(x)}</li>' for x in b['take'])

lab=LS['labels']
seen={}
for k,ct in enumerate(LS['card_terms'],1):
    for x in ct: seen.setdefault(x,[]).append(k)
tcards=[]
for n,t in enumerate(LS['terms'],1):
    links=' '.join(f'<a class="chip" href="#card-{k}">{e(b["cards"][k-1]["head"])}</a>' for k in seen.get(t['id'],[]))
    tcards.append(f'<article class="term" id="t-{t["id"]}"><h3><span class="n">{n}</span>{e(t["term"])}</h3><dl><dt>{e(lab["one"])}</dt><dd>{e(t["one"])}</dd><dt>{e(lab["pic"])}</dt><dd>{e(t["pic"])}</dd><dt>{e(lab["why"])}</dt><dd>{e(t["why"])}</dd></dl><div class="src">{e(lab["seen"])}: {links}</div><div class="src">{e(lab["wiki"])}: <code>wiki/{e(t["wiki"])}.md</code></div></article>')
quiz=[]
for n,q in enumerate(LS['quiz'],1):
    opts=''.join(f'<li>{"ABC"[i]}) {e(o)}</li>' for i,o in enumerate(q['o']))
    quiz.append(f'<div class="q"><p><b>{n}. {e(q["q"])}</b></p><ul class="opts">{opts}</ul><details><summary>{e(LS["show"])}</summary><p>{"ABC"[q["a"]]}) {e(q["o"][q["a"]])}. {e(q["why"])}</p></details></div>')
lesson_html=f'<nav class="nav"><a href="#lesson">{e(LS["nav1"])}</a><a href="#quiz">{e(LS["navq"])}</a><a href="#news">{e(LS["nav2"])}</a></nav><section id="lesson"><h2 class="part">{e(LS["part1"])}</h2><div class="goal"><b>{e(LS["goal_h"])}.</b> {e(LS["goal"])}</div>{"".join(tcards)}</section><section id="quiz" class="quiz"><h3>{e(LS["quiz_h"])}</h3>{"".join(quiz)}</section><h2 class="part" id="news">{e(LS["part2"])}</h2>'
CSS='''
:root{--ink:#e8eef8;--mute:#a9b8cf;--card:rgba(10,16,30,.86);--line:rgba(77,208,255,.22);--cy:#4dd0ff;--gold:#f5b942;--teal:#4dd6c0;--red:#ff7b7b}
*{box-sizing:border-box}html{background:#050912}
body{margin:0;color:var(--ink);font:17px/1.58 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;position:relative;min-height:100vh}
body::before{content:"";position:fixed;inset:0;z-index:-1;background:#050912 url(assets/bg-desktop.jpg) center/cover no-repeat}
body::after{content:"";position:fixed;inset:0;z-index:-1;background:linear-gradient(180deg,rgba(5,9,18,.15),rgba(5,9,18,.45))}
@media(max-width:700px){body::before{background-image:url(assets/bg-mobile.jpg)}}
.wrap{max-width:760px;margin:0 auto;padding:22px 16px 70px}
.hero{display:flex;gap:16px;align-items:center;padding:14px 18px;background:var(--card);border:1px solid var(--line);border-radius:18px;backdrop-filter:blur(8px)}.hero img{width:76px;height:76px;flex:none;filter:drop-shadow(0 0 14px rgba(77,208,255,.55))}
.hero h1{font-size:36px;line-height:1.08;margin:0 0 4px;letter-spacing:-.02em;background:linear-gradient(90deg,#fff,var(--cy));-webkit-background-clip:text;background-clip:text;color:transparent}
.hero p{margin:0;color:var(--mute);font-size:14px}
.tldr{background:linear-gradient(135deg,rgba(77,208,255,.16),rgba(245,185,66,.12));border:1px solid var(--line);border-radius:18px;padding:16px 20px;margin:18px 0;backdrop-filter:blur(6px)}
.tldr h3{margin:0 0 6px;font-size:12px;letter-spacing:.12em;text-transform:uppercase;color:var(--gold)}.tldr ul{margin:0;padding-left:20px}.tldr li{margin:5px 0}

.nav{display:flex;gap:10px;margin:14px 0;flex-wrap:wrap}.nav a{background:rgba(77,208,255,.14);border:1px solid var(--line);color:var(--cy);padding:6px 14px;border-radius:99px;text-decoration:none;font-size:14px;font-weight:600}
.part{font-size:22px;margin:26px 0 8px;color:#fff;border-bottom:2px solid var(--cy);padding-bottom:6px}
.goal{background:rgba(245,185,66,.12);border-left:4px solid var(--gold);border-radius:12px;padding:10px 14px;margin:10px 0;font-size:16px}.goal b{color:var(--gold)}
.term{background:var(--card);border:1px solid var(--line);border-radius:18px;padding:16px 20px;margin:14px 0;backdrop-filter:blur(6px);scroll-margin-top:10px}
.term h3{margin:0 0 6px;font-size:20px}.term .n{display:inline-block;width:28px;height:28px;line-height:28px;text-align:center;border-radius:50%;background:var(--cy);color:#06121f;font-size:15px;font-weight:700;margin-right:10px}
.term dl{margin:0}.term dt{font-size:12px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:var(--cy);margin-top:8px}.term dd{margin:2px 0 0}
.src{font-size:13px;color:var(--mute);margin-top:8px}.src code{color:#8fb4d9}
.chip{display:inline-block;font-size:12.5px;background:rgba(77,208,255,.14);border:1px solid var(--line);color:var(--cy);border-radius:99px;padding:1px 10px;margin:2px 4px 2px 0;text-decoration:none}
.terms{font-size:13px;color:var(--mute);margin:6px 0}
.quiz{background:var(--card);border:1px solid var(--line);border-radius:18px;padding:14px 20px;margin:16px 0}.quiz h3{margin:0 0 6px}
.q{margin:12px 0;padding-top:8px;border-top:1px solid var(--line)}.q:first-of-type{border-top:0}.opts{list-style:none;padding-left:4px;margin:2px 0 6px}
.q details{background:rgba(77,214,192,.1);border-radius:10px;padding:6px 12px}.q summary{cursor:pointer;color:var(--teal);font-weight:600}
html{scroll-behavior:smooth}.card{scroll-margin-top:10px}
.card{position:relative;background:var(--card);border:1px solid var(--line);border-radius:18px;padding:18px 20px 12px;margin:16px 0;backdrop-filter:blur(6px);box-shadow:0 8px 30px rgba(0,0,0,.35)}
.ic{position:absolute;top:14px;right:16px;width:58px;height:58px;object-fit:contain;filter:drop-shadow(0 0 10px rgba(77,208,255,.35))}
.meta{display:flex;gap:10px;align-items:center;flex-wrap:wrap;padding-right:70px}.pill{font-size:12px;font-weight:700;padding:3px 10px;border-radius:99px}
.pill.t1{background:rgba(77,208,255,.18);color:var(--cy)}.pill.t2{background:rgba(167,139,250,.2);color:#c4b5fd}.pill.t3{background:rgba(255,255,255,.1);color:#cbd5e1}
.topic{color:var(--mute);font-size:14px}
h2{font-size:23px;line-height:1.25;margin:8px 70px 10px 0}
.lbl{font-size:12px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:var(--cy);margin-bottom:2px}
ul{margin:4px 0 10px;padding-left:20px}li{margin:6px 0}
.cite{font-size:12.5px;display:block;margin-top:2px}.cite .tag{color:#7f93ad;margin-right:6px}.cite a.read{display:inline-block;color:#06121f;background:var(--cy);font-weight:600;text-decoration:none;padding:1px 9px;border-radius:99px;margin:2px 6px 2px 0}.cite a.read:hover{background:#fff}
.box{border-radius:12px;padding:10px 14px;margin:9px 0;font-size:16px}
.basics{background:rgba(77,214,192,.12);border-left:4px solid var(--teal)}.basics b{color:var(--teal)}
.ai{background:rgba(245,185,66,.13);border-left:4px solid var(--gold)}.ai b{color:var(--gold)}
.flag{background:rgba(255,123,123,.12);border-left:4px solid var(--red)}.flag b{color:var(--red)}
.take{background:rgba(245,185,66,.12);border:1px solid rgba(245,185,66,.4);border-radius:16px;padding:14px 20px;margin:20px 0;backdrop-filter:blur(6px)}.take h3{margin:0 0 6px;color:var(--gold)}.take small{color:var(--mute);font-weight:400}
footer{color:var(--mute);font-size:14px;margin-top:26px;border-top:1px solid var(--line);padding-top:14px}footer a{color:var(--cy)}
@media(max-width:480px){.hero h1{font-size:28px}.hero img{width:60px;height:60px}h2{font-size:20px;margin-right:62px}body{font-size:16px}.ic{width:48px;height:48px}.meta{padding-right:58px}}
'''
import re
frag=f'''<div class="lang" id="lang-{LANG}" lang="{L["lang"]}">
<header class="hero"><img src="assets/icon-atom.png" alt="" width="76" height="76"><div><h1>{e(b["title"])}</h1><p>{e(L["sub"].format(r=b["range"]))}</p></div></header>
{lesson_html}
<section class="tldr"><h3>{L["t20"]}</h3><ul>{tl}</ul></section>
{"".join(cards)}
<section class="take"><h3>{L["take"]}</h3><ul>{tk}</ul></section>
<footer>{L["foot"]}<br><a href="graph.html">{L["deck"]}</a></footer></div>'''
ids=set(re.findall(r'id="([^"]+)"',frag))-{f'lang-{LANG}'}
for x in ids:
    frag=frag.replace(f'id="{x}"',f'id="{LANG}-{x}"').replace(f'href="#{x}"',f'href="#{LANG}-{x}"')
open(f'tools/frag_{LANG}.html','w').write(frag)
open('tools/page.css','w').write(CSS)
