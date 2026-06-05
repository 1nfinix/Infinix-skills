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

## 安装

每个技能目录直接放入 Hermes Agent 的 skills 路径：

```bash
# 克隆仓库
git clone https://github.com/1nfinix/Infinix-skills.git

# 复制到 Hermes skills 目录
cp -r Infinix-skills/neat-freak ~/.hermes/skills/
cp -r Infinix-skills/hermes-config-upgrade ~/.hermes/skills/
```

---

## 目录结构

```
Infinix-skills/
├── neat-freak/
│   ├── SKILL.md
│   └── references/
│       ├── sync-matrix.md
│       ├── agent-paths.md
│       └── project-cleanup-checklist.md
├── hermes-config-upgrade/
│   ├── SKILL.md
│   └── references/
│       └── migrate-v0.13.md
├── LICENSE
└── README.md
```

---

## License

MIT © [1nfinix](https://github.com/1nfinix)
