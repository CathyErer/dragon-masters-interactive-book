# Dragon Masters Interactive Book · 本地候选

把有权使用的故事制作成场景优先、双语、可交互的浏览器读物。包含完整制作流程、可复制提示词、角色一致性与分状态绘图方法、音乐制作、数据驱动页面模板和检查工具。无需私人笔记库或原作者电脑。

**状态：0.2.0 本地审阅候选，未公开发布，作者 CathyErer，MIT 许可证。** 本目录没有第三方整书、角色素材或私人课程档案。已加入“使用者提供原书＋DM1制作配置”的同书工作流及固定轨迹拖动组件。原创三幕示例用于演示机制，不代表整本长篇书已一键自动化或通过独立复现。

## 五分钟运行

1. 用浏览器打开 `skills/dragon-masters-interactive-book/assets/starter/index.html`。
2. 点击 Open the book，再用顶部 Music 按钮试听。可观察空齿轮孔、拖动齿轮、按住红轮点灯，并完成三道题。
3. 点击 EN / 中英切换；刷新可恢复进度；Restart需要确认。
4. 若要新建自己的项目：在本目录运行以下命令（Python 3标准库，无第三方包）：

```sh
python3 skills/dragon-masters-interactive-book/scripts/new_project.py --destination ./my-book
python3 skills/dragon-masters-interactive-book/scripts/validate_book.py ./my-book
```

目标目录必须不存在，工具不会覆盖已有作品。直接打开`my-book/index.html`即可。若浏览器限制本地文件，运行`python3 -m http.server 8000 --directory my-book`，再访问本地8000端口。地址来源切换会使用另一份浏览器存档。

## 怎么制作一本新书

把`skills/dragon-masters-interactive-book/`交给支持本地Skill的助手，或直接把其中`SKILL.md`作为操作说明。公开候选的安装不是运行示例的前提。不要覆盖已有同名私用Skill；先放入独立测试环境。

开始时提供：可读取的书籍来源、使用范围、读者年龄/英文水平、输出语言、目标电脑尺寸、是否需音乐，以及角色/风格参考的使用许可。然后使用`references/prompts.md`的完整启动提示词。

| 制作环节 | 使用文件 | 交付物 |
|---|---|---|
| 来源、章节和分镜 | `references/workflow.md`、`prompts.md` | 带证据的场景表与连续性表 |
| 人物和绘图 | `references/art-direction.md` | 角色卡、状态图片、道具层、来源记录 |
| 音乐与声音 | `references/music.md`、`scripts/generate_score.py` | 情绪段落、循环音乐、切换点 |
| 互动与动画 | `references/interaction.md`、`assets/starter/app.js` | 真实操作、可见结果、Quiz、存档 |
| 接入自己的书 | `references/data-contract.md` | `story.json`和可直接打开的`story.js` |
| 修复与交付 | `references/qa.md`、`scripts/validate_book.py` | 技术检查和人工审阅清单 |

## 依赖、费用和人工步骤

- 示例浏览器运行不需要API、账号、网络、构建工具或付费音乐服务。示例音乐由附带脚本本地合成；可重新生成。
- 新故事的内容分析需要读到用户实际提供的材料。扫描书可能需要OCR或页面图检查；没有来源不能仅凭书名编造。
- 高质量插图需要用户可用的图像生成/编辑工具或画师。提示词和完整步骤已附；不同工具可能收费，费用与使用条款由所选服务决定，本套件不代购、不承诺免费或自动授权上传。
- 可用图像编辑器输出透明道具；可选Pillow用于图片压缩，不是运行模板的依赖。当前示例采用原创代码绘制SVG，来源及重建方式见`ASSET_PROVENANCE.md`；它是机制演示，不冒充精修2.5D书籍插画。
- 浏览器自动测试可选Node.js + Playwright；手动检查不要求安装它。`tests/browser.cjs`通过环境变量指定实际依赖，不硬编码某台电脑。
- 人工必须检查：原文含义、角色是否一致、动画是否自然、图中文字/道具是否正确、热点实际位置、音乐听感，以及发布材料的权利状态。

## 本版实现范围

已提供observe/drag/hold/trace基础组件，以及独立的固定轨迹sprite组件`track-flight.js`（距离自适应局部投影、连续位置、帧合并、transform、取消清理）。提供键盘替代、场景坐标、短气泡与Quiz分时显示、稳定乱序、EN/中英、存档、预解码、长按反馈、结果图、配乐淡化和静音记忆。示例直接覆盖observe/drag/hold；固定轨迹有独立快速拖动测试。trace保留参考实现，本版不宣称其独立专项已通过。不是骨骼动画、自由走路、在线多人或从PDF一键出整书。

## 同书制作与可复现构建

希望做《Rise of the Earth Dragon》时，提供实际可读取原书，使用`references/rise-of-the-earth-dragon.md`的完整启动提示词。它要求同一故事、证据对应、人物与剧情揭示一致；不会把灯塔示例当作替代故事，也不承诺像素级同图。角色参考由使用者在自己的项目中准备，不随公开包附送。

重建原创示例：`python3 skills/dragon-masters-interactive-book/scripts/build_demo.py`。重建后运行`validate_book.py`；浏览器测试：`node tests/browser.cjs`（需Playwright，必要时通过PLAYWRIGHT_MODULE和CHROME_PATH指定本机安装）。快速拖动、反复失焦取消和刷新保存均需实际测试。制作流程、人工视觉/听感以及独立整书复现的证据分别报告。

作者 CathyErer，采用 MIT 许可证（见 LICENSE）；许可范围见 ASSET_PROVENANCE.md。发布前请确认目标仓库。此候选不上传任何网站，不包含已发布仓库链接。
