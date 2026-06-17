# Infinix Skills

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Hermes Agent](https://img.shields.io/badge/Hermes-Agent-6C4DF6)](https://github.com/NousResearch/hermes-agent)

Hermes Agent 实用技能集 —— 让 AI Agent 学会自我维护、环境感知和配置审计。

---

## 技能列表

| 技能 | 用途 | 触发词 |
|------|------|--------|
| `neat-freak` | 会话收尾洁癖审查 + 环境自检 + 自适应优化 | 「整理一下」「同步一下」 |
| `hermes-config-upgrade` | 配置审计、版本迁移、断裂模式自动修复 | 「检查配置」「配置审计」 |
| `personal-ai-audit` | AI外脑全景审计：10件事+协作计划+用户画像 | 「审计」「审视」「能力盘点」「我是谁」 |
| `wiki-ingest` | 知识库标准摄入：链接→摘要→索引→日志（Karpathy Wiki 模式） | 「存档」「研究下这篇」 |

---

## neat-freak — 洁癖 v2

> 📌 基于 [KKKKhazix/khazix-skills — neat-freak](https://github.com/KKKKhazix/khazix-skills/tree/main/neat-freak) 增强，感谢原作者的跨平台设计框架。

会话结束后的六步审查机制：

1. **第零步：环境自检** — 检测 OS、磁盘、内存、Python/Node 版本、CLI 工具、服务健康
2. **第一步：盘点** — 遍历 skills、cron、临时文件、记忆、config.yaml
3. **第二步：识别变更** — 环境变化、跨项目影响、废弃项目残留
4. **第三步：动手改** — 清理 → 配置 → 记忆 → skill/cron，顺序执行
5. **第四步：自检** — 10 条检查项确保无遗漏
6. **第五步：变更摘要** — 只列实际变更

**核心特色**：环境感知 + 自适应优化 —— 磁盘 > 80% 自动降阈值、内存不足自动释放 Ollama、Hermes 升级自动触发配置迁移。

---

## hermes-config-upgrade — 配置审计 v2.0

配置审计 + 版本迁移 + 断裂模式自动修复。

- **快速诊断** — 5 项检查 + 6 条自动修复（作为 neat-freak 子流程）
- **完整审计** — 7 个子模块：主模型链、Provider、辅助模型分布、delegation、TTS、存储、Web
- **断裂模式库** — 10 条已知踩坑，每条带症状 + 一键修复命令
- **版本迁移** — 通用 6 步流程，不硬编码版本号

---

## wiki-ingest — 知识库摄入 v1.0

> 📌 灵感：[Karpathy LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) 模式

标准 5 步摄入流程：

1. **提取** — web_extract 获取内容
2. **结构化** — 读→理解→写摘要（非原文搬运），含交叉引用
3. **写入 wiki** — 按内容类型归入对应板块
4. **更新 index.md** — 全局目录追加新条目
5. **追加 log.md** — 时序日志记录操作

**配套基础设施**：vault-sync/index.md（全局目录）+ log.md（时序日志）+ SCHEMA.md（维护规范）

---

## personal-ai-audit — AI外脑全景审计 v1.0

系统性地审计用户的 AI 协作环境，输出三份交付物：

1. **我能帮你做的 10 件事** — 基于实际扫描证据，每条含发现线索/价值/优先级
2. **长期协作计划** — 立即/短期/长期/周期性 + 协作边界
3. **AI 眼中的你** — 确定观察 + 合理推测 + 协作原则

**核心特色**：只读不写、平台可适配、安全边界明确（密钥只检查存在不输出值）。

---

## 安装

每个技能目录直接放入 Hermes Agent 的 skills 路径：

```bash
# 克隆仓库
git clone https://github.com/1nfinix/Infinix-skills.git

# 复制到 Hermes skills 目录
cp -r Infinix-skills/neat-freak ~/.hermes/skills/
cp -r Infinix-skills/hermes-config-upgrade ~/.hermes/skills/
cp -r Infinix-skills/wiki-ingest ~/.hermes/skills/
cp -r Infinix-skills/personal-ai-audit ~/.hermes/skills/
```

---

## 目录结构

```
Infinix-skills/
├── neat-freak/
│   ├── SKILL.md
│   └── references/
├── hermes-config-upgrade/
│   ├── SKILL.md
│   └── references/
├── personal-ai-audit/
│   └── SKILL.md
├── wiki-ingest/
│   └── SKILL.md
├── LICENSE
└── README.md
```

---

## License

MIT © [1nfinix](https://github.com/1nfinix)
