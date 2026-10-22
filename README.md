# 圣约与荣耀 · 威斯敏斯特三大准则学习图谱

**主题：Westminster and Continental Reformed · 2026-10-22 · v1.0.0 · GTstudy**

创建于 2026-10-21，首版发布于 2026-10-22（Asia/Taipei）。仓库日期保留项目启动日；部署域名标示首版发布日期。

## 三个公开阅读地址

| 平台 | 地址 |
|---|---|
| GitHub Pages | https://07-je-gt-love-personal-20260918.github.io/westminster-20261021-v1-GTstudy/ |
| Surge | https://westminster-20261022-v1-gtstudy.surge.sh |
| Vercel | https://westminster-20261022-v1-gtstudy.vercel.app |

源代码：https://github.com/07-Je-GT-Love-Personal-20260918/westminster-20261021-v1-GTstudy

## 内容与功能

- 33 章信仰告白学习注释：核心、经文背景、历史问题、应用、误区、欧陆对读、记忆线索。
- 小要理 107 问、大要理 196 问的原创逐问释义，连接相关告白与圣经主题。
- 整本圣经故事、圣约神学、历史时间线、八个城市的可点击示意地图。
- 三份威斯敏斯特准则的目的、体裁、结构、关联及欧陆传统差异比较。
- 七篇主题深读、神学导航图、336 张主动回忆卡、遮字背诵、设备语音朗读。
- 可隐藏的详细目录、全文搜索、默认平铺、明暗主题、字号调整、打印与单文件离线版。
- 学习进度仅保存在当前浏览器；不同域名与设备不自动同步。

## 文本与范围说明

中文释义为原创学习辅助，不是信条译本或教会正式释义。全编号覆盖不等于已完成逐句逐分句的学术注释。

三份普世信经的正文按 CCI 指定页面的可读取文字保存，保留文字、标点、编号及来源快照。现代网页的段落空白与原始 HTML 字节不是同一概念，不宣称 HTML 字节级一致。

三项联合信条保留用户提供的《敬拜赞美手册》（2015）相应页的阅读版，已清理页码与排版换行，包含导言和经文注释。指定网站索引页只返回导言，其全文尚未完成逐字校验，界面明确标示。未宣称吸收 CCI 全站内容。

威敏主题与编号参考 OPC 现行标准，须区别 1646–1648 年历史文本与其后美国修订。主日、确据、圣约与“降在阴间”等差别保留说明，不将所有改革宗宗派视为同一无差别立场。

附件整份 PDF、账号密码、认证文件与凭据不进入仓库。第三方信经信条译文不因收入本项目而成为本项目原创作品。

## 本地运行与构建

需要 Python 3.11 或更新版；常规构建无第三方依赖。

```text
python build.py
python -m http.server 8765 --directory public
```

打开 http://127.0.0.1:8765 。直接打开 `public/study-offline.html` 可离线阅读，外部字体不可用时自动使用设备字体。

`content.json` 是 33+107+196 条释义的唯一维护源；`deepdives.json` 为主题文章；`reading.json` 为六份阅读文本；`cci-snapshots.json` 记录三份普世信经的网页文字快照；`index.html`、`app.js`、`style.css` 管理结构、交互与样式。构建输出在 `public/`，不需提交生成目录。

## 持续部署

GitHub Pages 与 Surge 在推送 `main` 后构建部署，也可在 Actions 手动重跑。Surge 的认证只保存在仓库加密 Secrets，名称为 `SURGE_LOGIN`、`SURGE_TOKEN`，不写入源文件。

Vercel 使用 `abners-projects-6f97a189/westminster-20261022-v1-gtstudy` 项目；生产部署前先运行 `python build.py`，然后 `vercel deploy --prod`。本版生产站已成功发布，但 Vercel 的 GitHub 仓库连接被平台拒绝，尚未启用其自动 Git 部署；当前通过本机已登录的 CLI 更新。GitHub Pages 与 Surge 的自动部署均已运行成功。

三份普世信经另提供 `creed-apostles.html`、`creed-nicene.html`、`creed-athanasian.html` 独立干净阅读页；全经故事支持逐站推演。`verify-public.yml` 可手动从公开网络校验三个站点是否允许匿名访问，并逐文件与同一构建比较。

## 版本与恢复

`v1.0.0-20261022` 为首版标签。每次更新应记录内容变化、校验结果及三平台部署状态，再新增版本标签，避免覆盖旧标签。

恢复查看旧版本：

```text
git fetch --tags
git switch --detach v1.0.0-20261022
python build.py
```

继续开发请创建新分支；需要重新发布旧版时，在新分支恢复对应文件并按部署流程发布。不要将旧版恢复解释为删除后续历史。

详细核验记录见 `VERIFICATION.md`；更新记录见 `CHANGELOG.md`。
