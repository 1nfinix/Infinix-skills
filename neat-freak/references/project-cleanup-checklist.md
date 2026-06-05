# 项目清理 Checklist

当项目废弃/删除时，系统性清理记忆和技能的完整流程。

---

## 第一阶段：删除远程资源

```bash
# 1. 删除 Vercel 项目
vercel remove <project-name> --yes

# 2. 删除 GitHub 仓库（如有，需手动）
# github.com/<owner>/<repo>/settings → Danger Zone → Delete this repository
```

---

## 第二阶段：清理 Cron Jobs

```bash
hermes cron list   # 列出所有 job，找到引用该项目的 job_id
hermes cron remove <job_id>
```

---

## 第三阶段：清理本地记忆

| 文件 | 要改什么 |
|------|----------|
| `~/.hermes/memories/MEMORY.md` | 移除项目相关条目（数据库路径、API Key 引用等） |
| `~/.hermes/memory/user/profile.md` | 定时任务表格中移除该项目的 cron job；已移除的记录移到「已完成」区 |
| `~/.hermes/memory/user/learned/corrections.yaml` | 搜索并移除该项目的 correction 条目 |
| `~/.hermes/todo` | 清空该项目的所有 Todo |

---

## 第四阶段：清理 Skills 中的项目引用

在以下路径搜索项目名称（`projects/<name>`, `vercel.com/<name>`, GitHub repo 名）：

```
~/.hermes/skills/*/SKILL.md
~/.hermes/skills/*/references/*.md
~/.hermes/skills/*/templates/*
~/.hermes/skills/*/scripts/*
~/.hermes/skills/_proposals/
~/.hermes/scripts/_self_improve_report.txt
```

### 处理原则

- **如果 skill 中有"当前项目状态"章节**：改为"无活跃项目"或"已废弃"
- **如果 skill 中有项目路径引用**：改为 `<owner>/<repo>` 占位符（保持示例可读）
- **如果 skill 引用的是纯踩坑文档**（如 astro-static-site 的 vercel-deploy-troubleshooting）：保留但加注"已废弃项目维护"
- **references/ 中的项目专属文档**：迁移到 `planning-with-files/references/`（知识保留，但不删除）
- **`_proposals/` 中的过期提案**：直接删除

### 迁移路径参考

当 references/ 中有项目专属文档可保留时：

```
skills/<category>/references/<project>-<doc>.md
  → skills/planning-with-files/references/<project>-<doc>.md
```

---

## 第五阶段：清理本地数据产出

### vault-sync 残留

```bash
# 搜索并删除项目产出的日报/简报文件
ls ~/vault-sync/*<project-keyword>* 2>/dev/null
rm -f ~/vault-sync/*<project-keyword>*
```

### skill 文件

```bash
# 在 Hermes 会话中直接调用
skill_manage(action='delete', name='<skill-name>')
```

---\n\n## 第六阶段：验证

```bash
# 确保无残留项目引用
grep -r "projects/<name>\|vercel.com/<name>\|<owner>/<repo>" \
  ~/.hermes/memories/ \
  ~/.hermes/memory/ \
  ~/.hermes/skills/ \
  2>/dev/null | grep -v ".lock" | head -20

# 确保 cron job 已清空
hermes cron list | grep -i "<name>"
```

---

## 本次清理记录（示例）

本次清理 `ai-news-daily` 项目：

| 步骤 | 操作 |
|------|------|
| 远程 | `vercel remove ai-news-daily` ✅ |
| Cron | 删除 job `8dba70928e7a`（AI News Daily 每日数据更新） |
| 记忆 | MEMORY.md 移除过期安装记录；profile.md 更新定时任务表 |
| Skills | astro-static-site 加注废弃说明；content-aggregator 清除项目状态 |
| References | 迁移 `ai-news-daily-architecture-blueprint.md` 和 `astro-ssr-upgrade-and-vercel-deploy.md` 至 planning-with-files/references/ |
| Proposals | 删除 `ai-news-daily-项目-借鉴下.md`、`p6-rss-feed-生成-订阅功能-pending-p7-移动端适配-分类筛.md` |
