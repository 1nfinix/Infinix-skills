---
name: wiki-ingest
description: 知识库标准摄入流程（Karpathy LLM Wiki 模式）：链接→结构化摘要→更新索引→追加日志。通用框架，需配置 wiki 结构和板块映射。
category: productivity
---

# Wiki Ingest

基于 [Karpathy LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) 模式的通用摄入流程。

## 使用前配置

用户需先告知 LLM 以下信息（或写入项目 AGENTS.md）：

```
WIKI_ROOT = 知识库根目录（如 ~/vault-sync/）
INDEX_FILE = 全局索引文件（如 index.md）
LOG_FILE = 时序日志文件（如 log.md）
SCHEMA_FILE = 维护规范文件（如 SCHEMA.md）

板块映射（内容类型 → 子目录）：
  - 研究笔记 → research/
  - 文章存档 → articles/
  - ...（按需定义）
```

LLM 应在首次执行前主动确认以上配置。未配置时默认将内容存入 `WIKI_ROOT/inbox/`，待用户分类。

## 触发条件

- 用户分享链接 + "存档"/"保存"/"记录"
- 用户说"研究下这篇文章"
- 任何需要存入知识库的外部素材

## 流程（5 步）

### Step 1: 提取内容

```
web_extract(url)  → 获取 markdown
浏览器不支持时用 terminal: curl + 转文本
```

### Step 2: 阅读 & 结构化

读完后写成结构化摘要页，**不是原文搬运**：

```markdown
# 标题

> 来源：作者 · 平台 · 日期
> 链接：url
> 存档日期：today

## 一句话
(用一句话提炼核心观点)

## 关键要点
- 要点 1
- 要点 2

## 数据/证据
(如有具体数字、案例)

## 与现有知识的关联
- [[相关页面1]]
- [[相关页面2]]
```

文件名：`YYYY-MM-DD_作者_主题关键词.md`

### Step 3: 写入对应板块

根据配置的板块映射，归入对应子目录。无匹配时存入 `inbox/`。

### Step 4: 更新索引

在 `WIKI_ROOT/INDEX_FILE` 对应分类下追加条目：

```
| [文件名](相对路径) | 一句话摘要 |
```

### Step 5: 追加日志

在 `WIKI_ROOT/LOG_FILE` 最前面追加：

```
## [日期] ingest | 标题简述
- 来源：url → 板块/文件名
- 交叉引用：page1, page2
```

## 交叉引用

写入时检查新内容是否涉及已有实体（人物/概念/项目），自动补 `[[wiki链接]]`。

## 注意事项

- 不搬运原文逐字翻译，写**结构化摘要**
- 文件名不含空格，用 `_` 连接
- 原始素材不修改（raw sources 只读）
- 公开发布前做隐私审查
