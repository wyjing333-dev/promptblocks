# -*- coding: utf-8 -*-
"""验证质量评分体系"""
import json

with open('D:/jieyuexingchen/promptblocks/quality_scoring.json', 'r', encoding='utf-8') as f:
    qs = json.load(f)

print(f'名称: {qs["name"]}')
print(f'维度数: {len(qs["dimensions"])}')
print(f'总分: {qs["totalScore"]}')
print(f'通过线: {qs["passThreshold"]}分')
print(f'修改线: {qs["reviseThreshold"]}分')
print()

print('8维度评分:')
for d in qs['dimensions']:
    print(f'  {d["name"]} ({d["nameEn"]})')
    print(f'    5分: {d["scoring"]["5"][:40]}...')
    print(f'    0分: {d["scoring"]["0"][:40]}...')
    print()

print('等级:')
for grade, info in qs['gradeLevels'].items():
    print(f'  {grade}: {info["min"]}-{info["max"]} -> {info["label"]}')
