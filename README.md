# Dragon Masters Interactive Book

**0.3.0 · CathyErer · MIT**

面向《Dragon Masters #1: Rise of the Earth Dragon》的完整互动书制作 Skill：从使用者提供的原书，到逐章证据、人物与场景、插图、音乐、真实互动、连续故事、检查与交付。需要可读取的原书和制作工具；没有附送原书或私人整书成品。

## 安装与调用

下载本仓库，将`skills/dragon-masters-interactive-book/`整个文件夹放进你的助手支持的Skills目录。必须包含references、scripts与assets，不能只复制SKILL.md；也可将整个文件夹交给能读取本地文件的助手。仓库ZIP是完整项目，`.skill`安装包只含Skill文件夹；不同客户端安装方式以其支持方式为准。

调用示例：

```text
请使用 dragon-masters-interactive-book，制作《Rise of the Earth Dragon》第一本互动书。
原书：[实际文件与版本]；用途：[有权使用的范围]；读者：[年龄/英文水平]；
视觉参考：[允许使用的文件或待补]；输出：[新的项目目录]。
请读取整本，先完成16章证据、人物与场景/衔接设计，再给我样章审阅。
确认后继续完整制作，保留连续故事、English/中英、剧情音乐、16个章级Story Check、
四个不阻挡主线的可选Retell及证据记录。把原书内容落实到画面、操作和可见结果。
不要把灯塔示例换个书名当交付，不要从记忆补缺页。列明缺项和实际测试范围。
```

明确只给一章时只做该章；不要虚构其余章节。已有同一范围的批准不重复询问；用户要求先讨论时停止在方案。

## 制作 DM1：唯一入口

```sh
python3 skills/dragon-masters-interactive-book/scripts/new_project.py --destination ./my-dm1
```

只生成《Rise of the Earth Dragon》第一本的制作工程：`SOURCE.md`、16章`production.json`、证据CSV、人物表、场景状态表、提示词/素材记录、音乐表和QA记录。`engine-reference/`是没有故事内容的引擎骨架，不含灯塔场景或示例音频；完成原书与样章核对后，实际作品放`book/`。

本Skill仅用于制作DM1，不提供原创故事模式或运行示例的使用选项。缺原书时保持待补；不能把测试素材改名当成DM1交付。

## 全流程文件

| 阶段 | 入口 | 可检查产出 |
|---|---|---|
| 读原书、查缺页 | references/workflow.md | 版本、页码、章节与必需事件 |
| DM1逐章设计 | references/rise-of-the-earth-dragon.md、dm1-chapter-checkpoints.md | 全16章事件/场景覆盖、揭示时序 |
| 人物与绘图 | references/art-direction.md、prompts.md | 身份参考、前后状态、透明道具、实际图 |
| 音乐制作 | references/music.md | 事件情绪表、本地音频、来历和试听 |
| 互动与页面 | references/interaction.md、data-contract.md | 多幕章节、手势、状态、Quiz/Journal/Retell |
| 记录和验收 | references/production-records.md、qa.md | 来源对照、素材来历、哈希与真实测试 |

运行模板支持observe、drag、hold、trace、advance及固定轨迹sprite；每幕可无Quiz，多幕共享章级检查；包含可选关键词排序复述和已完成证据Journal。封面、说明、结尾从书籍数据读取。更复杂的擦除、分层人物演出或连续镜头需要按计划扩展并测试，不会被一个通用按钮自动替代。

## 制作检查

```sh
python3 skills/dragon-masters-interactive-book/scripts/sync_story.py my-dm1/book
python3 skills/dragon-masters-interactive-book/scripts/validate_book.py my-dm1/book
python3 skills/dragon-masters-interactive-book/scripts/validate_production.py my-dm1
```

第一项同步可直接本地打开的数据；第二项查运行依赖和字段；第三项查16章事件、顺序、衔接、检查点、可选复述、素材来源与当前QA记录。缺项会失败，不能只靠16个标题冒充整书。

依赖：Python 3.9+标准库；作品运行无需账号/API/网络。新书图像需可用的图像工具或画师，可能有成本；音乐可用附带本地生成器试配。人工需核对来源、角色、画面、操作手感与听感。不得把原书/参考素材自动上传外部服务。

开发验证：`python3 tests/contracts.py`；`node tests/browser.cjs`与`node tests/production-browser.cjs`需Playwright，可用PLAYWRIGHT_MODULE与CHROME_PATH指定本机依赖。完整命令与证据范围见QA.md。

**证据边界：**内部组件回归、缺项拦截以及隔离调用审查分别记录；没有据此声称另一位使用者已独立生成并验收整本DM1。AI插图与音乐也不保证与私用成品相同。

## 许可和交付

代码、制作说明及原创示例采用MIT，见LICENSE和ASSET_PROVENANCE.md。Dragon Masters书籍文字、角色及第三方视觉参考不因该许可获得再发布权；使用者提供的来源保留在自己的授权项目中。

仓库：[CathyErer/dragon-masters-interactive-book](https://github.com/CathyErer/dragon-masters-interactive-book)。本仓库发布DM1制作工具；内部原创测试素材仅用于开发回归，不是面向使用者的制作模式。不附私人笔记、原书PDF、人物素材或私人课堂成品。打包：`python3 scripts/package_candidate.py --destination NEW_OUTPUT_DIR`。
