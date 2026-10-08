# -*- coding: utf-8 -*-
import json

filepath = 'D:/jieyuexingchen/promptblocks/blocks.json'

with open(filepath, 'r', encoding='utf-8') as f:
    data = json.load(f)

# 新积木1: con-token-compress (约束类, 来自caveman 109k stars)
con_token_compress = {
    "id": "con-token-compress",
    "title": "Token压缩输出",
    "content": "输出时压缩Token用量，遵循以下原则：1）省略客套话和过渡句，直接给结果；2）用符号替代连接词（用→替代\"因此\"，用•替代\"首先\"\"其次\"）；3）合并同类项，不重复展开已有信息；4）代码只给关键行，省略样板代码和注释；5）列表用分号分隔而非换行，除非超过3项；6）删除可推断的上下文（对方已知的不重述）。目标：在保持信息完整的前提下，将输出Token减少50-65%。",
    "tags": ["Token优化", "成本", "效率", "压缩"],
    "platforms": ["chatgpt", "claude", "stepfun"],
    "verified": "2026-10-06",
    "model": "GPT-4o+/Claude3.5/Step3+",
    "titleEn": "Token Compression",
    "contentEn": "Compress token usage in output following these principles: 1) Skip pleasantries and transitions, deliver results directly; 2) Replace connectors with symbols (use -> for therefore, * for first/second); 3) Merge similar items, do not repeat existing information; 4) Code: only key lines, omit boilerplate and comments; 5) Lists: semicolon-separated unless over 3 items; 6) Remove inferable context (do not restate what the other party already knows). Goal: reduce output tokens by 50-65% while preserving information completeness."
}

# 新积木2: task-arch-diagram (任务类, 来自Archify 36k stars)
task_arch_diagram = {
    "id": "task-arch-diagram",
    "title": "架构图生成",
    "content": "请根据以下代码仓库/系统描述/技术方案，生成一份架构图说明。包含五个维度：1）架构图（组件分层、依赖关系、数据流向，用文字描述布局）；2）工作流图（核心业务流程、调用链路、异步/同步标注）；3）序列图（关键交互的前后顺序、请求/响应路径）；4）数据流图（输入输出、存储节点、缓存层）；5）生命周期图（实例创建→运行→销毁的关键状态转换）。每个维度用Mermaid语法或ASCII图描述，附2-3句关键说明。最后标注设计决策的理由和潜在风险点。",
    "tags": ["架构图", "技术文档", "可视化", "Mermaid"],
    "platforms": ["chatgpt", "claude", "stepfun"],
    "verified": "2026-10-06",
    "model": "GPT-4o+/Claude3.5/Step3+",
    "titleEn": "Architecture Diagram",
    "contentEn": "Based on the following codebase/system description/technical proposal, generate an architecture diagram documentation. Include five dimensions: 1) Architecture diagram (component layers, dependencies, data flow, described in text layout); 2) Workflow diagram (core business processes, call chains, async/sync annotations); 3) Sequence diagram (interaction order, request/response paths); 4) Data flow diagram (inputs/outputs, storage nodes, cache layers); 5) Lifecycle diagram (instance creation to running to destruction, key state transitions). Use Mermaid syntax or ASCII art for each dimension with 2-3 key explanatory sentences. Finally, note design decision rationale and potential risk points."
}

# 找到约束分类和任务分类, 添加新积木
for cat in data['categories']:
    if cat['id'] == 'constraints':
        existing_ids = [b['id'] for b in cat['blocks']]
        if 'con-token-compress' not in existing_ids:
            cat['blocks'].append(con_token_compress)
            print(f"Added con-token-compress to constraints. Now {len(cat['blocks'])} blocks.")
        else:
            print("con-token-compress already exists in constraints.")
    elif cat['id'] == 'task':
        existing_ids = [b['id'] for b in cat['blocks']]
        if 'task-arch-diagram' not in existing_ids:
            cat['blocks'].append(task_arch_diagram)
            print(f"Added task-arch-diagram to task. Now {len(cat['blocks'])} blocks.")
        else:
            print("task-arch-diagram already exists in task.")

# 统计
total = sum(len(c['blocks']) for c in data['categories'])
print(f"Total blocks: {total}")
for c in data['categories']:
    print(f"  {c['id']}: {len(c['blocks'])}")

# 写回文件
with open(filepath, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("blocks.json updated successfully!")
