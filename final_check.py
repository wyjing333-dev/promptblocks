# -*- coding: utf-8 -*-
from html.parser import HTMLParser
import json

p = HTMLParser()
p.feed(open('index.html', 'r', encoding='utf-8').read())
print('HTML parse OK')

d = json.load(open('blocks.json', 'r', encoding='utf-8'))
w = json.load(open('workflows.json', 'r', encoding='utf-8'))
q = json.load(open('quality_scoring.json', 'r', encoding='utf-8'))
total = sum(len(c['blocks']) for c in d['categories'])
print(f'blocks={total}, workflows={len(w)}, score_dims={len(q["dimensions"])}')
