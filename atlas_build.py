"""Build local, network-independent geography and historical concept maps."""
import json,html,math,pathlib
P=pathlib.Path(__file__).parent
def render_atlas():
    data=json.loads((P/'atlas-data.json').read_text(encoding='utf-8'))
    outlines=json.loads((P/'geo-outlines.json').read_text(encoding='utf-8'))
    views=[('europe','改革宗欧洲','宫廷、大学、城市与教会',[-12,23,42,61]),('east','圣经与大公教会','先辨救赎事件，再辨认信会议',[24,40,28,45]),('world','跨海与跨文化','文本、移民与本地牧养',[-132,43,19,66])]
    diagrams=[]
    for key,title,subtitle,bounds in views:
        west,east,south,north=bounds;cos=math.cos(math.radians((north+south)/2));scale=min(820/((east-west)*cos),420/(north-south))
        def xy(lng,lat):return 450+(lng-(west+east)/2)*cos*scale,250-(lat-(north+south)/2)*scale
        paths=[]
        for shape in outlines:
            rings=[]
            for ring in shape['rings']:
                if not any(west-8<=x<=east+8 and south-8<=y<=north+8 for x,y in ring):continue
                rings.append('M'+'L'.join(f'{xy(x,y)[0]:.1f},{xy(x,y)[1]:.1f}' for x,y in ring)+'Z')
            if rings:paths.append('<path d="'+''.join(rings)+'"><title>'+html.escape(shape['name'])+'</title></path>')
        relevant=[(i,x) for i,x in enumerate(data['places']) if x['region']==key or key=='world' and x['id'] in ['geneva','london','dort']]
        pins=[]
        for i,x in relevant:
            a,b=xy(x['lng'],x['lat']);dx,dy=(0,0)
            if key=='east' and x['id']=='constantinople':dx,dy=-22,-12
            if key=='east' and x['id']=='nicaea':dx,dy=16,13
            pins.append(f'<g class="atlas-pin" role="button" tabindex="0" aria-label="{html.escape(x["name"])}：{x["year"]}" data-city="{x["id"]}"><title>{x["name"]} · {x["year"]}</title><line x1="{a:.1f}" y1="{b:.1f}" x2="{a+dx:.1f}" y2="{b+dy:.1f}"/><circle cx="{a+dx:.1f}" cy="{b+dy:.1f}" r="15"/><text x="{a+dx:.1f}" y="{b+dy+5:.1f}" text-anchor="middle">{i+1}</text></g>')
        if key=='world':
            a,b=xy(4.69,51.81);c,d=xy(-112.845,49.696)
            routes=f'<path class="atlas-route" d="M{a:.1f},{b:.1f} Q{(a+c)/2:.1f},65 {c:.1f},{d:.1f}"/><text class="sea-label" x="430" y="100">二战后荷兰移民 → 加拿大</text>'
        elif key=='europe':
            routes='<text class="sea-label" x="80" y="370">不同处境，同受圣经检验</text>'
        else:routes='<text class="sea-label" x="65" y="410">事件先于认信，圣经高于信条</text>'
        svg=f'<svg class="atlas-svg" viewBox="0 0 900 500" aria-labelledby="atlas-title-{key}"><title id="atlas-title-{key}">{title}地理示意图</title><defs><clipPath id="clip-{key}"><rect x="25" y="20" width="850" height="460" rx="18"/></clipPath></defs><rect width="900" height="500" rx="22" class="sea"/><g clip-path="url(#clip-{key})"><g class="country-shapes">'+''.join(paths)+'</g>'+routes+''.join(pins)+'</g></svg>'
        chips=''.join(f'<button data-city="{x["id"]}"><span>{i+1:02d}</span> {x["icon"]} {x["name"]}</button>' for i,x in relevant)
        diagrams.append(f'<div class="atlas-pane" id="atlas-{key}" role="tabpanel" aria-labelledby="tab-{key}" {"hidden" if key!="europe" else ""}><p class="atlas-subtitle">{subtitle}</p>{svg}<div class="city-chips">{chips}</div></div>')
    cards=''.join(f'<article class="culture-card"><span class="culture-icon">{x["icon"]}</span><h3>{x["region"]}</h3><p class="label">真实压力</p><p>{x["pressure"]}</p><p class="label">形成的文体</p><p><strong>{x["form"]}</strong></p><p>{x["logic"]}</p><p class="culture-caution">{x["compare"]}</p><p class="source">'+ ' · '.join(f'<a href="{u}">{t}</a>' for t,u in x['refs'])+'</p></article>' for x in data['cultures'])
    first=data['places'][0]
    result='''<div class="atlas-heading"><p class="eyebrow">HISTORY × GEOGRAPHY × CULTURE</p><h3>先看处境，才听得懂认信在回答什么</h3><p>文化解释问题与文体，<strong>圣经判断真理</strong>；历史背景不能代替经文根据。</p></div><div class="atlas-tabs" role="tablist" aria-label="历史地理图层">'''+''.join(f'<button role="tab" id="tab-{k}" aria-controls="atlas-{k}" aria-selected="{str(k=="europe").lower()}" tabindex="{0 if k=="europe" else -1}" data-atlas-tab="{k}">{t}</button>' for k,t,_,_ in views)+'''</div><div id="atlasDiagrams">'''+''.join(diagrams)+'''</div><p class="source">图形与城市数据随网站保存，无需网络。地理轮廓采用 Natural Earth 简化数据；国界为现代定位参考，不代表历史疆界。弧线表示特定迁徙背景，不是个人旅行轨迹。</p><article id="cityStory" class="city-story" aria-live="polite"><p class="eyebrow">01 · LONDON · 1643–1647</p><h3>♜ 伦敦：战争中的教会改革</h3><p>选择图上的编号，联读当时处境、核心问题与认信回应。</p></article><div class="real-map-card"><div class="real-map-head"><div><span class="live-dot"></span><h3>在真实的现代地图上定位</h3><p>拖动、缩放，查看所选城市在今天的位置；历史疆界结合上方年代与背景阅读。</p></div><button id="loadRealMap">⊕ 加载现代地图</button></div><div class="map-tools" hidden id="mapTools"><label>底图<select id="mapProvider"><option value="esri">Esri 世界街道图</option><option value="osm">OpenStreetMap 街道图</option></select></label><button id="mapLocate">⌖ 返回所选城市</button><button id="mapOverview">▦ 当前图层全览</button><button id="mapPause">Ⅱ 关闭网络底图</button></div><div id="realMap" class="real-map" hidden aria-label="可交互的现代真实地图"></div><p id="mapStatus" class="map-status" aria-live="polite">离线示意图已就绪。需要时再加载网络底图，避免拖慢阅读。</p><div id="externalMaps" class="external-maps"></div></div><h3 class="culture-title">同一个信仰，为何长成不同的文本？</h3><div class="culture-grid">'''+cards+'''</div><div class="causal-strip"><div><b>✝ 逼迫</b><span>公开澄清信什么</span><strong>比利时信条</strong></div><div><b>▥ 教养</b><span>让信仰成为共同语言</span><strong>海德堡要理</strong></div><div><b>⚖ 争议</b><span>区分恩典与人的功劳</span><strong>多特信经</strong></div><div><b>♜ 改革</b><span>宣认、教导、敬拜与治理</span><strong>威敏三份准则</strong></div></div><div class="notice"><strong>记住四个动词：澄清、教养、辨析、整顿。</strong><br>这是文体与历史处境的学习概括，不是声称每份信条只有一个目的。读完再问：它怎样从圣经论证，而不只问它为何在当时流行？</div>'''

    boundaries="""<details class="history-boundaries"><summary>▤ 历史阅读的四条边界 · 点开自检</summary><div class="tablewrap"><table><thead><tr><th>容易混淆</th><th>历史辨析</th><th>记忆锚点</th></tr></thead><tbody><tr><td>把1561年的“比利时”当作今日国家</td><td>回到历史低地地区及其逼迫处境，再看现代城市位置。</td><td>历史区域 ≠ 今日国界</td></tr><tr><td>把写成、采纳、实施当作同一件事</td><td>伦敦会议写作、苏格兰总会采纳、各地实际实施，分别有其时间与主体。</td><td>写成 → 采纳 → 实施</td></tr><tr><td>把多特的五项教义当作全部改革宗神学</td><td>它针对特定争论作裁断；完整阅读还须连于三一、圣约、教会与生活。</td><td>争议焦点 ≠ 全部信仰</td></tr><tr><td>把海德堡的安慰文体当作教义较浅</td><td>安慰来自属于基督的真实关系，并展开救赎、信心与感恩的生活。</td><td>准确教义 → 真实安慰</td></tr></tbody></table></div></details>"""
    return result.replace('<div class="notice"><strong>记住四个动词',boundaries+'<div class="notice"><strong>记住四个动词')
