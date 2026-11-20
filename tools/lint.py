import glob,re,sys,datetime
today=datetime.date(2026,11,20) if len(sys.argv)<2 else datetime.date.fromisoformat(sys.argv[1])
pages=sorted(glob.glob('wiki/**/*.md',recursive=True))
ids=set()
for p in glob.glob('wiki/sources/*.md'):
    ids|=set(re.findall(r'\|\s*(SPN-\d{4}-\d{2})\s*\|',open(p).read()))
bad=0
def fail(m):
    global bad; bad+=1; print('FAIL',m)
text={p:open(p).read() for p in pages}
idx=open('index.md').read()
for p,t in text.items():
    body=t.split('---',2)[2] if t.startswith('---') else t
    src_page='/sources/' in p
    for n,l in enumerate(body.split('\n'),1):
        s=l.strip()
        # 1 uncited statements
        if not s.startswith(('- ','* ')) or src_page: pass
        else:
            if '[SPN-' not in s and '(Explainer)' not in s and '(AI hypothesis)' not in s and 'Related:' not in s and 'Scope note' not in s and not s.startswith('- Status') and not s.startswith('- (Explainer)') and '[[' not in s:
                fail(f'1-uncited {p}:{n}: {s[:70]}')
        for m in re.finditer(r'\[(SPN-\d{4}-\d{2}), (\d{4}-\d{2}-\d{2})\]',s):
            if m.group(1) not in ids: fail(f'1-unknown-id {p}:{n} {m.group(1)}')
            # 3 outdated
            d=datetime.date.fromisoformat(m.group(2))
            if (today-d).days>30: print('WARN outdated (>30d)',p,m.group(1))
    # 4 orphans
    name=p[5:-3]
    links=sum(1 for q,tt in text.items() if q!=p and f'[[{name}]]' in tt)
    if f'[[{name}]]' not in idx: fail(f'4-orphan (not in index) {p}')
    if links==0 and '/sources/' not in p: fail(f'4-orphan (no inbound link) {p}')
# 2 conflicts logged
oq=text['wiki/open-questions.md']
if oq.count('## Conflict')<1: fail('2-no conflicts logged')
print('lint done, failures:',bad)
sys.exit(1 if bad else 0)
