"""Create reading editions from the user-supplied PDF. Does not claim website identity."""
from pypdf import PdfReader
import re,json,pathlib,argparse
root=pathlib.Path(__file__).parent
parser=argparse.ArgumentParser();parser.add_argument('pdf',help='Path to the user-supplied 2015 handbook');args=parser.parse_args()
r=PdfReader(args.pdf)
def pages(a,b):
    return '\n'.join(re.sub(r'^\s*\d+\s*\n','',r.pages[n-2].extract_text() or '') for n in range(a,b+1))
def clean(t):
    paragraphs=[]
    for part in re.split(r'\n\s*\n',t):
        part=re.sub(r'(?<=[\u4e00-\u9fff])\s+(?=[\u4e00-\u9fff])','',part)
        part=re.sub(r'[ \t]+',' ',part.replace('\n','')).strip()
        if part:paragraphs.append(part)
    return '\n\n'.join(paragraphs)
rows=[]
configs=[('使徒信经','creeds/apostles-creed',5,5,'我信神'),('尼西亚信经','creeds/nicene-creed',6,7,'我们信独一的神'),('亚他那修信经','creeds/athanasian-creed',8,10,'1)'),('比利时信条','confessions/belgic-confession',11,47,None),('海德堡要理问答','confessions/heidelberg-catechism',48,94,None),('多特信经','confessions/canons-of-dort',95,138,None)]
for title,slug,a,b,start in configs:
    t=pages(a,b)
    if start:
        # PDF line spacing may split the incipit; remove formatting whitespace first.
        t=clean(t)
        if start in t:t=t[t.index(start):]
    else:t=clean(t)
    if slug.endswith('belgic-confession'):slug='confessions/the-belgic-confession'
    rows.append(dict(title=title,url='https://ccifellowship.org/books/book-of-praise/'+slug,text=t,status='附件阅读版 · 网站逐字核验未完成',note=f'用户提供的《敬拜赞美手册》（2015）印刷页 {a}–{b}，清理换行、页码与排版空白；内容含原书经文注释。不是已完成逐字校验的 CCI 网站转录。'))
snapshots=json.loads((root/'cci-snapshots.json').read_text(encoding='utf-8'))
for i,s in enumerate(snapshots):
    body='\n'.join(x['text'] for x in s['lines'] if x['n']>=4).strip()
    rows[i].update(text=body,status='CCI 网页可读取正文 · 2026-10-22',note='以用户所提供手册为交叉参考，按指定 CCI 网页可读取正文核对。保留该页面的文字、标点与编号，段落按网页文本排列；不是拉丁文或希腊文校勘本。',url=s['url'])
(root/'reading.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
print('Reading editions:',[(x['title'],len(x['text'])) for x in rows])
