# 字帖库 AI 练字助手

让 AI 帮你选练习、安排练法，并生成可在字帖库预览、调整、下载 PDF 和 A4 打印的字帖。

支持姓名练字、汉字描红、拼音、笔顺、基础笔画、控笔线条和古诗字帖。当前 Skill 主分支包含最新修复。`v0.5.1` 标签保留为此前的固定快照。

## 选择常用 AI，复制指令

在[平台使用指南](https://zitieku.com/ai-zitie/start/)选择 WorkBuddy、豆包、Kimi、腾讯元宝、通义千问、DeepSeek、扣子、ChatGPT、Claude 或 Grok，复制对应指令开始练字。支持技能的环境可获取仓库并添加；普通对话可先安排练习，再到网站制作。

```text
请从 https://github.com/bryancat/zitieku-print 安装“字帖库 AI 练字助手”Skill，使用 main 分支的最新版本。
先确认当前环境支持技能安装、联网获取文件和 Python 3 脚本运行；按本平台的技能安装机制获取完整文件，保留 SKILL.md、scripts、references 和 agents，不要只读取说明就声称安装成功，也不要覆盖已有同名技能。
安装后确认技能可被宿主发现和启用，运行 scripts/create_link.py --list-templates，再用 basic-strokes 方案验证能生成 configuration_ready 和完整字帖链接。
如果环境不支持安装或脚本执行，请给出练习文字、格型与练法建议，并提供 https://zitieku.com/zitie-shengchengqi.html 供我手动制作，不编造已预填的链接。验证成功后，开始帮我安排这次练字，只问还缺少的必要信息。
```

安装后可以说：“孩子刚开始学写名字，叫林小禾”，或“把春夏秋冬做成带拼音的田字格”。

## 各平台使用方法

- [WorkBuddy 练字教程](https://zitieku.com/ai-zitie/start/#platform-workbuddy)：在对话中添加，接着就能练字。
- [豆包 练字教程](https://zitieku.com/ai-zitie/start/#platform-doubao)：聊聊孩子的情况，让豆包帮你选内容和练法。
- [Kimi 练字教程](https://zitieku.com/ai-zitie/start/#platform-kimi)：在 Kimi 对话中安排练习，用 Kimi Work 获取技能。
- [腾讯元宝 练字教程](https://zitieku.com/ai-zitie/start/#platform-yuanbao)：从名字、生字或练字困惑出发，整理一份练习方案。
- [通义千问 练字教程](https://zitieku.com/ai-zitie/start/#platform-qwen)：用千问规划练习，也可在千问办公中添加技能。
- [DeepSeek 练字教程](https://zitieku.com/ai-zitie/start/#platform-deepseek)：把练字目标说清楚，得到具体的练习内容与建议。
- [扣子 练字教程](https://zitieku.com/ai-zitie/start/#platform-coze)：在扣子编程中准备技能，再进入对话使用。
- [ChatGPT 练字教程](https://zitieku.com/ai-zitie/start/#platform-chatgpt)：在已开通 Skills 的工作区中，通过对话添加练字技能。
- [Claude 练字教程](https://zitieku.com/ai-zitie/start/#platform-claude)：用 Claude Code 获取技能，或在 Claude 的 Skills 中添加。
- [Grok 练字教程](https://zitieku.com/ai-zitie/start/#platform-grok)：在 Grok Build 中添加技能，用对话准备练习。

## 适用环境

需要宿主支持 Agent Skills、联网获取仓库、文件操作和 Python 3 执行。生成链接只使用 Python 标准库，不需要字帖库 API Key。

仓库地址让具备相应能力的 AI 自行获取文件，不能让普通聊天窗口自动获得技能安装能力。各平台的安装入口、权限与账号要求以实际客户端为准；使用方式见平台指南：ChatGPT 使用已开通 Skills 的工作区；Claude 区分 Claude Code 与网页 Skills；Grok 使用 Grok Build。Kimi Work、千问办公和扣子编程按各自技能机制添加。

## 安装验证

将仓库内容放入宿主规定的技能目录，并保持根目录 SKILL.md 及配套目录结构。按宿主机制启用；不要猜测安装目录。

从技能目录执行：

```sh
python3 scripts/create_link.py --list-templates
python3 scripts/create_link.py --describe-template name-blank
python3 scripts/create_link.py --input request.json
```

request.json 的非个人信息测试内容：

```json
{"template_id":"basic-strokes"}
```

应列出 13 种模板；`--describe-template` 应返回支持字段、默认设置和示例；测试输出应包含 configuration_ready 和完整网站链接。还需确认宿主已发现、启用技能；运行脚本成功不等于宿主安装完成。

配置生成成功不代表网页渲染或 PDF 已导出。请打开链接确认字形、拼音、笔顺及分页，再下载或打印。

## 文件结构

- SKILL.md：技能入口与顾问工作流程。
- scripts/create_link.py：确定性配置链接生成脚本。
- references/：能力契约、输入说明和练习建议。
- agents/：宿主展示配置。

## 官网与备用下载

只有 Agent 无法访问 GitHub，或环境仅支持手动导入时，才需要下载备用 ZIP。

- [产品介绍](https://zitieku.com/ai-zitie.html)
- [安装帮助](https://zitieku.com/ai-zitie/start/)
- [可直接上传的扁平 ZIP](https://zitieku.com/downloads/zitieku-print-0.5.1.zip)
- [问题反馈](https://github.com/bryancat/zitieku-print/issues)

GitHub 自动生成的源码 ZIP 带仓库外层目录；若平台要求 ZIP 根目录直接包含 SKILL.md，请使用官网提供的扁平 ZIP。上述 0.5.1 ZIP 是此前快照；需要本次修复请从 GitHub main 分支安装。

## 内容与隐私

本地脚本不发起网络请求。用户输入会由所用 AI 平台处理；生成链接包含可还原的练习文字，压缩不等于加密，请只分享给信任的人。不要在公开问题中提交孩子的真实姓名或个人字帖链接。

## 质量检查

当前修复覆盖链接长度校验、方案能力查询、无效字段拒绝和实际设置回执。对话验收场景见 [tests/evals/conversations.md](tests/evals/conversations.md)，需在目标 Agent 宿主执行。

## 版本维护

使用明确版本标签可固定安装内容。更新时按宿主机制操作，保留用户自行修改的版本。本仓库为独立分发版本，维护源为字帖库项目中的 integrations/zitieku/skills/zitieku-print；更新源后需同步发布，当前未配置自动同步。
