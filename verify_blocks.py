"""
PromptBlocks 回归测试 - 验证新积木
检查所有积木的结构完整性、字段完整性、ID唯一性、中英双语
"""
import json
import sys

BLOCKS_PATH = r'D:\jieyuexingchen\promptblocks\blocks.json'

with open(BLOCKS_PATH, 'r', encoding='utf-8') as f:
    data = json.load(f)

errors = []
warnings = []
all_ids = set()
total = 0

REQUIRED_FIELDS = ['id', 'title', 'content', 'tags', 'platforms', 'verified', 'model', 'titleEn', 'contentEn', 'agentRole', 'inputs', 'prerequisites', 'outputFormat', 'qualityChecks', 'recommendedWith']

for cat in data.get('categories', []):
    for b in cat.get('blocks', []):
        total += 1
        bid = b.get('id', 'NO_ID')
        
        # ID唯一性
        if bid in all_ids:
            errors.append(f"重复ID: {bid}")
        all_ids.add(bid)
        
        # 必需字段检查
        for field in REQUIRED_FIELDS:
            if field not in b:
                errors.append(f"{bid}: 缺少字段 {field}")
            elif not b[field] and field != 'content' and field not in ['tags', 'platforms']:
                warnings.append(f"{bid}: 字段 {field} 为空")
        
        # content不能为空（ex-none除外）
        if bid != 'ex-none' and not b.get('content', '').strip():
            errors.append(f"{bid}: content为空")
        
        # 中英双语检查
        if not b.get('titleEn'):
            warnings.append(f"{bid}: 缺少titleEn")
        if not b.get('contentEn'):
            warnings.append(f"{bid}: 缺少contentEn")
        
        # agentRole检查
        valid_roles = ['general', 'pm', 'developer', 'tester', 'designer', 'marketer', 'researcher']
        role = b.get('agentRole', 'general')
        if role not in valid_roles:
            errors.append(f"{bid}: agentRole={role} 不在有效列表中")
        
        # platforms检查
        valid_platforms = ['all', 'chatgpt', 'claude', 'stepfun', 'gemini', 'wenxin', 'tongyi']
        for p in b.get('platforms', []):
            if p not in valid_platforms:
                errors.append(f"{bid}: platform={p} 不在有效列表中")

# 新增积木专项检查
for new_id in ['task-skill-export', 'task-competitor-monitor']:
    if new_id not in all_ids:
        errors.append(f"新积木 {new_id} 未找到!")
    else:
        print(f"✅ {new_id} 验证通过")

print(f"\n=== 回归测试结果 ===")
print(f"积木总数: {total}")
print(f"错误: {len(errors)}")
print(f"警告: {len(warnings)}")

if errors:
    print("\n--- 错误 ---")
    for e in errors:
        print(f"❌ {e}")
else:
    print("\n✅ 所有积木结构验证通过！")

if warnings:
    print(f"\n--- 警告({len(warnings)}) ---")
    for w in warnings[:10]:
        print(f"⚠️ {w}")
    if len(warnings) > 10:
        print(f"  ...还有{len(warnings)-10}条警告")

# 冲突对检查
conflicts = data.get('conflictPairs', [])
print(f"\n冲突对数: {len(conflicts)}")
for cp in conflicts:
    if cp['a'] not in all_ids or cp['b'] not in all_ids:
        print(f"⚠️ 冲突对引用了不存在的积木: {cp['a']} vs {cp['b']}")

# 分类统计
print("\n=== 分类统计 ===")
for c in data.get('categories', []):
    n = len(c.get('blocks', []))
    print(f"  {c['id']:12s} {c['name']:8s} {n:3d}")

# 角色统计
role_count = {}
for c in data.get('categories', []):
    for b in c.get('blocks', []):
        r = b.get('agentRole', 'general')
        role_count[r] = role_count.get(r, 0) + 1
print("\n=== 角色统计 ===")
for r in sorted(role_count.keys()):
    print(f"  {r:12s} {role_count[r]:3d}")

sys.exit(1 if errors else 0)
