# 字帖库 AI 练字助手

让 AI 帮你选练习、安排练法，并生成可在字帖库预览、调整、下载 PDF 和 A4 打印的字帖。

支持姓名练字、汉字描红、拼音、笔顺、基础笔画、控笔线条和古诗字帖。当前版本 **0.5.1**。

## 推荐：复制指令，发给 WorkBuddy

WorkBuddy 的仓库获取、技能添加、对话生成与官网使用流程已完成真实环境验证。复制以下指令发给 WorkBuddy，按提示授权后即可开始，无需手动下载文件。

```text
请在 WorkBuddy 中帮我完成以下操作：请从 https://github.com/bryancat/zitieku-print 安装“字帖库 AI 练字助手”Skill，优先使用 v0.5.1 版本。
先确认当前环境支持技能安装、联网获取文件和 Python 3 脚本运行；按本平台的技能安装机制获取完整文件，保留 SKILL.md、scripts、references 和 agents，不要只读取说明就声称安装成功，也不要覆盖已有同名技能。
安装后确认技能可被宿主发现和启用，运行 scripts/create_link.py --list-templates，再用 basic-strokes 方案验证能生成 configuration_ready 和完整字帖链接。
如果环境不支持安装或脚本执行，请明确告诉我限制。验证成功后，开始帮我安排这次练字，只问还缺少的必要信息。
```

安装后可以说：“孩子刚开始学写名字，叫林小禾”，或“把春夏秋冬做成带拼音的田字格”。

## 适用环境

需要宿主支持 Agent Skills、联网获取仓库、文件操作和 Python 3 执行。生成链接只使用 Python 标准库，不需要字帖库 API Key。

仓库地址让具备相应能力的 AI 自行获取文件，不能让普通聊天窗口自动获得技能安装能力。各平台的安装入口、权限与账号要求以实际客户端为准；WorkBuddy 已完成真实环境验证；其他 Agent 需按其实际能力使用，不能据此推断其他平台均已通过兼容性验收。

## 安装验证

将仓库内容放入宿主规定的技能目录，并保持根目录 SKILL.md 及配套目录结构。按宿主机制启用；不要猜测安装目录。

从技能目录执行：

```sh
python3 scripts/create_link.py --list-templates
python3 scripts/create_link.py --input request.json
```

request.json 的非个人信息测试内容：

```json
{"template_id":"basic-strokes"}
```

应列出 13 种模板，测试输出应包含 configuration_ready 和完整网站链接。还需确认宿主已发现、启用技能；运行脚本成功不等于宿主安装完成。

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

GitHub 自动生成的源码 ZIP 带仓库外层目录；若平台要求 ZIP 根目录直接包含 SKILL.md，请使用官网提供的扁平 ZIP。

## 内容与隐私

本地脚本不发起网络请求。用户输入会由所用 AI 平台处理；生成链接包含可还原的练习文字，压缩不等于加密，请只分享给信任的人。不要在公开问题中提交孩子的真实姓名或个人字帖链接。

## 版本维护

使用明确版本标签可固定安装内容。更新时按宿主机制操作，保留用户自行修改的版本。本仓库为独立分发版本，维护源为字帖库项目中的 integrations/zitieku/skills/zitieku-print；更新源后需同步发布，当前未配置自动同步。
