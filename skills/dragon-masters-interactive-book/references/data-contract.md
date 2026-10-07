# 运行数据与整书接入

先改story.json，再运行`python3 scripts/sync_story.py PROJECT/book`；story.js以普通script加载，支持本地file打开。模板不是PDF解析器，实际数据来自核实后的场景表。

顶层：schemaVersion=1，唯一id，title/description/ending为{en,zh}，music={mood:相对音频路径}，scenes数组。封面标题、描述和结束文案全部取自这里。不同书用不同id；改结构须设计迁移，不随意清空学生已有进度。

每幕：id、chapterId、eventIds、title、image、alt、source、reading、caption、instruction、music、action、result、quiz。除id/chapterId/eventIds/path/alt/source外，文字为{en,zh}。DM1制作门禁要求chapterId/eventIds；原创演示可不带。image与afterImage为同机位16:9画面。

- observe：`{type:"observe",at:[50,40],duration:800,label:{en:"Inspect",zh:"观察"}}`
- hold：同observe；需要持续按住，有可见进度。
- drag：`{type:"drag",from:[20,70],to:[65,50],radius:7,sprite:"art/prop.webp",label:{en:"Carry",zh:"移动"}}`
- trace：`{type:"trace",points:[[20,50],[40,40],[60,50]],label:{en:"Trace",zh:"循迹"}}`
- advance：`{type:"advance",label:{en:"Enter",zh:"进入"}}`；明确的故事行动按钮，配合afterImage/下一幕地点改变，不假扮复杂手势。
- track：`{type:"track",sprite:"art/sprite.webp",path:"M200 500 C400 150 600 850 800 500",width:18,label:{en:"Follow the wind",zh:"顺风飞行"}}`；path使用0..1000坐标，width为百分比，背景不包含该sprite的副本。末端松手才完成；箭头键循迹，Enter提交，Esc取消。没有afterImage时保留终点sprite；有afterImage时由结果图表达。通过后Replay flight可重玩，返回/切语言/完成重玩都保留已完成存档。

拖动物体与decoration可设置width（画面宽度百分比，默认8）和aspectRatio（宽/高，默认1）；idle/drag/placed及后续幕必须使用相同几何。长柄道具须按实图比例设置，检查落点中心与下一幕状态一致。

其他动作坐标使用0..100图片坐标。可选afterImage/afterAlt、resultMusic、decoration={sprite,at}。背景和独立sprite加载成功后才出现交互；素材失败显示Retry。

quiz可为null：动作完成→观察结果→Continue→下一幕。章级检查幕的quiz为`{question:{en,zh},hint:{en,zh},options:[{id,text:{en,zh}}],answer:"option-id"}`。DM1要求3个选项。Quiz期隐藏阅读、气泡和Journal；Review evidence返回结果，再进入题目。通过后可继续本章后续事件。

可选evidence={en,zh}：操作结果已提交后进入Journal，不提前揭示。

可选retell：`{prompt:{en,zh},items:[{id:"a",text:{en:"look",zh:"观察"}},{id:"b",text:{en:"repair",zh:"修理"}}],order:["a","b"]}`。出现在该幕通过后，关键词初始打乱，用Up/Down调整，Check sequence核对；随时可下一幕/合书，不能设成主线门槛。关键词必须依据本次书的原文，不使用示例结尾的词。

必需运行文件：index.html、style.css、app.js、track-flight.js、story.js、全部引用图/音频；story.json用于编辑。完整生产还要填production-records.md所列来源、状态和QA文件。
