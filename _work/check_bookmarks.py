#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""check_bookmarks.py —— 核对 PDF 书签页码与 LaTeX .toc 记录是否一致。
用法： python3 _work/check_bookmarks.py [toc文件] [pdf文件]
"""
import re, sys, os

work = os.path.dirname(os.path.abspath(__file__))
tocf = sys.argv[1] if len(sys.argv) > 1 else os.path.join(work, "xiandai.toc")
pdf = sys.argv[2] if len(sys.argv) > 2 else os.path.join(os.path.dirname(work), "考研线性代数蓝本.pdf")

latex = {}
for line in open(tocf, encoding="utf-8"):
    m = re.match(r"\\contentsline \{section\}\{(.*?)\}\{(\d+)\}", line)
    if m:
        raw, pg = m.group(1), int(m.group(2))
        name = re.sub(r"\\hskip 1em\\relax\s*", "", raw)
        latex[name.replace(" ", "")] = pg   # 归一化：去掉空格（\quad/\hskip 产生的空格）

import pymupdf
d = pymupdf.open(pdf)
ok = True
print(f"{'书签标题':<30} {'书签页':>6} {'toc页':>6}  判定")
for lvl, t, p in d.get_toc():
    if lvl != 1:
        continue
    L = latex.get(t.replace(" ", ""))
    good = (L == p)
    ok &= good
    print(f"{t[:28]:<30} {p:>6} {str(L):>6}  {'✓' if good else '✗'}")
print("\n结论:", "✓ 全部书签页码准确" if ok else "✗ 存在偏差")
sys.exit(0 if ok else 1)
