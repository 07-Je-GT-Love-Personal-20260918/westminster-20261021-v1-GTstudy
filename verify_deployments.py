"""Check anonymous public access and matching built bytes across the three hosts."""
import urllib.request,hashlib,pathlib,concurrent.futures,json
root=pathlib.Path(__file__).parent
urls={
 'GitHub Pages':'https://07-je-gt-love-personal-20260918.github.io/westminster-20261021-v1-GTstudy/',
 'Surge':'https://westminster-20261022-v1-gtstudy.surge.sh/',
 'Vercel':'https://westminster-20261022-v1-gtstudy.vercel.app/'
}
def check(item):
 name,base=item;result={'platform':name,'url':base,'checks':[]}
 for filename in ['index.html','app.js','data.js','style.css','reader.css','atlas.js','reader.js','vendor/leaflet.js','vendor/leaflet.css','vendor/LEAFLET-LICENSE.txt','study-offline.html','version.json','creed-apostles.html','creed-nicene.html','creed-athanasian.html']:
  try:
   with urllib.request.urlopen(base+filename,timeout=20) as r:body=r.read();status=r.status
   match=body==(root/'public'/filename).read_bytes()
   result['checks'].append({'file':filename,'status':status,'matchesBuild':match,'sha256':hashlib.sha256(body).hexdigest()})
  except Exception as e:result['checks'].append({'file':filename,'error':type(e).__name__})
 return result
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:results=list(pool.map(check,urls.items()))
print(json.dumps(results,indent=2))
assert all(x.get('status')==200 and x.get('matchesBuild') for r in results for x in r['checks']),'One or more public endpoints differ or are unavailable'
