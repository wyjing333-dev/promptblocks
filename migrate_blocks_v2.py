# -*- coding: utf-8 -*-
"""
Phase 1: 积木标准化迁移脚本

为现有84个积木增加6个标准化字段：
  agentRole: 适用角色 (researcher/developer/tester/designer/marketer/pm/general)
  inputs: 输入参数描述
  prerequisites: 前置条件
  outputFormat: 输出格式 (markdown/table/json/report/list/checklist)
  qualityChecks: 质量检查项列表
  recommendedWith: 推荐搭配积木id列表

迁移策略：
  - 根据积木的category和id自动推断agentRole、outputFormat等
  - inputs/prerequisites/recommendedWith给合理默认值
  - qualityChecks根据category生成通用检查项
  - 保留所有现有字段不变
"""

import json
import re
import os
from datetime import datetime

BLOCKS_PATH = 'D:/jieyuexingchen/promptblocks/blocks.json'
BACKUP_PATH = f'D:/jieyuexingchen/promptblocks/blocks_backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'


def infer_agent_role(block_id, category, title, tags):
    """根据积木分类和内容推断适用角色"""
    bid = block_id.lower()
    tags_str = ' '.join(tags).lower() if tags else ''
    title_lower = title.lower() if title else ''

    # role类积木 - 多数是通用的
    if category == 'role':
        if any(k in bid for k in ['marketer', 'growth', 'seo']):
            return 'marketer'
        if any(k in bid for k in ['developer', 'programmer', 'coder', 'engineer']):
            return 'developer'
        if any(k in bid for k in ['designer', 'ux', 'ui']):
            return 'designer'
        if any(k in bid for k in ['pm', 'product', 'manager']):
            return 'pm'
        if any(k in bid for k in ['researcher', 'analyst', 'research']):
            return 'researcher'
        if any(k in bid for k in ['tester', 'qa', 'test']):
            return 'tester'
        return 'general'

    # task类积木
    if category == 'task':
        if any(k in bid for k in ['write', 'article', 'content', 'copy', 'social']):
            return 'marketer'
        if any(k in bid for k in ['code', 'debug', 'refactor', 'review']):
            return 'developer'
        if any(k in bid for k in ['test', 'verify', 'validate']):
            return 'tester'
        if any(k in bid for k in ['design', 'layout', 'review-ui']):
            return 'designer'
        if any(k in bid for k in ['research', 'analyze', 'compare']):
            return 'researcher'
        if any(k in bid for k in ['plan', 'priority', 'roadmap', 'prd']):
            return 'pm'
        if any(k in bid for k in ['requirements', 'clarify', 'acceptance']):
            return 'pm'
        return 'general'

    # industry类积木
    if category == 'industry':
        if any(k in bid for k in ['lawyer', 'legal', 'contract']):
            return 'general'
        if any(k in bid for k in ['finance', 'accountant']):
            return 'general'
        return 'general'

    # decision类积木 - 多数跟PM/开发相关
    if category == 'decision':
        if any(k in bid for k in ['route', 'tool', 'select']):
            return 'general'
        if any(k in bid for k in ['priority', 'risk', 'tradeoff']):
            return 'pm'
        return 'general'

    # 其他类积木默认通用
    return 'general'


def infer_output_format(block_id, category, content):
    """根据积木类型推断输出格式"""
    bid = block_id.lower()
    content_lower = content.lower() if content else ''

    if any(k in content_lower for k in ['表格', 'table', '| ---', '列']):
        return 'table'
    if any(k in content_lower for k in ['json', 'json格式', '{', '}']):
        return 'json'
    if any(k in content_lower for k in ['清单', '检查', 'checklist', '列表']):
        return 'checklist'
    if any(k in bid for k in ['report', 'analysis', 'review']):
        return 'report'
    if any(k in bid for k in ['list', 'steps', 'plan']):
        return 'list'
    return 'markdown'


def generate_quality_checks(category, block_id, title):
    """根据分类生成通用质量检查项"""
    base_checks = [
        '输出内容是否与标题主题一致',
        '是否有明确的执行目标',
    ]

    category_checks = {
        'role': ['角色设定是否清晰可执行', '是否避免了过于宽泛的角色描述'],
        'task': ['任务目标是否可验证', '输出是否包含可执行的步骤或结果'],
        'context': ['上下文信息是否充分', '是否避免了不必要的背景噪音'],
        'constraints': ['约束条件是否可量化', '约束是否与任务目标不矛盾'],
        'format': ['输出格式是否符合指定标准', '格式是否在不同平台通用'],
        'examples': ['示例是否与任务场景匹配', '示例数量是否适当'],
        'industry': ['行业知识是否准确', '是否考虑了行业合规性'],
        'decision': ['决策框架是否覆盖关键维度', '是否区分了事实与假设'],
    }

    extra = category_checks.get(category, [])
    return base_checks + extra


def infer_inputs(category, block_id, title):
    """推断输入参数"""
    bid = block_id.lower()

    inputs_map = {
        'role': '用户的任务描述和目标',
        'task': '用户的任务需求和期望结果',
        'context': '任务背景信息',
        'constraints': '任务的限制条件和要求',
        'format': '期望的输出格式要求',
        'examples': '任务的示例输入和输出',
        'industry': '行业相关的任务需求',
        'decision': '需要决策的问题和备选方案',
    }
    return inputs_map.get(category, '用户的需求描述')


def infer_prerequisites(category, block_id):
    """推断前置条件"""
    base = '用户已明确任务目标'
    if category == 'task':
        return '已确定角色设定和上下文'
    if category == 'constraints':
        return '已明确任务和角色'
    if category == 'format':
        return '已确定任务和内容'
    if category == 'examples':
        return '已确定任务和格式要求'
    if category == 'decision':
        return '已收集足够的信息和选项'
    return base


def infer_recommended_with(category, block_id, all_block_ids):
    """推断推荐搭配积木"""
    # 基于分类的推荐规则
    recommendations = {
        'role': [],  # role积木推荐搭配task类
        'task': [],  # task积木推荐搭配role类
        'context': [],
        'constraints': [],
        'format': [],
        'examples': [],
        'industry': [],
        'decision': [],
    }

    # 根据当前积木分类，推荐互补分类的积木
    complementary = {
        'role': ['task'],
        'task': ['role', 'format'],
        'context': ['role', 'task'],
        'constraints': ['task'],
        'format': ['task', 'examples'],
        'examples': ['task', 'format'],
        'industry': ['role', 'task'],
        'decision': ['task', 'constraints'],
    }

    target_categories = complementary.get(category, [])
    result = []

    # 从所有积木中找同分类互补的（取前3个）
    for target_cat in target_categories:
        count = 0
        for bid in all_block_ids:
            if bid.startswith(target_cat + '-') and bid != block_id:
                result.append(bid)
                count += 1
                if count >= 2:
                    break

    return result[:4]  # 最多推荐4个


def migrate():
    """执行迁移"""
    # 读取原始数据
    with open(BLOCKS_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 备份
    with open(BACKUP_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f'✅ 备份已保存: {BACKUP_PATH}')

    # 收集所有积木id（用于推荐搭配）
    all_block_ids = []
    for cat in data['categories']:
        for b in cat.get('blocks', []):
            all_block_ids.append(b['id'])

    # 迁移每个积木
    total = 0
    role_stats = {}
    for cat in data['categories']:
        cat_id = cat['id']
        for b in cat.get('blocks', []):
            # 推断新字段
            agent_role = infer_agent_role(b['id'], cat_id, b.get('title', ''), b.get('tags', []))
            output_format = infer_output_format(b['id'], cat_id, b.get('content', ''))
            quality_checks = generate_quality_checks(cat_id, b['id'], b.get('title', ''))
            inputs = infer_inputs(cat_id, b['id'], b.get('title', ''))
            prerequisites = infer_prerequisites(cat_id, b['id'])
            recommended_with = infer_recommended_with(cat_id, b['id'], all_block_ids)

            # 添加新字段（不覆盖已有字段）
            b['agentRole'] = agent_role
            b['inputs'] = inputs
            b['prerequisites'] = prerequisites
            b['outputFormat'] = output_format
            b['qualityChecks'] = quality_checks
            b['recommendedWith'] = recommended_with

            total += 1
            role_stats[agent_role] = role_stats.get(agent_role, 0) + 1

    # 写回
    with open(BLOCKS_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f'✅ 迁移完成: {total}个积木已标准化')
    print()
    print('角色分布:')
    for role, count in sorted(role_stats.items(), key=lambda x: -x[1]):
        print(f'  {role}: {count}个')
    print()
    print('新增字段:')
    new_fields = ['agentRole', 'inputs', 'prerequisites', 'outputFormat', 'qualityChecks', 'recommendedWith']
    print(f'  {", ".join(new_fields)}')


if __name__ == '__main__':
    migrate()
