import json,re,sys
items={i['id']:i for i in json.load(open('tools/items.json'))}
n=json.load(open('tools/notes.json')); b=json.load(open('tools/briefing.json'))
STOP={'the','a','an','and','or','of','to','in','for','with','by','as','is','are','its','it','at','on','from','also','under','than','that','this','new','another','later'}
bad=0
for c in b['cards']:
    for h in c['happened']:
        cc=' '.join((n[i][1]+' '+items[i]['title']+' '+items[i]['outlet']) for i in h['c']).lower().replace('ʼ',"'")
        for t in re.findall(r"[A-Za-z0-9][A-Za-z0-9.,$µ'-]*[A-Za-z0-9µ]|\d",h['t']):
            tl=re.sub(r"'s$",'',t.lower().strip('.,'))
            if tl in STOP: continue
            if (re.search(r'\d',tl) or t[0].isupper()) and tl not in cc: bad+=1;print('MISSING',h['c'],t)
print('briefing faithfulness failures:',bad);sys.exit(1 if bad else 0)
