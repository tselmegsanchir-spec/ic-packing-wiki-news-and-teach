import json,re,sys,os,os
from playwright.sync_api import sync_playwright
ids={i['id'] for i in json.load(open('tools/items.json'))}
F=sys.argv[1] if len(sys.argv)>1 else 'index.html'
src=open(F).read(); bad=0
for c in set(re.findall(r'SPN-\d{4}-\d{2}',src)):
    if c not in ids: print('FAIL id',c);bad+=1
import os
anchors=set(re.findall(r'id="([^"]+)"',src))
for h in set(re.findall(r'href="#([^"]+)"',src)):
    if h not in anchors: print('FAIL dead anchor',h); bad+=1
for wp in set(re.findall(r'<code>wiki/([^<]+)</code>',src)):
    if not os.path.exists('wiki/'+wp): print('FAIL wiki page missing',wp); bad+=1
if src.count('class="term"')!=14 or src.count('<details>')!=10: print('FAIL lesson parts',src.count('class="term"'),src.count('<details>')); bad+=1
with sync_playwright() as p:
    b=p.chromium.launch(executable_path=os.environ.get('CHROME_PATH') or None,args=['--no-sandbox'])
    for w,lg in [(390,'en'),(390,'mn'),(1280,'en'),(1280,'mn')]:
        pg=b.new_page(viewport={'width':w,'height':900})
        pg.goto('file://'+os.path.abspath(F)+'?lang='+lg)
        r=pg.evaluate('''()=>{const W=document.documentElement.clientWidth;const o=[];
          document.querySelectorAll('h1,h2,li,.box,.tldr,.cite a').forEach(e=>{const q=e.getBoundingClientRect();if(q.right>W+1||q.left<-1)o.push(e.textContent.slice(0,30))});
          return [document.documentElement.scrollWidth>W,o,[...document.querySelectorAll('article.card')].filter(a=>a.offsetParent).length,
            [...document.querySelectorAll('article.card')].filter(a=>a.offsetParent).filter(a=>!a.querySelector('.cite a')).length]}''')
        imgs=pg.evaluate('''()=>[...document.images].filter(i=>!i.complete||i.naturalWidth==0).map(i=>i.src)''')
        if imgs: print('FAIL broken images',imgs); bad+=1
        print(w,lg,r,pg.evaluate('document.documentElement.lang'));
        if r[2]!=8: print('FAIL visible cards',r[2]); bad+=1
        if pg.evaluate('document.querySelectorAll(".lang").length&&[...document.querySelectorAll(".lang")].filter(x=>x.offsetParent).length')!=1: print('FAIL both langs visible'); bad+=1
        if r[0] or r[1] or r[3]: bad+=1
        pg.screenshot(path=f'/tmp/br{F[:-5]}{lg}{w}.png',full_page=True)
    b.close()
print('briefing render failures:',bad);sys.exit(1 if bad else 0)
