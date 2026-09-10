# 发布候选与使用入口

当前为 0.2.0 本地审阅候选，作者 CathyErer，采用 MIT 许可证，尚未公开发布。

## 包内有什么

- `skills/dragon-masters-interactive-book/`：完整 Skill。导入支持本地 Skill 的助手时选此目录，不是上层仓库目录。
- `skills/dragon-masters-interactive-book/assets/starter/index.html`：无需安装 Skill 即可打开的原创三幕演示。
- `references/prompts.md`（Skill 内）：从原书到绘图、配乐、交互和验收的分步提示词。
- `references/rise-of-the-earth-dragon.md`（Skill 内）：用户自行提供原书的同书制作配置。
- `tests/`、`scripts/`、`QA.md`：回归测试、脱敏与打包工具、证据边界。

本包不包含第三方完整书籍、私用成品图片、个人资料或服务凭证。原创演示不是目标书替代品；完整插图制作仍需要可用绘图工具、适当参考和人工审阅。

## 本地候选打包

在仓库根目录运行：

```sh
python3 scripts/package_candidate.py --destination ../candidate-output
```

生成 ZIP 与逐文件 SHA256 清单；目标已有同名文件时拒绝覆盖。包使用固定内部时间戳，不带电脑用户名／绝对路径。此命令不上传、不创建仓库、不自动选择许可证。

## 正式发布前

1. 已确认作者 CathyErer 与 MIT 许可证；范围见 ASSET_PROVENANCE.md。根目录与独立Skill目录均含LICENSE。
2. 确认目标仓库和发布授权；上传前核对当前包与源文件一致。
3. 回读公开包，检查解压资源、哈希与独立运行；记录未完成的新用户整书复现和人工验收，不将候选测试当成这些验收。

许可证已确认不等于已上传发布；仓库和远程发布仍待确认。
