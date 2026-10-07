# 可执行的制作记录

`new_project.py`创建下列文件。字段未知用空值与待补状态；禁止为了通过检查虚构证据。

- SOURCE.md：原书文件/版本、使用范围、页码对应、扫描缺口、角色参考与未核项。原始书籍放在使用者的私用输入目录。
- chapter-evidence.csv：chapter_id、event_id、locator、fact、kind（source/adaptation）、status。每个必需事件至少有一个真实locator和核对后的fact；不要将检查表当locator。
- character-bible.md：逐人/龙固定身份、原页/参考ID、角色配对、尺度、批准图和禁止改变项。
- scene-state-table.json：`[{id, chapterId, eventIds, entry, action, result, exit, next}]`。entry/exit为对象；前幕exit等于后幕entry。变化发生在action/result内，省略的转换必须补一幕。最后next为null。
- prompts.jsonl：每条`{id,stage,sceneIds,references,prompt,tool,output,review}`；保存实际采用的提示词，失败图不能标通过。
- art-provenance.json：`[{path,promptId,origin,rights,review}]`，path相对book，origin标明原创/获准素材，rights写实际许可或用户确认的私用范围；运行中的图、sprite和音频都要登记，不能把未知写MIT。
- music-cues.json：`[{sceneId,before,after,reason}]`，mood键对应story.json的music，reason依据当时事件。
- qa/report.json：`{runtimeSha256, checks:[{name,status,evidence}]}`。hash由实际book文件计算；status为pass/fail/pending；evidence记录真实命令或审阅结果。技术测试和人工检查分项。
- production.json：顶层profile、status、source、chapters、bookDirectory、qaReport。每章`{id,sourceStatus,requiredEvents,sceneIds,quizSceneId,retellSceneId}`。DM1章ID为ch01…ch16，待补项初始为空。

## 与运行数据对应

story.json的scene需要chapterId和eventIds，与表和production.json一致。source写实际原书定位；一幕可覆盖多个事件，一个事件也可分几幕表达。按事件清单查漏，不以16张图或16个标题充当整书覆盖。

每章只有quizSceneId指向的幕含Quiz（3个选项）；其他幕quiz:null。Ch4/8/12/16的一幕可带retell，数据见data-contract；retellSceneId指向它。章末必须经过该章检查点，但其后允许继续当前章事件。新的制作计划若改变该合同，应记录用户明确要求，不能为了通过工具偷偷删事件。

QA必查名称：`source-evidence`、`normal-route`、`reduced-motion-route`、`language-reload`、`input-cancellation`、`asset-failure-retry`、`quiz-no-leak`、`visual-review`、`music-listening`。`validate_production.py`只接受真实记录；pending会阻止宣称整书完成。教师/课堂状态另记，不自动要求或伪写为pass。

## 完成检查

`python3 scripts/validate_production.py PROJECT`检查记录、章节/事件/scene、相邻状态、素材路径、实际运行哈希及QA状态。它是覆盖门禁，不是自动事实审稿：写了“verified”仍需出示真实页码与审阅证据。仅做规划时保留planning并交付缺口，不要伪造完成报告。
