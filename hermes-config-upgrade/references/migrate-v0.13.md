# v0.13.0 迁移记录

**日期：** 2026-05-14
**从版本：** v0.12.x
**到版本：** v0.13.0 (The Tenacity Release)

## 迁移步骤

### 1. 升级版本
```bash
hermes update --yes
```
结果：升级成功，gateway 自动重启

### 2. 初始化子模块
```bash
cd ~/.hermes/hermes-agent
git submodule update --init --recursive
```
结果：tinker-atropos 子模块已初始化

### 3. 设置中文界面
```bash
hermes config set display.language zh
```

### 4. 优化压缩模型
```bash
hermes config set compression.model "google/gemini-2.5-flash"
hermes config set compression.provider "openrouter"
hermes config set auxiliary.compression.model "google/gemini-2.5-flash"
hermes config set auxiliary.compression.provider "openrouter"
```

### 5. 添加检查点配置
```bash
# max_disk_mb 和 prune_keep_last 需要手动编辑 config.yaml
# 在 checkpoints 部分添加：
#   max_disk_mb: 500
#   prune_keep_last: 10
```

### 6. 更新 SOUL.md
追加了以下章节：
- 任务持久化原则（v0.13+）
- 安全与隐私原则（v0.13+）
- Skill 与知识库管理（v0.13+）
- v0.13 新能力备忘

### 7. 更新 AGENTS.md
追加了以下章节：
- Kanban Worker 行为规范（v0.13+）
- Cron 任务规范（v0.13+）
- 文件写入规范（v0.13+）
- MCP 使用规范（v0.13+）

### 8. 调整 Cron 任务频率
```bash
hermes cron edit 100bacd3cbed --schedule "every 720m"
```
将 Self-Improving 从每 6 小时改为每 12 小时

### 9. 清理技能
```bash
rm -rf ~/.hermes/skills/gaming
```
移除了 gaming 类别（minecraft-modpack-server、pokemon-player）

### 10. 日志清理
```bash
# 备份
cd ~/.hermes/logs
tar -czf logs_backup_$(date +%Y%m%d_%H%M%S).tar.gz *.log

# 清理（保留最近 1000 行）
for log in agent.log errors.log gateway.log; do
  tail -1000 ~/.hermes/logs/$log > ~/.hermes/logs/${log}.tmp
  mv ~/.hermes/logs/${log}.tmp ~/.hermes/logs/$log
done
```

## 验证结果

### hermes doctor 检查
- ✅ Python 环境正常
- ✅ 配置文件版本最新 (v23)
- ✅ API 连通性正常
- ⚠️ Gemini API 密钥误报（实际有效）

### v0.13.0 适配检查
- ✅ display.language: zh
- ✅ security.redact_secrets: true
- ✅ checkpoints.max_disk_mb: 500
- ✅ checkpoints.prune_keep_last: 10
- ✅ compression.model: google/gemini-2.5-flash
- ✅ SOUL.md 已更新
- ✅ AGENTS.md 已更新
- ✅ 子模块已初始化

## 已知问题

1. **Gemini API 密钥误报** - doctor 使用了错误的 header 检查，实际密钥有效
2. **部分 OAuth 未登录** - Nous Portal、Google Gemini、MiniMax

## 备份位置

- 配置备份：`~/.hermes/config.yaml.bak.20260514004238`
- 日志备份：`~/.hermes/logs/logs_backup_20260514_073921.tar.gz`
