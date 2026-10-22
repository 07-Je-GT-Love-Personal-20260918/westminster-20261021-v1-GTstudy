"""Dependency-free static packaging; all authored sources remain reviewable."""
import json,pathlib,shutil,html as html_utils
p=pathlib.Path(__file__).parent
d=json.loads((p/'content.json').read_text(encoding='utf-8-sig'))
for key,count in [('wcf',33),('sc',107),('lc',196)]:
    assert len(d[key])==count,(key,len(d[key]))
    assert [x.get('n',i+1) for i,x in enumerate(d[key])]==list(range(1,count+1)),key
reading=json.loads((p/'reading.json').read_text(encoding='utf-8-sig'))
essays=json.loads((p/'deepdives.json').read_text(encoding='utf-8'))
script='window.STUDY_DATA='+json.dumps(d,ensure_ascii=False)+';\nwindow.READING_DATA='+json.dumps(reading,ensure_ascii=False)+';\nwindow.DEEP_DIVES='+json.dumps(essays,ensure_ascii=False)+';'
(p/'data.js').write_text(script,encoding='utf-8',newline='\n')
out=p/'public';out.mkdir(exist_ok=True)
for stale in ['_qa.html','CNAME']:
    if (out/stale).exists():(out/stale).unlink()
for name in ['index.html','style.css','app.js','data.js']:
    (out/name).write_text((p/name).read_text(encoding='utf-8'),encoding='utf-8',newline='\n')
html=(p/'index.html').read_text(encoding='utf-8')
html=html.replace('<link rel="stylesheet" href="style.css?v=20261022-v1">','<style>'+(p/'style.css').read_text(encoding='utf-8')+'</style>')
html=html.replace('<script src="data.js?v=20261022-v1"></script>','<script>'+script+'</script>').replace('<script src="app.js?v=20261022-v1"></script>','<script>'+(p/'app.js').read_text(encoding='utf-8')+'</script>')
(out/'study-offline.html').write_text(html,encoding='utf-8',newline='\n')
for i,slug in enumerate(['apostles','nicene','athanasian']):
    item=reading[i]
    clean='<!doctype html><html lang="zh-Hans"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+item['title']+' · 干净阅读版</title><link rel="stylesheet" href="style.css?v=20261022-v1"></head><body class="no-toc"><header><a class="brand" href="index.html#texts">← 返回学习图谱</a><button onclick="window.print()">打印</button></header><main><section><h1>'+item['title']+'</h1><div class="clean-text">'+html_utils.escape(item['text'])+'</div><p class="source">原文来源：<a href="'+item['url']+'">CCI '+item['title']+'</a> · 网页可读取正文核对日期 2026-10-22</p></section></main></body></html>'
    (out/f'creed-{slug}.html').write_text(clean,encoding='utf-8',newline='\n')
(out/'version.json').write_text(json.dumps({'topic':'Westminster and Continental Reformed','version':'v1.0.0','started':'2026-10-21','published':'2026-10-22','chapters':33,'shorter':107,'larger':196},indent=2),encoding='utf-8',newline='\n')
(out/'.nojekyll').touch()
snapshots=json.loads((p/'cci-snapshots.json').read_text(encoding='utf-8'))
for i,s in enumerate(snapshots):
    assert reading[i]['text']=='\n'.join(x['text'] for x in s['lines'] if x['n']>=4).strip(),reading[i]['title']
print('Verified 33 chapters + 107 questions + 196 questions; 6 reading texts. Packaged public/.')
