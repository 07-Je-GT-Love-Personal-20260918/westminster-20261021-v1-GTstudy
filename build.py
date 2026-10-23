"""Dependency-free static packaging; all authored sources remain reviewable."""
import json,pathlib,shutil,html as html_utils
from atlas_build import render_atlas
p=pathlib.Path(__file__).parent
d=json.loads((p/'content.json').read_text(encoding='utf-8-sig'))
for key,count in [('wcf',33),('sc',107),('lc',196)]:
    assert len(d[key])==count,(key,len(d[key]))
    assert [x.get('n',i+1) for i,x in enumerate(d[key])]==list(range(1,count+1)),key
reading=json.loads((p/'reading.json').read_text(encoding='utf-8-sig'))
essays=json.loads((p/'deepdives.json').read_text(encoding='utf-8'))
atlas=json.loads((p/'atlas-data.json').read_text(encoding='utf-8'))
script='window.STUDY_DATA='+json.dumps(d,ensure_ascii=False)+';\nwindow.READING_DATA='+json.dumps(reading,ensure_ascii=False)+';\nwindow.DEEP_DIVES='+json.dumps(essays,ensure_ascii=False)+';\nwindow.ATLAS_DATA='+json.dumps(atlas,ensure_ascii=False)+';'
(p/'data.js').write_text(script,encoding='utf-8',newline='\n')
out=p/'public';out.mkdir(exist_ok=True)
for stale in [out/'CNAME',*out.glob('_qa*')]:
    if stale.is_file():stale.unlink()
for name in ['index.html','style.css','reader.css','app.js','atlas.js','reader.js','data.js']:
    (out/name).write_text((p/name).read_text(encoding='utf-8'),encoding='utf-8',newline='\n')
html=(p/'index.html').read_text(encoding='utf-8').replace('<!--ATLAS-->',render_atlas())
(out/'index.html').write_text(html,encoding='utf-8',newline='\n')
for name in ['style.css','reader.css']:
    html=html.replace(f'<link rel="stylesheet" href="{name}?v=20261023-v11">','<style>'+(p/name).read_text(encoding='utf-8')+'</style>')
for name,body in [('data.js',script),('app.js',(p/'app.js').read_text(encoding='utf-8')),('atlas.js',(p/'atlas.js').read_text(encoding='utf-8')),('reader.js',(p/'reader.js').read_text(encoding='utf-8'))]:
    html=html.replace(f'<script src="{name}?v=20261023-v11"></script>','<script>'+body+'</script>')
(out/'study-offline.html').write_text(html,encoding='utf-8',newline='\n')
for i,slug in enumerate(['apostles','nicene','athanasian']):
    item=reading[i]
    clean='<!doctype html><html lang="zh-Hans"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+item['title']+' · 干净阅读版</title><link rel="stylesheet" href="style.css?v=20261023-v11"><link rel="stylesheet" href="reader.css?v=20261023-v11"></head><body class="no-toc"><header><a class="brand" href="index.html#texts">← 返回学习图谱</a><button onclick="window.print()">打印</button></header><main><section><h1>'+item['title']+'</h1><div class="clean-text">'+html_utils.escape(item['text'])+'</div><p class="source">原文来源：<a href="'+item['url']+'">CCI '+item['title']+'</a> · 网页可读取正文核对日期 2026-10-22</p></section></main><script src="reader.js?v=20261023-v11"></script></body></html>'
    (out/f'creed-{slug}.html').write_text(clean,encoding='utf-8',newline='\n')
(out/'version.json').write_text(json.dumps({'topic':'Westminster and Continental Reformed','version':'v1.1.0','started':'2026-10-21','published':'2026-10-23','chapters':33,'shorter':107,'larger':196,'atlasPlaces':12,'localMaps':3},indent=2),encoding='utf-8',newline='\n')
shutil.copytree(p/'vendor',out/'vendor',dirs_exist_ok=True)
for asset in (out/'vendor').rglob('*'):
 if asset.suffix in {'.js','.css','.txt'}:
  asset.write_bytes(asset.read_bytes().replace(b'\r\n',b'\n'))
(out/'.nojekyll').touch()
snapshots=json.loads((p/'cci-snapshots.json').read_text(encoding='utf-8'))
for i,s in enumerate(snapshots):
    assert reading[i]['text']=='\n'.join(x['text'] for x in s['lines'] if x['n']>=4).strip(),reading[i]['title']
print('Verified 33 chapters + 107 questions + 196 questions; 6 reading texts. Packaged public/.')
