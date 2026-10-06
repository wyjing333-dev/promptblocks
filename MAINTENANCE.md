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

## 2026-09-24
- 网站：正常
- GitHub：0 stars, 0 forks, 0 issues
- 流量：0 visitors, 26 clones（15 unique，全部来自9/23）
- 更新：新增"role-data-analyst"（数据分析师）角色积木，第9个角色，总计41个积木
- 推广：X（推特）发了数据分析师新积木推广
- Issue检查：0条未关闭Issue，一切正常

## 2026-09-26
- 网站：正常（64积木/8分类/6平台/10预设，内容完整加载）
- GitHub：0 stars, 0 forks, 0 issues, 10 commits
- 流量：无法获取（gh CLI未配置GH_TOKEN）
- 更新：新增6积木+1预设（DevOps工程师/研究员/写邮件/对比分析/预算约束/大纲格式 + 商务邮件预设），58→64
- 推广：X（推特）发了64积木更新推广（内容保存在推广内容_20260926.md）
- Issue检查：0条未关闭Issue，一切正常
- 其他：桌面Hermes快捷方式已改为Web Dashboard入口

## 2026-09-27
- 网站：正常（66积木/8分类/6平台/10预设，功能完整加载无异常）
- GitHub：0 stars, 0 forks, 0 issues, 12 commits（+2 since 9/26）
- 流量：0 views / 26 clones（15 unique，全部来自9/23），之后无新访客
- 更新：新增2积木（项目经理role-pm + 改写润色task-rewrite），64→66，回归测试0错误1警告
- 推广：X（推特）发了66积木更新推广（内容保存在推广内容_20260927.md）
- Issue检查：0条未关闭Issue，一切正常

## 2026-09-28
- 网站：正常（68积木/8分类/6平台/10预设，功能完整加载无异常）
- GitHub：0 stars, 0 forks, 0 issues, 13 commits（+1 since 9/27）
- 流量：0 views / 26 clones（15 unique，全部来自9/23），9/23后仍无新访客
- 更新：新增2积木（AI工程师role-ai-engineer + 写报告task-report），66→68
- 推广：X（推特）发了68积木更新推广（内容保存在推广内容_20260928.md）
- Issue检查：0条未关闭Issue，一切正常

## 2026-09-29
- 网站：正常（70积木/8分类/6平台/13预设，功能完整加载无异常）
- GitHub：0 stars, 0 forks, 0 issues, 14 commits（+1 since 9/28）
- 流量：0 views / 26 clones（15 unique，全部来自9/23），9/23后仍无新访客
- 更新：新增2积木（写方案task-proposal + 金融分析师ind-financial-analyst），68→70，回归测试0错误1警告通过
- 推广：即刻/知乎想法发了70积木更新推广（内容保存在推广内容_20260929.md）
- Issue检查：0条未关闭Issue，一切正常

## 2026-10-04 (2)
- 网站：正常（76积木/8分类/6平台/13预设，功能完整加载无异常）
- GitHub：0 stars, 0 forks, 0 issues, 15 commits（+1 since 9/29）
- 流量：1 view / 127 clones（59 unique），9/23-10/2期间持续有克隆，9/26首次页面访问1次
- 更新：新增4积木（AI痕迹消除con-anti-ai-slop + 懒人阶梯决策dec-lazy-dev + 过度工程审计dec-over-engineer + 专业文案框架task-copywriting-framework），72→76
- 来源：对标GitHub Trending热门项目marketingskills（53k stars）和ponytail（154k stars），提取精华融入积木
- 推广：即刻发了72积木更新推广（内容保存在推广内容_20261004.md）
- Issue检查：0条未关闭Issue，一切正常
- 备注：上次维护9/29，间隔4天补维护；流量相比上次记录大幅增长（26→127 clones，15→59 unique）

## 2026-10-05
- 网站：正常（72积木/8分类/6平台/10预设，功能完整加载无异常）
- GitHub：0 stars, 0 forks, 0 issues, last updated 2026-10-04T15:46:13Z
- 流量：1 view / 127 clones（59 unique），与10/04数据一致，10月以来几乎无新流量（仅10/2有1次clone）
- 更新：新增2积木（Prompt优化task-prompt-optimize + 会议纪要task-meeting-summary），76→78
- 推广：即刻发了78积木更新推广，重点介绍新增的Prompt优化+会议纪要两个积木（内容保存在推广内容_20261005.md）
- Issue检查：0条未关闭Issue，一切正常
- 备注：流量持续低迷，需加强推广引流
- 对标分析：GitHub Trending前十AI项目（ponytail 154k/gstack 135k/agent-skills 101k等），核心发现——主流项目面向开发者CLI工具，PromptBlocks面向普通用户是差异化优势；今天新增的task-prompt-optimize积木正好对标prompt-optimizer(9.4k stars)，方向正确；建议后续增加高管角色积木+转化率优化积木+Prompt对比测试功能（详细分析见GitHub对标分析_20261005.md）

## 2026-10-06
- 网站：正常（76积木/8分类/7平台/10预设，功能完整加载无异常，MCP Server 9工具/Chrome扩展/PWA/导出图片/AI测试全功能正常）
- GitHub：0 stars, 0 forks, 0 issues, 0 watchers, last pushed 2026-10-05T00:13:26Z
- 流量：
  - 页面访问(views)：1 total / 1 unique（9/26有1次访问，之后无新页面访问）
  - 代码克隆(clones)：287 total / 123 unique
  - 10/4大爆发：139次克隆/59唯一用户（10/4大更新P0+P1+P2+MCP+Trending对标引发关注）
  - 10/5持续：21次克隆/11唯一用户
  - 10/6暂无新数据（未到统计周期）
- 更新：今日暂无新增积木（计划新增caveman Token压缩+Archify架构图生成2积木）
- GitHub Trending对标：2026-10-05日榜分析完成
  - 已对标：ponytail(154k星)+marketingskills(53k星) → 4积木已提取
  - 可借鉴5方向：impeccable前端设计审查/Agent-Reach跨平台调研/OpenMontage视频脚本/caveman Token压缩/Archify架构图生成
- 推广：待发
- Issue检查：0条未关闭Issue，一切正常
- 备注：克隆数从上次127暴增到287（+160），唯一用户从59到123（+64），10/4更新效果显著；但Stars仍为0，287次克隆0 star说明用户在用但不star，需在README和网站增加Star引导
- 更新2：新增con-token-compress+task-arch-diagram 2积木（76→80），commit fba56b4已push
- Star弹窗：已加Star引导弹窗（第3次访问自动弹+localStorage记忆+"不再提醒"按钮）
- 设计审查：设计师Agent完成6维度审查，总分5.0/10，P0问题=移动端适配缺失
- 移动端适配：已完成！汉堡菜单+全屏弹窗+44px触控+横向滚动平台栏+积木库折叠+按钮换行，commit 7881f05已push

---

## 自动化建议（未来升级）
1. GitHub Actions定时检测网站可访问性，挂了自动发通知
2. 接入Google Analytics或Umami看更细的流量数据
3. 用GitHub Trending技能（调研员Agent）监控竞品动态
4. 积木库数据抽成JSON文件，方便批量管理
