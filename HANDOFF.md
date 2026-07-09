# HANDOFF — davinci-bot.ai(给 Claude Code 的继续开发说明)

这份文档面向接手继续开发的人/Agent。先读 `README-交接说明.md`(完整工程说明),
本文件只补充「当前状态 + 待办 + 坑」三件事。

---

## 0. 一分钟上手

```bash
# 依赖:Node 18+、Python 3、pip
pip install fonttools brotli          # 仅字体重新子集化时需要
# 改源码 → 只改 index.html,然后:
python3 build.py                       # 生成 davinci-v3-preview.html(自包含成品)
# 部署:把 davinci-v3-preview.html 复制成 index.html 拖到 app.netlify.com/drop
```

**铁律:只改 `index.html`(源文件)。`davinci-v3-preview.html` 是构建产物,不要手改。**
`build.py` 会把 three.js、字体 b64、assets 图片全部内联进产物。

> **Windows 本机(第4轮环境)**:Python 装在 `%LOCALAPPDATA%\Programs\Python\Python312`,
> fonttools/brotli 装在 `davinci\.tooling\pylibs`(因 C 盘满,装到了 D 盘)。直接跑:
> ```powershell
> powershell -File davinci-source\build.ps1        # 构建(自带 PYTHONPATH/TEMP 环境)
> powershell -File - <<...  或手动:$env:PYTHONPATH='...\.tooling\pylibs'; python subset.py; python build.py
> ```
> 加了新中文文案后:先 `subset.py`(收字→子集化两字重→写 font-900/700.b64),再 `build.ps1`。
> `build.py` 已加 `encoding='utf-8'`(中文 Windows 默认 GBK 会导致读取崩溃)。

建议第一步先 `git init` 建仓,之后每次改动提交,替代之前来回传 ZIP 的方式。

---

## 1. 架构速记(细节见 README)

- 纯前端单页,无框架。一个 Three.js 场景,相机随滚动沿 -Z 前进。
- 滚动进度 `p`(0–1)由 `#spacer` 高度(当前 `1050vh`)驱动,全部逻辑在 `tick()`。
- `HERO_END=0.11`:`pf` 驱动首屏+钻隧道;`ps` 驱动之后的内容段。
- **`ps` 时间轴(改动画必看,各段首尾不要重叠;第6轮重排,spacer=1150vh):**
  | ps 区间 | 内容 |
  |---|---|
  | 0–0.27 | 三拍能力序列,边界 `0 / BB1=0.07 / BB2=0.17 / BEATS_END=0.27`(拍1窗口更短,补偿英雄段尾部驻留 → 三拍**体感等长**) |
  | 0.282–0.317 | 三拍序列退场 |
  | 0.27–0.50 | 粒子「释放」:warp 冲刺 bell 0.27–0.47、半径外扩 0.30–0.50、去雾化淡出 0.36–0.50、色调 蓝→青 0.30–0.52 |
  | 0.335–0.465 | 大标题(穿过粒子风暴飞入;正中居中、字号 clamp(30,4.6vw,64)) |
  | 0.50–1.0 | **交互式现场总图 `#fieldMap`**:入场是「穿出隧道拉升俯瞰」(`mapIn` ps 0.50–0.60,scale 2.6→1,同时隧道环/壁 ×(1-mapIn) 退场),到站后锚点错峰浮现(`.arrived`)。SVG 总平面图(程序生成 13 条等高线 + 用地红线/尺寸标注/高程点工程图层 + 巡逻路线 + 巡行光点),5 个锚点;点击 01–04 → 画中画 `#pip`(视频+标题+简介+四要点,PCB 连线从锚点引出);05+「更多巡检场景」→ `#solGrid` 矩阵。图例在左下(手机在顶部),XY 读数右下。`.live` 控制 pointer-events,滚离自动关面板停视频 |
  相机:`BEATS_END=0.27` 前全速 470,减速至 `EASE_END=0.46`,之后慢速 150。
  手机端:地图变顶部含视图(aspect 1000/560),锚点只留光点,下方 chips 列表承载标题;画中画变底部抽屉。锚点定位是 JS 按 cover(slice) 数学换算(`placeAnchors`),改 viewBox 或锚点坐标要同步 `MAP_ANCHORS`。
- 场景框、四拍 intro、大标题都是 **HTML overlay + CSS 3D translateZ**,不是 3D 物体。
- 机器狗是 **PNG**(无 .glb,不能做成可旋转 3D,已与用户确认)。

---

## 2. 已完成 ✅

- 首屏 Hero:不对称编辑式排版(小标 + 主标题「自主巡检/专家」+ 说明 + 右侧机器狗 +
  左下 01–04 功能切换 bar)。**电脑端刚调过**:删了右下 HUD 和左下 chip,标题字号缩小防重叠、
  重排填满左栏,宋体统一成黑体。
- 机器狗被吸入隧道(已缩短)。
- 第一段隧道:四拍能力升级序列(带步骤导轨)。
- 第二段隧道:大标题(已下移)。
- 六个应用场景:粮仓→园区安防→半导体→能源涵洞→变电站→数据中心(3D 纵深进出 + PCB 走线)。
- 手机端场景内容垂直居中修正。
- 字体子集化,`fonts-full/` 附完整字体可自包含重切。
- **【第4轮】电影段之后接常规滚动信息版块**:三款机器人产品(M20/S10/X30,真实参数,`#products`)+ 预约演示/联系(`#contact`)+ 页脚。
  新架构:`#spacer` 之后加 `#site` 容器承载常规滚动内容,`p` 改为只由 spacer 自身范围驱动(见 README 第4轮说明)。字体重切到 344 字。

## 3. 待办 ⬜(用户想继续做的部分,官网 davinci-bot.ai 有参考)

按官网信息架构,场景段之后大致还缺:

1. ~~**三款机器人产品**:M20 / S10 / X30~~ —— **已做(第4轮,`#products`)**。以后 2–6 各段照抄 `#products`/`#contact` 的写法往 `#site` 里加即可。
2. ~~**载荷上装模块**~~ —— **已做(第11轮)**:与三款机器人合并成 `#products` 换装间配置器(左参数卡/中展示台/右模块抽屉/下机型轮转),八模块规格全录。
3. ~~**AI 巡检能力清单**~~ —— **已做(第14轮)**:15 项全录,做成换装间页面的第二幕(轨道卫星 + iOS 快捷列表 + 左右详情卡)。
4. ~~**巡检管理平台**~~ + 5. ~~**巡检流程闭环**~~ —— **已做(第15轮)**:合并为 `#platform` 苹果发布会式 bento 整页(大图=控制中心/风险分析,数据瓦=统计+MQTT/HTTP,五步流程+闭环瓦)。
6. **公司介绍 / 合作 / 联系方式 / 页脚**:预约演示、邮箱 bd@davinci-bot.com、
   地址(杭州西湖区玉古路 172 号 / 深圳福田区)、社媒。

> 做新段落时保持既有设计语言(见 README「设计语言」):石墨黑底、发丝测量网格、
> HUD 边框角标、等宽数据读数、单一电光青 `#37e0f2`。避免左对齐单列套路,用不对称编辑式网格。
> 效果要服务内容,别加无意义的装饰粒子。场景描述用连贯句子,不要碎词堆叠。

---

## 4. 坑 / 注意事项 ⚠️

1. **字体子集化(最容易踩)。** 中文用思源黑体的**子集化**字体,只含当前页面出现过的字。
   **新增任何页面里还没出现过的中文字,不重新子集化就会掉成系统字体(Windows 上是宋体)。**
   - 重切流程见 README「字体重新子集化方法」,`fonts-full/` 已附完整字体,**不依赖网络**。
   - 加完新文案,务必按页面全部用字重新跑 `pyftsubset` 两个字重 → 重新 base64 → `build.py`。
   - 校验:`python3 -c "from fontTools.ttLib import TTFont; print(len(TTFont('sub-900.woff2').getBestCmap()))"`
     数字应等于 chars.txt 字数。

2. **等宽字体没有中文字形。** `--fm`(SF Mono 等)只用于纯数字/英文读数。
   任何**含中文**的文字都要用 `--fb` 或 `--fd`(思源黑体 + CJK 回退),否则回退成宋体。
   —— 上一轮就是修这个。加新组件时别把中文塞进 `--fm`。

3. **改滚动动画时校验时间轴不重叠。** 各段的 `ps` 窗口(见上表)首尾不能压到一起。
   之前是用 Python 数值模拟 `tick()` 的关键量(opacity/z/active-beat)来验证的,
   在没有浏览器的环境里这是唯一手段。

4. **本地可以真截图(相对之前沙箱的升级)。** 之前的构建环境下载不了 Playwright 浏览器,
   只能靠数值模拟验证 3D 滚动状态。**在本地机器上 Code 可以跑 Playwright / 真实浏览器**,
   建议对关键滚动位(首屏、四拍每拍、大标题、每个场景)截图目视确认,比纯数值模拟可靠得多。
   ES module 在 `file://` 下有 CORS 问题 —— 这也是构建时把 three.js 转成全局 classic script 的原因;
   截图时用本地 http server(如 `python3 -m http.server`)打开产物,别直接 `file://`。

5. **用户的工作方式**:主要用中文沟通;手机端(微信/App)审阅,红圈批注截图给精确反馈;
   偏好「先简短确认理解 → 再动手大改」,重视对需求理解的准确性胜过交付速度;
   大改前最好先复述一遍要做什么。手机端布局别搞臃肿。

---

## 5. 文件清单(简)

- `index.html` —— 源文件,**改这个**
- `build.py` —— 构建脚本
- `three.global.js` —— Three.js 全局版
- `font-900.b64` / `font-700.b64` —— 子集化字体(base64)
- `fonts-full/` —— 原始完整字重(重切用,自包含)
- `assets/` —— 图片(robot.png / logo.png / tunnel.jpg / 六张场景图)
- `davinci-v3-preview.html` —— 构建产物(=部署用 index.html)
- `README-交接说明.md` —— 完整工程说明
- `HANDOFF.md` —— 本文件
