import sys,subprocess
for l in ('en','mn'): subprocess.run([sys.executable,'tools/_build_lang.py',l],check=True)
fe=open('tools/frag_en.html').read(); fm=open('tools/frag_mn.html').read(); css=open('tools/page.css').read()
css+='''
.lang{display:none}html[data-lang=en] #lang-en,html[data-lang=mn] #lang-mn{display:block}
.sw{position:fixed;top:10px;right:10px;z-index:10;display:flex;border:1px solid var(--line);border-radius:99px;overflow:hidden;background:rgba(10,16,30,.92)}
.sw button{font:600 13px system-ui;color:var(--cy);background:none;border:0;padding:7px 14px;cursor:pointer}
html[data-lang=en] .sw [data-l=en],html[data-lang=mn] .sw [data-l=mn]{background:var(--cy);color:#06121f}
.hero{margin-top:34px}
'''
js='''<script>
(function(){var h=document.documentElement,q=(location.search.match(/lang=(en|mn)/)||[])[1],s=null;
try{s=localStorage.getItem('lang')}catch(e){}
function set(l,save){h.setAttribute('data-lang',l);h.lang=l;if(save){try{localStorage.setItem('lang',l)}catch(e){}}}
set(q||(s=='mn'||s=='en'?s:'en'),!!q);
document.querySelectorAll('.sw button').forEach(function(b){b.onclick=function(){set(b.dataset.l,true);window.scrollTo(0,0)}});
})();</script>'''
page=f'''<!doctype html><html lang="en" data-lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Chip Morning Brief · EN / МН</title><style>{css}</style></head><body><div class="sw" role="group" aria-label="Language"><button data-l="en">EN</button><button data-l="mn">МН</button></div><div class="wrap">{fe}{fm}</div>{js}</body></html>'''
open('index.html','w').write(page)
open('index-mn.html','w').write('<!doctype html><meta charset="utf-8"><meta http-equiv="refresh" content="0;url=index.html?lang=mn"><title>Redirect</title><a href="index.html?lang=mn">Монгол хувилбар: index.html?lang=mn</a>')
print('ok',len(page))
