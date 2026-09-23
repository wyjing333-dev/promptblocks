# PromptBlocks 每日维护清单

## 每日6件事（约35分钟）

### 1. 查网站是否活着（2分钟）
- 打开 https://wyjing333-dev.github.io/promptblocks/
- 点几个积木，确认功能正常
- GitHub Pages偶尔构建失败，进仓库Settings → Pages看状态

### 2. 看GitHub仓库动态（5分钟）
- 访问 https://github.com/wyjing333-dev/promptblocks
- 看有没有Issue、Pull Request、Star变化
- 有人提Issue就回复，有人PR就Review

### 3. 查流量数据（5分钟）
- GitHub仓库 → Insights → Traffic：看访客数、克隆数
- 记录到维护日志，追踪增长趋势

### 4. 更新一个积木或预设（10分钟）
- 每天至少新增1个积木模块或1个预设模板
- 积木库从40个→100个→200个持续扩充
- 改完git push，GitHub Pages自动更新

### 5. 推广一条内容（8分钟）
- 小红书/抖音/即刻/推特，挑一个平台发一条
- 内容方向：产品更新、使用技巧、Prompt对比效果、新积木预告

### 6. 定时检查GitHub Issue并由AMOO回复（5分钟）
- 运行脚本：`$env:GH_TOKEN='token'; cd D:\jieyuexingchen\promptblocks; C:\Users\admin\AppData\Local\Programs\Python\Python311\python.exe scripts\check_github_issues.py`
- 脚本自动拉取未关闭Issue列表和详情
- AMOO用humanizer-zh技能写真人风格回复
- 用 `gh issue comment <编号> --body "回复内容" --repo wyjing333-dev/promptblocks` 提交回复
- 回复后用 `gh issue close <编号> --repo wyjing333-dev/promptblocks` 关闭已解决的Issue
- 无Issue时输出"[OK] 当前没有未关闭的Issue，一切正常！"

---

## 每周1件事（约1小时）

### 用SEO审计技能跑一遍
- 用已装的SEO审计技能（运营官Agent）扫描网站
- 检查meta标签、SEO关键词、页面结构
- 根据报告优化README和产品文案

---

## 每月1件事（约2小时）

### 用测试Agent全面回归测试
- 用webapp-testing技能（测试员Agent）跑完整测试
- 确认新加的积木没有破坏已有功能
- 更新TEST_REPORT.md

---

## 维护日志模板
在 promptblocks/ 目录下建 MAINTENANCE.md，每天追加一行：

```
## 2026-09-23
- 网站：正常
- GitHub：+2 stars, 0 issues
- 流量：14 visitors, 3 clones
- 更新：新增"role-data-analyst"积木
- 推广：小红书发了"30秒拼出专业Prompt"笔记
- Issue检查：N条新Issue，已回复/无新Issue
```

---

## 自动化建议（未来升级）
1. GitHub Actions定时检测网站可访问性，挂了自动发通知
2. 接入Google Analytics或Umami看更细的流量数据
3. 用GitHub Trending技能（调研员Agent）监控竞品动态
4. 积木库数据抽成JSON文件，方便批量管理
