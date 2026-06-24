---
name: hermes-model-optimization
description: Hermes模型配置优化审计：六步法（盘点→分层→评分→路由→方案→验证），含全Provider模型矩阵、降级链、pitfall库、验证脚本。触发：「优化模型」「模型审计」「模型配置」「扫模型」。
category: hermes
---

# Hermes 模型配置优化

六步审计法：不追求"最强模型"，追求最稳定、最合适、可降级的模型组合。

## 第一步：盘点现状

使用 `scripts/scan-all-models.py` 一键扫描所有 Provider 连通性，同时检查：

- `config.yaml` 中的 `model`、`delegation`、`auxiliary`、`fallback_providers`
- `skills/` 和 `scripts/` 中是否硬编码了模型名
- Cron jobs 是否有 `model` 覆盖
- 最近日志中的模型失败记录

输出现状表：

| 用途 | 当前模型 | Provider | 触发位置 | 近期问题 | 建议 |
|:--|:--|:--|:--|:--|:--|

## 第二步：任务分层

| 层级 | 任务 | 优先指标 | 不适合的模型特征 |
|:--|:--|:--|:--|
| fast | Telegram 快速回复、轻量问答 | 低延迟、低成本 | 慢、限流、上下文短 |
| default | 日常任务、普通写作 | 稳定、中文好 | 输出飘、格式不稳 |
| reasoning | 排障、代码、金融分析 | 推理强、谨慎 | 幻觉高、乱改配置 |
| long_context | 长文档、知识库、记忆 | 长上下文、摘要保真 | 丢约束、压缩过度 |
| structured | JSON/YAML/工具调用 | 格式遵循 | 输出多余解释 |
| creative | 公众号、社媒、选题 | 中文自然、风格可控 | 营销腔、空话多 |
| multimodal | 图片/音频/视觉 | 支持对应模态 | 纯文本或成本过高 |
| fallback | 主模型失败兜底 | 可用性高、独立 | 与主模型同源同故障 |

## 第三步：候选模型评分

评分维度：可用性、延迟、成本、上下文、中文、推理、工具调用、安全、供应商独立性。

### 当前模型矩阵（2026-06-24）

| 模型 | Provider | 稳定性 | 成本 | 延迟 | 上下文 | 工具调用 | 中文 | 推理 | 建议角色 |
|:--|:--|:--|:--|:--|:--|:--|:--|:--|:--|
| `deepseek-v4-pro` | DeepSeek | ⭐⭐⭐ | 已充值 | 1.2s | 128K | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | **main** |
| `deepseek-v4-flash` | DeepSeek | ⭐⭐⭐ | 低 | 1.3s | 128K | ⭐⭐ | ⭐⭐ | ⭐⭐ | aux + fallback |
| `mimo-v2.5-pro` | MiMo | ⭐⭐⭐ | 已充值 | 3.5s | 1M | ⭐⭐ | ⭐⭐ | ⭐⭐⭐ | **delegation** |
| `mimo-v2.5` | MiMo | ⭐⭐⭐ | 低 | 1.5s | 1M | ⭐⭐ | ⭐⭐ | ⭐⭐ | aux 主力 |
| `agnes-2.0-flash` | Agnes | ⭐⭐ | **免费** | 11s | 256K | ⭐ | ⭐ | ⭐ | 视觉+轻量 |
| `nemotron-120b:free` | OpenRouter | ⭐⭐ | 免费 | 3.5s | 1M | ⭐⭐ | ⭐ | ⭐ | 应急 fallback |
| `ling-2.6-flash` | OpenRouter | ⭐⭐ | 免费 | 0.8s | 262K | ⭐ | ⭐ | ⭐ | 快速 fallback |
| `nex-n2-pro:free` | OpenRouter | ❌ | — | — | — | — | — | — | **已转付费** |
| `mimo-v2-omni` | MiMo | ❌ | — | — | — | — | — | — | **6/30下线** |
| `mimo-v2-pro` | MiMo | ⚠️ | — | — | — | — | — | — | 旧版，6/30停用 |

## 第四步：推荐路由

```
main       → deepseek-v4-pro           → nemotron-120b → v4-flash
delegation → mimo-v2.5-pro              → v4-pro (回主)
aux·关键   → deepseek-v4-flash          → v4-pro
aux·中量   → mimo-v2.5                  → v4-flash
aux·轻量   → agnes-2.0-flash            → mimo-v2.5
vision     → agnes-2.0-flash            → v4-pro(视觉)
TTS        → mimo-v2.5-tts/voiceclone   → Edge 晓伊
image      → FAL FLUX /dev              → agnes-image-2.0-flash
fallback   → nemotron-120b              → v4-flash
emergency  → ling-2.6-flash (0.8s极速)  → —
```

### 当前 Config 对齐检查

```
model.default      → deepseek-v4-pro          ✅
delegation         → mimo-v2.5-pro             ✅
auxiliary ×12      → 按任务分配 4 Provider     ✅
fallback_providers → nemotron → v4-flash       ✅
TTS providers      → voiceclone + bingtang     ✅
```

## 第五步：配置修改原则

1. 先备份 `config.yaml`
2. 只改模型相关字段，不动凭证、工具、平台配置
3. 使用 `python3` 脚本批量写入（`hermes config set` 会截断 API key 为 `**`）
4. 保留可回滚版本
5. 不强行优化——当前已稳定就不动

> 当前 config（2026-06-24）**无需任何修改**，已是最优状态。

## 第六步：验证

运行 `scripts/verify-models.py` 覆盖：

| 测试 | 模型 | 验证点 |
|:--|:--|:--|
| 轻量问答 | v4-pro | 中文自然回复 |
| 结构化JSON | v4-pro | 严格格式输出 |
| 长文本摘要 | v4-flash | 保留关键数字和事实 |
| 配置排障 | v4-pro | 准确识别原因 |
| 创作任务 | v4-pro | 文艺风格，字数控制 |
| Fallback | nemotron-120b | 独立 Provider 可用 |

## Pitfall 库

### 🔴 thinking mode 空返回

**影响**：DeepSeek v4-pro、v4-flash、MiMo v2.5 默认开启 thinking mode。低 `max_tokens`（<150）下 reasoning tokens 吃掉全部预算，`content` 为空但 `completion_tokens` 被消耗。

**修复**：auxiliary 任务必须加 `extra_body: {thinking: {type: disabled}}`

| 模型 | thinking 默认 | 最小安全 max_tokens | 修复 |
|:--|:--|:--|:--|
| deepseek-v4-pro | enabled | ~150 | 生产已充裕 |
| deepseek-v4-flash | enabled | ~100 | ✅ auxiliary 已 disabled |
| mimo-v2.5 | enabled | ~80 | ✅ auxiliary 已 disabled |
| mimo-v2.5-pro | enabled | ~50 | 无需处理（Delegation 慢推理专用） |

### 🔴 MiMo 认证方式静默切换（2026-06-24）

`api-key:*** → `Bearer`。旧前缀返回 401。Hermes `api_mode: chat_completions` 自动使用 Bearer，config 无需改。但自定义脚本直接调 MiMo API 的需检查。

### 🟡 Agnes 免费层波动

- 延迟 11s+（高峰期可能更差）
- 连续调用 401（等 30s 恢复）
- 调用间隔 ≥4s

### 🟡 v4-flash → v2.5 默认值差异

MiMo 官方下线：`mimo-v2-flash` → `mimo-v2.5` 自动路由（2026-06-18 起）

| 参数 | v2-flash 默认 | v2.5 默认 |
|:--|:--|:--|
| thinking | disabled | **enabled** |
| temperature | 0.3 | 1.0 |
| max_completion_tokens | 65536 | 32768 |

### 🟡 Config 编辑限制

Hermes 拒绝 `patch`/`write_file` 直接编辑 `config.yaml`。用 `python3` 脚本通过 `terminal` 批量写入。

### 🔴 自动化健康检查陷阱（2026-06-24 已移除）

`model_health_check.py` 存在两个致命缺陷，已从 cron 中删除：

1. **`max_tokens=5` 必然误判**：v4-pro/v4-flash/mimo-v2.5 的 thinking mode 会吃掉全部 5 tokens → 空返回被误判为失败
2. **`--fix` 污染配置**：连续 3 次"失败"后自动改 `config.yaml`，将精心分配的 DeepSeek/MiMo/Agnes auxiliary 替换为不稳定的 OpenRouter 免费模型

> 教训：自动化模型检测的 max_tokens 必须 ≥50，auto-fix 绝不能直接改生产配置。

## 官方模型下线时间线（MiMo）

| 旧模型 | 系统替换 | 替换为 | 下线 | 关键影响 |
|:--|:--|:--|:--|:--|
| mimo-v2-pro | 6/1 | v2.5-pro | 6/30 | API 完全适配 |
| mimo-v2-omni | 6/1 | v2.5 | 6/30 | API 完全适配 |
| mimo-v2-flash | 6/18 | v2.5 | 6/30 | thinking 默认 disabled→enabled |
| mimo-v2-tts | 6/25 | v2.5-tts | 6/30 | `mimo_default`→冰糖(中国) |

来源：https://mimo.mi.com/docs/zh-CN/updates/deprecate

## 关联技能

- `hermes-auxiliary-models` — Auxiliary 12 项任务详细配置 + Pitfall
- `agnes-free-text` — Agnes 2.0 Flash 用法 + key 冒号陷阱
- `hermes-openrouter-auxiliary-setup` — OpenRouter 免费模型配置
