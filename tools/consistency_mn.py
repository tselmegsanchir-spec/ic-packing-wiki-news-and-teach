import json,re,sys
en=json.load(open('tools/briefing.json'));mn=json.load(open('tools/briefing_mn.json'))
bad=0
nums=lambda s:sorted(n.strip('.,') for n in re.findall(r'\d[\d,.]*\d|\d',s.replace('%','')))
def lat(s): return set(w.rstrip('-') for w in re.findall(r"[A-Za-z][A-Za-z0-9-]+",s) if w[0].isupper() or w.isupper())
assert len(en['cards'])==len(mn['cards'])
for a,b in zip(en['cards'],mn['cards']):
    assert a['tier']==b['tier'] and len(a['happened'])==len(b['happened'])
    for x,y in zip(a['happened'],b['happened']):
        assert x['c']==y['c']
        if nums(x['t'])!=nums(y['t']): bad+=1;print('NUM',x['c'])
        miss=[w for w in lat(y['t']) if w.lower() not in x['t'].lower()]
        if miss: bad+=1;print('NAME',x['c'],miss)
    if ('basics' in a)!=('basics' in b) or ('flag' in a)!=('flag' in b): bad+=1
print('mn consistency failures:',bad);sys.exit(1 if bad else 0)
