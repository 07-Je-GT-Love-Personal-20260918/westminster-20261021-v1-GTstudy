/* Historical context stays local. Network basemaps are optional and load on request. */
(()=>{
 'use strict';
 const data=window.ATLAS_DATA;if(!data||!document.querySelector('#atlasDiagrams'))return;
 const qs=s=>document.querySelector(s),safe=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
 let selected=data.places[0],map=null,tiles=null,markers=[],provider='esri',generation=0,fallbackUsed=false,timeout=null;
 const status=s=>qs('#mapStatus').textContent=s;
 function city(id){
  const p=data.places.find(x=>x.id===id);if(!p)return;selected=p;
  qs('#cityStory').innerHTML=`<div class="city-story-heading"><span class="story-icon">${p.icon}</span><div><p class="eyebrow">${p.year} · 历史处境</p><h3>${safe(p.name)}：${safe(p.focus)}</h3></div></div><div class="city-facts"><div><h4>① 当时在哪里，面对什么？</h4><p>${safe(p.setting)}</p></div><div><h4>② 为什么必须回应？</h4><p>${safe(p.cause)}</p></div><div><h4>③ 产生什么认信回应？</h4><p>${safe(p.result)}</p></div></div><p class="memory-line">✦ ${safe(p.memory)}</p><p class="source">来源：${p.refs.map(([t,u])=>`<a href="${u}" target="_blank" rel="noopener">${safe(t)}</a>`).join(' · ')}</p>`;
  document.querySelectorAll('[data-city]').forEach(el=>{el.classList.toggle('selected',el.dataset.city===id);el.setAttribute('aria-pressed',el.dataset.city===id?'true':'false')});
  const lat=p.lat,lng=p.lng;
  qs('#externalMaps').innerHTML=`<span>也可直接打开：</span><a target="_blank" rel="noopener" href="https://www.openstreetmap.org/?mlat=${lat}&mlon=${lng}#map=11/${lat}/${lng}">OpenStreetMap ↗</a><a target="_blank" rel="noopener" href="https://www.google.com/maps/search/?api=1&query=${lat}%2C${lng}">Google Maps ↗</a><a target="_blank" rel="noopener" href="https://www.bing.com/maps?cp=${lat}~${lng}&lvl=11">Bing Maps ↗</a>`;
  if(map)map.setView([lat,lng],7,{animate:false});
 }
 city(selected.id);
 qs('#atlasDiagrams').addEventListener('click',e=>{const el=e.target.closest('[data-city]');if(el)city(el.dataset.city)});
 qs('#atlasDiagrams').addEventListener('keydown',e=>{const el=e.target.closest('.atlas-pin');if(el&&(e.key==='Enter'||e.key===' ')){e.preventDefault();city(el.dataset.city)}});
 const tabs=[...document.querySelectorAll('[data-atlas-tab]')];
 if('IntersectionObserver'in window)new IntersectionObserver(entries=>entries.forEach(x=>x.target.classList.toggle('is-visual-active',x.isIntersecting))).observe(qs('#atlasDiagrams'));
 function tab(key){tabs.forEach(b=>{let active=b.dataset.atlasTab===key;b.setAttribute('aria-selected',String(active));b.tabIndex=active?0:-1});document.querySelectorAll('.atlas-pane').forEach(el=>el.hidden=el.id!=='atlas-'+key);const first=data.places.find(x=>x.region===key);if(first)city(first.id)}
 window.addEventListener('gt-atlas-city',e=>{const p=data.places.find(x=>x.id===e.detail);if(p){tab(p.region);city(p.id)}});
 tabs.forEach((b,i)=>{b.onclick=()=>tab(b.dataset.atlasTab);b.onkeydown=e=>{let n;if(e.key==='ArrowRight')n=(i+1)%tabs.length;else if(e.key==='ArrowLeft')n=(i+tabs.length-1)%tabs.length;else if(e.key==='Home')n=0;else if(e.key==='End')n=tabs.length-1;else return;e.preventDefault();tab(tabs[n].dataset.atlasTab);tabs[n].focus()}});
 const providers={esri:{url:'https://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}',credit:'Tiles © Esri — Sources: Esri, HERE, Garmin, USGS, NGA, EPA, NPS',maxZoom:19},osm:{url:'https://tile.openstreetmap.org/{z}/{x}/{y}.png',credit:'© <a href="https://www.openstreetmap.org/copyright">OpenStreetMap contributors</a>',maxZoom:19}};
 function choose(value,automatic=false){
  if(!map)return;provider=value;qs('#mapProvider').value=value;generation++;const gen=generation;clearTimeout(timeout);if(tiles)map.removeLayer(tiles);let count=0,errors=0;
  const p=providers[value];status(`${value==='esri'?'Esri':'OpenStreetMap'} 底图请求中；离线历史图始终保留。`);
  tiles=L.tileLayer(p.url,{attribution:p.credit,maxZoom:p.maxZoom,keepBuffer:1,updateWhenIdle:true,updateWhenZooming:false}).addTo(map);
  const fail=()=>{if(gen!==generation||count>0)return;if(value==='esri'&&!fallbackUsed){fallbackUsed=true;choose('osm',true)}else status('网络底图暂不可用。城市坐标与上方历史示意仍可阅读；可切换底图或打开外部地图。')};
  tiles.on('tileload',()=>{if(gen!==generation)return;count++;clearTimeout(timeout);status(`${value==='esri'?'Esri':'OpenStreetMap'} 已返回地图瓦片 · 可拖动缩放${automatic?' · 已自动切换备用底图':''}。现代底图不表示历史疆界。`)});
  tiles.on('tileerror',()=>{if(gen!==generation)return;errors++;if(errors>=4&&count===0)fail();else if(errors>=4)status('部分地图瓦片未能返回；可切换底图。离线历史示意不受影响。')});
  timeout=setTimeout(fail,9000);
 }
 let loading=false;
 function resource(type,url){return new Promise((resolve,reject)=>{if(type==='style'&&document.querySelector('link[data-map-css]')?.sheet){resolve();return}if(type==='script'&&window.L){resolve();return}const el=document.createElement(type==='style'?'link':'script');if(type==='style'){el.rel='stylesheet';el.href=url;el.dataset.mapCss='true'}else el.src=url;const timer=setTimeout(()=>{el.remove();reject(Error('timeout'))},10000);el.onload=()=>{clearTimeout(timer);resolve()};el.onerror=()=>{clearTimeout(timer);el.remove();reject(Error('resource'))};document.head.append(el)})}
 async function load(){
  if(location.protocol==='file:'){status('离线文件保留三张完整示意图；请用下方入口打开在线地图，或回到网站加载交互底图。');return}
  if(map){qs('#realMap').hidden=false;map.invalidateSize();return}if(loading)return;loading=true;qs('#loadRealMap').disabled=true;status('准备本地地图组件…');
  try{
   await Promise.all([resource('style','vendor/leaflet.css'),resource('script','vendor/leaflet.js')]);
   qs('#realMap').hidden=false;qs('#mapTools').hidden=false;
   map=L.map('realMap',{scrollWheelZoom:false,zoomAnimation:false,fadeAnimation:false,markerZoomAnimation:false,attributionControl:true}).setView([selected.lat,selected.lng],7);
   markers=data.places.map((p,i)=>L.circleMarker([p.lat,p.lng],{radius:7,color:'#fff',weight:2,fillColor:'#bd623c',fillOpacity:1}).addTo(map).bindTooltip(`${i+1}. ${safe(p.name)}`).on('click',()=>city(p.id)));
   fallbackUsed=false;choose(provider);qs('#loadRealMap').textContent='现代地图面板已打开';requestAnimationFrame(()=>map?.invalidateSize());
  }catch{status('地图组件未能加载。离线历史示意仍然可用；请使用下方外部地图入口。');qs('#loadRealMap').textContent='重试加载现代地图'}
  finally{loading=false;qs('#loadRealMap').disabled=false}
 }
 qs('#loadRealMap').onclick=load;
 qs('#mapProvider').onchange=e=>{fallbackUsed=false;choose(e.target.value)};
 qs('#mapLocate').onclick=()=>map?.setView([selected.lat,selected.lng],9,{animate:false});
 qs('#mapOverview').onclick=()=>{if(!map)return;const key=tabs.find(x=>x.getAttribute('aria-selected')==='true').dataset.atlasTab,points=data.places.filter(x=>x.region===key||key==='world'&&['geneva','london','dort'].includes(x.id)).map(x=>[x.lat,x.lng]);map.fitBounds(L.latLngBounds(points),{padding:[26,26],animate:false})};
 qs('#mapPause').onclick=()=>{generation++;clearTimeout(timeout);if(map){map.remove();map=null;tiles=null;markers=[]}qs('#realMap').hidden=true;qs('#mapTools').hidden=true;qs('#loadRealMap').textContent='⊕ 加载现代地图';status('网络底图已关闭，停止请求新瓦片。离线历史示意仍可使用。')};
})();
