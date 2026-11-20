import json,re,sys,os
from playwright.sync_api import sync_playwright
items={i['id'] for i in json.load(open('tools/items.json'))}
src=open('outputs/briefing-en.html').read()
bad=0
for c in set(re.findall(r'SPN-\d{4}-\d{2}',src)):
    if c not in items: print('FAIL unknown id',c); bad+=1
with sync_playwright() as p:
    b=p.chromium.launch(executable_path=os.environ.get('CHROME_PATH') or None,args=['--no-sandbox'])
    pg=b.new_page(viewport={'width':1280,'height':800})
    pg.goto('file://'+__import__('os').path.abspath('outputs/briefing-en.html')+'?all')
    res=pg.evaluate('''()=>{const out=[];document.querySelectorAll('.slide').forEach((s,n)=>{
      const r=s.getBoundingClientRect();
      s.querySelectorAll('h1,li,footer,.stats,.dia,.sub').forEach(el=>{
        const q=el.getBoundingClientRect();
        if(el.scrollHeight>el.clientHeight+1||el.scrollWidth>el.clientWidth+1)out.push([n+1,el.tagName,'clipped',el.textContent.slice(0,30)]);
        if(q.bottom>r.bottom-2||q.right>r.right+1)out.push([n+1,el.tagName,'outside',el.textContent.slice(0,30)]);
      });
      const ul=s.querySelector('ul').getBoundingClientRect(),f=s.querySelector('footer').getBoundingClientRect();
      if(ul.bottom>f.top-4)out.push([n+1,'UL','overlaps footer',Math.round(ul.bottom-f.top)]);
      if(!s.querySelector('footer').textContent.trim())out.push([n+1,'footer','no citation line','']);
    });return out}''')
    for r in res: print('FAIL',r); bad+=1
    if len(sys.argv)>1:
        pg.goto('file://'+__import__('os').path.abspath('outputs/briefing-en.html')+'?all')
        for n in range(1,10):
            pg.locator(f'#s{n}').screenshot(path=f'/tmp/s{n}.png')
    b.close()

import collections
its=json.load(open('tools/items.json')); notes=json.load(open('tools/notes.json'))
uniq=[i for i in its if 'repeat' not in i]
nums=[int(x) for x in re.findall(r'<b>(\d+)</b>',src)]
tc=collections.Counter(notes[i['id']][0] for i in uniq)
if nums!=[7,len(uniq),tc[1],tc[2],tc[3]] or 0 in nums: print('FAIL stats',nums); bad+=1
print('stats',nums)
print('render check failures:',bad); sys.exit(1 if bad else 0)
