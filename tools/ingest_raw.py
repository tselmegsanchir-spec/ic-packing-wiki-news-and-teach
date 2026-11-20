import glob,json,re,sys,os
src=sys.argv[1]; out=sys.argv[2]
for f in sorted(glob.glob(src+'/*.txt')):
    d=json.load(open(f))
    b=d['plaintextBody']
    # cut footer (personal tokens / unsubscribe)
    m=re.search(r'(?i)(unsubscribe|you are receiving|manage (your )?subscription|view in browser)',b)
    # remove sponsor blocks: "Sponsor\n<url>\n\n<title> (url)\n<blurb>\n<name>\n"
    blocks=re.split(r'\n(?=Sponsor\n)',b)
    kept=[blocks[0]]
    for blk in blocks[1:]:
        lines=blk.split('\n')
        # sponsor block = first 6 lines approx; keep rest after the sponsor's company-name line
        # find end: after line index of company name (4th non-empty after 'Sponsor')
        ne=[i for i,l in enumerate(lines) if l.strip()]
        cut=ne[3]+1 if len(ne)>3 else len(lines)
        kept.append('\n'.join(lines[cut:]))
    t='\n'.join(kept)
    t=re.sub(r'https?://\S*(MEDIA-CLICK|unsub|token|click\.|track)\S*','',t)
    date=d['date'][:10]
    hdr=f"ISSUE: {d['subject']}\nDATE: {date}\nMSGID: {d['id']}\n\n"
    open(f"{out}/{date}_{d['id']}.txt",'w').write(hdr+t)
    print(date,d['subject'],len(t))
