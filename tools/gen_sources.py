import json,collections
items=json.load(open('tools/items.json')); notes=json.load(open('tools/notes.json'))
by=collections.defaultdict(list)
for it in items: by[it['date']].append(it)
for date,its in by.items():
    subj=its[0]['issue']
    ids=[i['id'] for i in its]
    L=["---",f"title: SPN issue {date}",f"type: source","tier: 1",f"updated: 2026-11-20",f"sources: [{', '.join(ids)}]","---",
       f"# Semiconductor Packaging News — {date}",f"Issue headline: {subj}. Sponsor ads, Industry Press releases, quiz and cartoon are excluded (see AGENTS.md section 9).","",
       "| ID | Tier | Item (outlet) | My one-line paraphrase | Link |","|---|---|---|---|---|"]
    for i in its:
        if 'repeat' in i:
            L.append(f"| {i['id']} | - | {i['title'][:80]} ({i['outlet']}) | repeat of {i['repeat']} (not counted again) | [link]({i['url']}) |")
        else:
            t,s=notes[i['id']]
            L.append(f"| {i['id']} | {t} | {i['title'][:80]} ({i['outlet']}) | {s} [{i['id']}, {date}] | [link]({i['url']}) |")
    L+=["","Related: [[index]] · [[glossary]] · [[open-questions]]",""]
    open(f"wiki/sources/spn-{date}.md",'w').write('\n'.join(L).replace('ʼ',"'"))
print(len(by))
