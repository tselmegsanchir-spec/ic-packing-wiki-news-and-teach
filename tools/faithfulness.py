import json,re,sys
items={i['id']:i for i in json.load(open('tools/items.json'))}
notes=json.load(open('tools/notes.json'))
slides=json.load(open('tools/slides.json'))
def card(i): return (notes[i][1]+' '+items[i]['title']+' '+items[i]['outlet']).lower().replace('ʼ',"'")
STOP={'the','a','an','and','or','of','to','in','for','with','by','as','is','are','its','it','at','on','from','also','under','than','that','this','new'}
bad=0
for s in slides:
    for b in s['bullets']:
        if b['k']!='fact': continue
        cc=' '.join(card(i) for i in b['c'])
        toks=re.findall(r"[A-Za-z0-9][A-Za-z0-9.,$µ'-]*[A-Za-z0-9µ]|\d",b['t'])
        missing=[]
        for t in toks:
            tl=re.sub(r"'s$",'',t.lower().strip('.,'))
            if tl in STOP: continue
            if tl.isdigit() or re.search(r'\d',tl) or t[0].isupper():
                if tl not in cc: missing.append(t)
        # numbers must match
        if missing:
            bad+=1; print(f"slide {s['n']}: NOT IN CARD {b['c']}: {missing} | {b['t'][:60]}")
print('faithfulness failures:',bad); sys.exit(1 if bad else 0)
