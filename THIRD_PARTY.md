# 地图组件与数据

- Leaflet 1.9.4：从 npm 官方包取得 `leaflet.js` 与 `leaflet.css`，随项目本地提供。BSD-2-Clause 许可原文位于 `vendor/LEAFLET-LICENSE.txt`。未依赖第三方脚本 CDN 才能显示历史地图。
- Natural Earth 1:110m 国家轮廓：公共领域数据。来源为维护者仓库 `nvkelso/natural-earth-vector` 的 `geojson/ne_110m_admin_0_countries.geojson`；本项目抽取52个国家的简化外轮廓，坐标保留三位小数，以构建时生成的SVG显示。使用说明：https://www.naturalearthdata.com/about/terms-of-use/ 。现代疆界仅作城市定位参考，不表达历史或政治归属判断。
- 可选网络底图：Esri World Street Map 与 OpenStreetMap，按用户点击加载，保留服务归属说明。网络图像不在此仓库中打包，不承诺所有国家、地区或网络永久可用。
- OpenStreetMap： https://www.openstreetmap.org/copyright ；瓦片使用政策：https://operations.osmfoundation.org/policies/tiles/ 。不预取整片地图，不批量离线下载底图，尊重浏览器与服务缓存。
- 历史文化注释为原创学习辅助，城市叙事逐条附来源。示意图与现代地图分层，避免以今天的国界解释古代政治实体。
