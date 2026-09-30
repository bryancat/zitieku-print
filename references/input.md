# 输入与能力说明

Skill 使用规范字帖文档与 v3 链接协议。`contract-v2.json` 由 `js/worksheet/presets.js` 和 `js/worksheet/schema.js` 生成；网站配置变化后必须重新生成契约，并运行网页、API 与 Skill 契约测试。

## 查询方案能力

运行 `python3 scripts/create_link.py --describe-template name-blank`，返回 `required_fields`、`fields`（允许值）、`defaults` 和可直接执行的 `example`。只使用该方案支持的字段；姓名自写等方案不支持描红浓度，不要根据其他方案推测。

## 输入字段

| 字段 | 要求 |
|---|---|
| `template_id` | 必填；来自 `--list-templates` 返回的 13 个方案编号 |
| `text` | 汉字、笔顺、古诗方案必填；非空字符串，保留原文 |
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
| `source` | 可选来源标识：`advisor`、`skill`、`kimi`、`coze`、`share`、`developer`、`mcp`；默认 `skill` |

未声明或不适用于当前方案的字段会报错，不会静默忽略。不要发送字体、课本版本、固定行数、指定页数或自定义跟踪参数。不要主动索要班级和学号。

## 示例

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

脚本返回状态、网址、方案编号、方案名称、实际设置、内容长度、是否已验证渲染和警告。覆盖设置后，以返回的 `settings` 为准，不根据方案名称猜测实际格型、列数或方向。`settings` 同时返回 `pinyin`、`trace_style`、`trace_density` 和实际 `practice_stages`；梯度以阶段角色和数量为准。参数错误返回 `field`、`allowed_values` 和 `hint`；允许值为空数组表示该方案不支持这个字段。

单次输入最多读取 100000 个字符；完整状态序列化不能超过 20000 个 UTF-16 单元；编码令牌最长 3000 个字符。这些是协议上限，不是单页容量承诺。新版生成器会按 A4 容量自动分页，但脚本不运行排版和浏览器渲染，因此始终要求在网站预览后再导出。

多音字、生僻字、缺字、缺拼音或缺笔顺数据需要在网站核对。名称渐淡不是成绩评价，输入诗词和课堂材料的准确性由调用方确认。

生成链接本身不访问服务器；打开网站时仍会加载页面依赖和网站统计。链接内容可被持有者恢复，不代表端到端加密。本包不把姓名或正文写入来源参数，也不宣称已经实现完整渠道归因。

当前生成器只在页面初始化时读取链接载荷。连续生成多份字帖时，每个网址都应在新标签页打开；不要只在同一页面替换 `#reprint` 片段。
