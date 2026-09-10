# 数据与接入自己的书

复制starter到新目录；先改story.json，再运行`python3 scripts/sync_story.py <project>`生成story.js。页面使用普通script标签而非fetch，所以可直接file打开。不把JSON当不可信代码执行。

顶层：schemaVersion=1，id（新书唯一键），title={en,zh}，music={mood:相对音频路径}，scenes数组。每幕必须有稳定id、title、image、alt、source（原书页码或原创段号）、reading、caption、instruction、music、action、result和quiz。除alt/source/id/path外，文字均为{en,zh}。

action形状：

```json
{"type":"observe","at":[50,40],"duration":800,"label":{"en":"Inspect","zh":"观察"}}
```

```json
{"type":"drag","from":[20,70],"to":[65,50],"radius":7,"sprite":"art/prop.webp","label":{"en":"Carry","zh":"移动"}}
```

hold与observe字段相同。trace改成`points:[[20,50],[40,40],[60,50]]`并保留label，不需要at/duration。每个点是图片百分比坐标。

可选afterImage/afterAlt是动作完成后的同镜头图；resultMusic指定成功阶段音乐。decoration={sprite,at}放置上一幕已提交的道具。

quiz：question、hint为双语；options=[{id,text:{en,zh}}]，answer是其中一个id。id必须唯一，不把正确答案写进选项编号或固定第一位。

必需运行文件：index.html、style.css、app.js、story.js及引用的art/audio。story.json留作编辑。演示模板没有整书解析器；AI/制作者需依据证据表填写每幕并验证。改变状态结构时提高version并设计迁移，不能随意清空用户存档。
