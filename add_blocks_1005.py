"""添加2个新积木到blocks.json: task-prompt-optimize 和 task-meeting-summary"""
import json
import shutil
from datetime import datetime

blocks_path = r'D:\jieyuexingchen\promptblocks\blocks.json'

# 备份
shutil.copy2(blocks_path, blocks_path + '.bak')

with open(blocks_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# 找到task分类
for cat in data['categories']:
    if cat['id'] == 'task':
        # 检查是否已存在
        existing_ids = [b['id'] for b in cat['blocks']]
        print(f"Existing task blocks: {existing_ids}")
        
        # 新积木1: Prompt优化师
        if 'task-prompt-optimize' not in existing_ids:
            new_block_1 = {
                "id": "task-prompt-optimize",
                "title": "Prompt优化",
                "content": "请对以下Prompt进行专业优化。从六个维度逐一改进：1.角色定义是否清晰明确 2.任务描述是否具体可执行 3.上下文信息是否充分 4.约束条件是否完整（字数/格式/语气/禁忌） 5.输出格式是否明确  6.是否有示例引导。先指出原Prompt的问题，再给出优化后的完整版本，最后用对比表格说明改进点。",
                "tags": ["Prompt优化", "Prompt工程", "改进"],
                "platforms": ["all"],
                "verified": "2026-10-05",
                "model": "GPT-4o+/Claude3.5/Step3+",
                "titleEn": "Prompt Optimization",
                "contentEn": "Please professionally optimize the following Prompt. Improve it across six dimensions: 1) Is the role definition clear and specific 2) Is the task description concrete and actionable 3) Is the context information sufficient 4) Are the constraints complete (word count/format/tone/taboo) 5) Is the output format explicit 6) Are there example guides. First identify the issues in the original Prompt, then provide the optimized full version, and finally use a comparison table to explain the improvements."
            }
            cat['blocks'].append(new_block_1)
            print("Added: task-prompt-optimize")
        
        # 新积木2: 会议纪要
        if 'task-meeting-summary' not in existing_ids:
            new_block_2 = {
                "id": "task-meeting-summary",
                "title": "会议纪要",
                "content": "请根据以下会议记录/录音转写，整理一份结构化会议纪要。包含五个部分：1.会议信息（时间/参会人/议题） 2.讨论要点（按议题分组，提炼各方观点） 3.决议事项（明确通过的决定） 4.待办事项（负责人/截止时间/交付物，用表格呈现） 5.遗留问题（未决议题及后续计划）。语言精炼，重点突出，避免流水账。",
                "tags": ["会议纪要", "职场", "文档"],
                "platforms": ["all"],
                "verified": "2026-10-05",
                "model": "GPT-4o+/Claude3.5/Step3+",
                "titleEn": "Meeting Minutes",
                "contentEn": "Please organize the following meeting notes/transcript into a structured meeting summary. Include five sections: 1) Meeting info (time/attendees/agenda) 2) Discussion points (grouped by topic, summarizing viewpoints) 3) Decisions made (clearly state passed resolutions) 4) Action items (owner/deadline/deliverable, presented as a table) 5) Open issues (unresolved topics and follow-up plans). Keep the language concise and focused, avoiding a running account style."
            }
            cat['blocks'].append(new_block_2)
            print("Added: task-meeting-summary")
        
        break

# 写回
with open(blocks_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

# 验证
with open(blocks_path, 'r', encoding='utf-8') as f:
    verify = json.load(f)
    for cat in verify['categories']:
        if cat['id'] == 'task':
            print(f"\nTask blocks now ({len(cat['blocks'])}):")
            for b in cat['blocks']:
                print(f"  - {b['id']}: {b['title']}")

total = sum(len(c['blocks']) for c in verify['categories'])
print(f"\nTotal blocks: {total}")
