import glob,re,json,collections
items=[]
for f in sorted(glob.glob('raw/*.txt')):
    t=open(f).read()
    date=re.search(r'DATE: (\S+)',t).group(1)
    iss=re.search(r'ISSUE: (.+)',t).group(1)
    body=t.split('Industry Press')[0]
    lines=body.split('\n')
    for i,l in enumerate(lines):
        m=re.match(r'^(.+?) \((https?://[^)\s]+)\s*\)$',l.strip())
        if not m or l.startswith('■'): continue
        title,url=m.groups()
        if 'semiconductorpackagingnews.com' in url and '/papers/' not in url: continue
        blurb=lines[i+1].strip() if i+1<len(lines) else ''
        outlet=lines[i+2].strip() if i+2<len(lines) else ''
        kind='paper' if '/papers/' in url else 'news'
        items.append(dict(date=date,issue=iss,title=title,url=url,blurb=blurb,outlet=outlet,kind=kind))
items=[i for i in items if 'MORE TECH' not in i['title']]
cnt=collections.Counter();first={}
for it in items:
    mmdd=it['date'][5:7]+it['date'][8:10]
    cnt[mmdd]+=1
    it['id']=f"SPN-{mmdd}-{cnt[mmdd]:02d}"
    if it['url'] in first: it['repeat']=first[it['url']]
    else: first[it['url']]=it['id']
json.dump(items,open('tools/items.json','w'),indent=1,ensure_ascii=False)
print(len(items),'items;',sum('repeat' not in i for i in items),'unique')
