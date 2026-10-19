# 输入与能力说明

Skill 使用规范字帖文档与 v3 链接协议。`contract-v2.json` 由 `js/worksheet/presets.js` 和 `js/worksheet/schema.js` 生成；网站配置变化后必须重新生成契约，并运行网页、API 与 Skill 契约测试。

## 查询方案能力

`python3 scripts/create_link.py --list-templates` 返回全部方案，每项含 `required_fields`、`fields`（允许值）和 `defaults`，通常一次调用即可确定参数。只需查一个方案或需要示例时，运行 `python3 scripts/create_link.py --describe-template name-blank`，返回 `required_fields`、`fields`（允许值）、`defaults` 和可直接执行的 `example`。只使用该方案支持的字段；姓名自写等方案不支持描红浓度，不要根据其他方案推测。

## 输入字段

| 字段 | 要求 |
|---|---|
| `template_id` | 必填；来自 `--list-templates` 返回的方案编号 |
| `text` | 汉字、笔顺、古诗方案必填；非空字符串，至少含一个汉字，保留原文；数字方案必填 0–9，可用空格或换行分隔，支持全角数字 |
| `student_name` | 姓名方案必填，最多 6 个字符；不能与 `text` 同时使用 |
| `student_class` | 姓名方案可选；仅在用户主动提供并希望显示时使用 |
| `student_id` | 姓名方案可选；仅在用户主动提供并希望显示时使用 |
| `title` | 可选字符串；是否显示及布局以网站预览为准 |
| `grid_type` | 可选：`mi` 米字格、`tian` 田字格、`square` 方格 |
| `columns` | 可选整数 4–16；仅在方案声明支持时使用，数值越大通常字格越小 |
| `orientation` | 可选：`portrait` 纵向、`landscape` 横向；姓名方案只支持纵向 |
| `pinyin` | 可选布尔值；开启或关闭声调拼音，仅在方案声明支持时使用 |
| `trace_style` | 可选：`solid` 实心灰字、`hollow` 空心双钩 |
| `trace_density` | 可选：`light` 浅、`normal` 标准、`dark` 深 |
| `practice_gradient` | 可选：`classic` 一范二描全自写、`half` 半描半写、`all-trace` 一范全描红 |
| `host` | 建议填写：Agent 所在平台名称。常用写法见 `fields.host.suggested_values`（如 `workbuddy`、`claude`、`codex`、`kimi`），新平台直接写平台名，不确定用 `other`。自动转为小写短标识（`a-z0-9-`，最长 32 位），格式不符的部分被丢弃，从不报错 |
| `source` | 可选来源标识：`advisor`、`skill`、`kimi`、`coze`、`share`、`developer`、`mcp`；默认 `skill` |

未声明或不适用于当前方案的字段会报错，不会静默忽略。不要发送字体、课本版本、固定行数、指定页数或自定义跟踪参数。不要主动索要班级和学号。

## 生字综合练习

`standard-study` 用于每字一行的生字学习表：拼音、范字、部首、笔画数、结构与累积笔顺对照，随后描红和自写。默认纵向 A4、12 列蓝色田字格，可调整拼音、格型、列数、方向、描红形态和浓度以及行内梯度。每行的范字和信息栏占两列。

需要扫码重打时，让用户在网站“重印设置”中开启二维码；不要向脚本发送 `reprint` 或 `reprint_enabled` 等未声明字段。网站的扫码链接保留综合练习类型和配置。

## 示例

```json
{"template_id":"standard-study","text":"长比巴把下个雨们问有半从"}
```

```json
{"template_id":"standard-copy","text":"春夏秋冬","grid_type":"tian","pinyin":true,"practice_gradient":"half"}
```

```json
{"template_id":"name-fade","student_name":"林小禾","trace_density":"light"}
```

```json
{"template_id":"poetry-split","title":"静夜思","text":"床前明月光，疑是地上霜。\n举头望明月，低头思故乡。"}
```

`basic-strokes` 和 `prewriting-lines` 不传文字。姓名、基础练习和普通汉字方案支持每行格数；古诗方案使用各自固定列数。姓名超过 4 个字符时，网站会采用更适合长姓名的布局。

## 返回与限制

脚本返回状态、网址、方案编号、方案名称、实际设置、内容长度、是否已验证渲染和警告。覆盖设置后，以返回的 `settings` 为准，不根据方案名称猜测实际格型、列数或方向。`settings` 同时返回 `pinyin`、`trace_style`、`trace_density` 和实际 `practice_stages`；梯度以阶段角色和数量为准。参数错误时 `errors` 列出全部问题，每项含 `error_code`、`field` 和 `allowed_values`；顶层同时保留第一项和 `hint`。允许值为空数组表示该方案不支持这个字段；未知字段的允许值是当前方案支持的字段名。退出码 2 和 `INTERNAL_ERROR` 表示脚本自身故障，不是输入问题，不要反复改参数重试。

数字综合与专项使用田字格左半格，范字、浅描与点阵使用同一数字路径。`numbers-copy` 为纯空格纸，不传 text；整页无预填数字或口诀。`numbers-single` 只接受一个数字；数字内容错误返回 `INVALID_DIGITS` 或 `SINGLE_DIGIT_ONLY`。不支持数数、填空或加减法。

非数字方案的 `text` 没有汉字时返回 `NO_CJK_CONTENT`。网站会把每个非空白字符都排成练习内容，所以含英文、数字、表情，或在非古诗方案中含标点时，`warnings` 会提示；是否删除由用户决定。

单次输入最多读取 100000 个字符；完整状态序列化不能超过 20000 个 UTF-16 单元；编码令牌最长 3000 个字符。这些是协议上限，不是单页容量承诺。新版生成器会按 A4 容量自动分页，但脚本不运行排版和浏览器渲染，因此始终要求在网站预览后再导出。

多音字、生僻字、缺字、缺拼音或缺笔顺数据需要在网站核对。名称渐淡不是成绩评价，输入诗词和课堂材料的准确性由调用方确认。

生成链接本身不访问服务器；打开网站时仍会加载页面依赖和网站统计。链接内容可被持有者恢复，不代表端到端加密。网址查询参数只含来源 `from`、Skill 版本 `v` 和可选平台 `host`，不含姓名或正文；平台由 Agent 自报，不代表经过验证的渠道归因。

生成器在链接片段变化时会重新载入，同一标签页连续打开多份字帖也能正确显示。

### 认字描写

`standard-card`：左侧圆角认字卡（拼音、范字、部首、笔画、结构），右侧默认三行田字格：先按笔顺逐格累积描写，可延续到第二行，余格整字描红，末行自写；笔画更多时增加练习行以保留完整笔顺。A4 竖版、绿色格线，默认每页约 5 字；无宣传大标题，页首留姓名和日期。`columns` 表示整行配置列数，右侧每行实际为 `columns - 2` 格。调整列数后仍优先排完笔顺，再安排描红和自写；`practice_gradient` 可切换为半描半写或全描红。

```json
{"template_id":"standard-card","text":"一二三上口"}
```

### 按组练习偏旁（dot-components）

`text` 可传练习组号、部首编号或偏旁字符，每行一组。如 `G59\nG73` 分别练两组；`氵 扌 亻` 自选为一组。每组独立排页，每个部首一行，大组自动跨页。完整目录包含 B001–B201 主部首、53 个常用位置变形（如 B077-1 三点水）和基础笔画组；G 组号为本站练习编排。左右耳旁需用明确编号区分，不能静默忽略无效内容。

推荐选组：G72 为 28 种常用笔画，G59 为 28 个常用偏旁，G73–G82 为按笔画数编排的部首练习页。内置推荐组均为 28 项，适配默认 A4 双栏；最后一页含前页复习项，同一页不重复。原 G01–G71 继续可恢复，界面展示连续页名而非内部组号。
