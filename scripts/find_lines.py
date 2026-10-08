# -*- coding: utf-8 -*-
"""Find relevant line numbers in index.html"""
import re

with open(r"D:\jieyuexingchen\promptblocks\index.html", "r", encoding="utf-8") as f:
    lines = f.readlines()

patterns = [
    "block-card", "block-item", "tool-link", ".block ", "hover", "selected",
    "toast", "quick-mode", "preset", "quickMode", "block.selected",
    "addBlock", "toggleBlock", "block-card"
]

for i, line in enumerate(lines, 1):
    for pat in patterns:
        if pat in line:
            print(f"L{i}: {line.rstrip()[:120]}")
            break
