---
name: neat-freak
description: >
  会话结束后对项目文档和记忆进行洁癖级审查与同步，包含环境自检与自适应优化。
  MUST trigger when the user says:
  "同步一下", "整理文档", "整理一下", "更新记忆", "梳理一下", "收尾",
  "这个阶段做完了", or any phrase suggesting cleanup.
  Bare "整理" / "tidy" with prior dev context counts.
---

# 洁癖 v3 — 环境感知 + 自适应优化

> **原作出处**：[KKKKhazix/khazix-skills — neat-freak](https://github.com/KKKKhazix/khazix-skills/tree/main/neat-freak)
> 本项目在 KKKKhazix 原始洁癖技能的基础上增强：新增第零步「环境自检 + 自适应优化」、整合 Hermes 配置审计联动、自适应环境发现。原始五步法框架和跨平台设计理念继承自原版，在此致谢。

你是一个**知识库编辑 + 系统运维**，不是记录员。审查全局、感知环境、自适应优化、合并重复、修正过期、删除废弃。

---

## 第零步：环境自检 + 自适应优化

**先感知环境，再动文档。** 环境变了，文档和配置要跟着变。

### 0.1 系统基础信息

```bash
uname -s                    # Linux / Darwin → 决定路径风格
df -h / | tail -1           # 使用率 > 80% 触发清理
free -h | grep Mem          # available < 500MB 触发降配
```

### 0.2 运行时环境

```bash
python3 --version
which uv && uv --version
which node && node --version
which hermes && hermes --version
```

### 0.3 服务健康

```bash
# 根据 config.yaml 中实际配置的 TTS provider 检查对应服务
# 例如：voxcpm → curl localhost:<port>/health
#       edge/openai → 检查对应 API 连通性
hermes config get tts.provider
# 根据返回结果检查对应服务

# API 连通性抽查（只测 config.yaml 中实际配置的 provider）
hermes config get model.provider
# 根据返回的 provider 名检查对应 API 端点
```

### 0.4 环境 → 自适应优化

**根据 0.1-0.3 的结果，自动执行以下调整：**

| 检测到的环境特征 | 自适应操作 |
|-----------------|-----------|
| 磁盘 > 80% | 降低 checkpoints 上限；清理 audio_cache、image_cache |
| 内存 < 500MB | 清理 heavy 后台进程；建议降配并发 |
| Python 版本变化 | 更新 memory 中记录的版本号；检查 venv 路径 |
| 关键 CLI 缺失 | 在 memory 中记录；若 skill 引用该工具 → 加注「需安装 xxx」 |
| TTS 服务 DOWN | 尝试重启对应服务；失败则记录到 memory |
| API 连通性 FAIL | 检查 .env 中的 API Key；若 provider 为 fallback 链成员 → 标记降级风险 |
| Hermes 版本升级 | 触发 config-upgrade 子流程（检查新配置项、废弃项） |
| `providers: {}` 为空但 fallback 引用了 provider | 补全 provider 定义 |

### 0.5 环境感知结果写入 memory

将关键环境特征以简洁条目写入 memory，例如：
```
服务器环境：Linux (kernel-version)，Python 3.x，已安装工具列表
```

---

## 第一步：盘点

对你影响范围内的所有东西做 ls：

1. **Hermes skills**：`find ~/.hermes/skills -maxdepth 2 -name "SKILL.md" | wc -l` — 数量合理吗？有空的吗？
2. **Cron jobs**：`cronjob action='list'` — 每个 job 的 skill 真实存在吗？last_run_at 有 null 吗？
3. **临时文件**：`ls /tmp/*.md /tmp/*.html /tmp/*.png 2>/dev/null` — 本会话遗留？
4. **知识库目录**：扫描用户常用的知识库路径（如 vault-sync/、wiki/、notes/）— 有没有该归档的？
5. **记忆**：扫一遍系统提示里的 MEMORY + USER PROFILE。哪些过期/重复/可删除？相对时间词转绝对日期了吗？
6. **对话**：回顾本次会话产出
7. **config.yaml**：检查是否有 `${ENV_VAR}` 未展开、空 `api_key: ''`、已下架模型引用

输出内部清单（不需要给用户看），每个项目标「评估过 / 要改 / 不用改」。

---

## 第二步：识别变更

不要只看新增了什么，要看变动波及了什么：

| 变动类型 | 影响面 |
|----------|--------|
| 新建/删除 skill | skills 目录 + cron prompt 引用 |
| 新建/删除 cron job | cron job 列表 + skill 声明 |
| 修改配置 | config.yaml + 记忆 |
| 环境变化（OS/工具/版本） | 路径、命令、skill 引用 → 全链路 |
| 归档/清理文件 | temp + 知识库 + cron output |
| 记忆过时/重复 | memory add 覆盖 |
| 项目废弃 | cron + skill + temp + 记忆引用 → 全清 |

**关键**：跨项目？如果改了 A 且 B 依赖它，B 也要改。
**环境变化**：工具版本或路径变了 → 所有引用该工具的 skill 都要检查。

---

## 第三步：动手改

必须真的用工具修改/创建/删除。不要描述打算怎么做。

**顺序**：清理（风险最低）→ 配置（环境适配）→ 记忆（最常用）→ skill/cron（影响后续执行）

**记忆编辑原则**：
- **合并优于追加**：改旧条目，不新增
- **删除优于保留**：完成的计划、推翻的决策、过期的上下文，删
- **绝对时间**：永远写 `2026-06-05`，不写"今天""最近"
- **简洁**：一条记一件事，不塞三件

**⚠️ memory remove/replace 经常失败**（工具内部格式与显示格式不一致）。
对策：优先 `memory add` 追加修正版，靠新条目自然覆盖旧条目。
如果 `remove` 连续失败 ≥3 次，放弃改用 add，在摘要里注明残留旧条目。

**⚠️ config.yaml 是受保护文件**，`patch` 和 `write_file` 无法直接修改。
对策：键值修改用 `hermes config set <key> <value>`；复杂/批量修改用 `terminal` + `python3` 脚本。

---

## 第四步：自检

- [ ] 每个列出的文件都判断了「不用改」或「已改」
- [ ] 环境自检结果已写入 memory
- [ ] 记忆之间没有矛盾，没有相对时间词（"今天""最近""上周"）
- [ ] skill 内容跟实际代码/脚本/环境一致
- [ ] cron job 引用的是真实存在的 skill 名
- [ ] config.yaml 无空 api_key、无已下架模型、provider 引用有效
- [ ] 废弃项目的 cron/skill/temp/记忆全部清干净了
- [ ] 跨项目影响？下游也同步了
- [ ] 关键环境变化（Python版本、路径、工具）已通知用户

哪条打不了勾，回去补。

---

## 第五步：变更摘要

改完后给用户简洁输出：

```
## 🧹 同步完成

### 🌐 环境
- OS / 磁盘 / 内存概况
- 服务状态（TTS / API 连通性）
- 发现的问题 + 处理结果

### 🧠 记忆变更
- 更新：xxx（原因）
- 新增：xxx
- 删除：xxx（原因）

### 📄 文档/配置变更
- config.yaml — xxx
- skill/xxx — xxx
- 其他文件 — xxx

### ⚠️ 未处理
- xxx（为什么没处理）
```

只列有实际变更的项目。没改的不列。

---

## 参考

- 变更影响矩阵 → `references/sync-matrix.md`
- 各平台路径速查 → `references/agent-paths.md`
- 项目废弃清理清单 → `references/project-cleanup-checklist.md`
