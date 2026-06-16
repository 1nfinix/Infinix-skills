---
name: vault-sync-ingest
description: Vault-Sync Wiki 标准摄入流程：读取→理解→结构化写入→更新index→追加log。触发：分享链接/文章 + 存档意图
category: productivity
---

# Vault-Sync Ingest

Karpathy LLM Wiki 模式的标准摄入流程。

## 触发条件

- 用户分享链接 + "存档"/"保存"/"记录"
- 用户说"研究下这篇文章"
- 老多/李一恩/甜南瓜等博主的文章链接
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

| 内容类型 | 板块 |
|---------|------|
| AI Agent / 工程 / 系统设计 | `ai-agent-loops/` |
| 老多文章 | `bloggers/老多/` |
| 李一恩直播/分析 | `li-yien/` |
| 甜南瓜内容 | `bloggers/甜南瓜/` |
| 投资/金融/标的分析 | `chengsuan-drafts/` |
| 公众号长文 | `chengsuan-drafts/` |
| GPT 图片提示词 | `gpt-image-prompts/` |
| 纯参考/转载 | `chengsuan-drafts/reference/` |

### Step 4: 更新 index.md

在 `vault-sync/index.md` 对应板块追加一条：

```
| [文件名](相对路径) | 一句话摘要 |
```

### Step 5: 追加 log.md

在 `vault-sync/log.md` 最前面追加：

```
## [日期] ingest | 标题简述
- 来源：url → 板块/文件名
- 交叉引用：page1, page2
```

## 交叉引用

写入时检查：
- 是否提到已有标的（新易盛/SIVE/中际旭创 等）→ 链接到相关日报
- 是否提到已有概念（CPO/Loop Engineering/Agentic Engineering）→ 链接到已有笔记
- 是否与 self-improving 中的规则冲突 → 标记待验证

## 注意事项

- 不搬运原文逐字翻译，写**结构化摘要**
- 文件名不含空格，用 `_` 连接
- 发布到公众号前做隐私审查（见 writing domain）
- 原始素材不修改（raw sources 只读）
