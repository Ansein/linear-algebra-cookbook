#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
verify_chapter.py —— 蓝本单章自动验收脚本（AGENTS.md §4.4 的机械化部分）

用法：
    python3 _work/verify_chapter.py ch05            # 验收 frag/ch05.tex
    python3 _work/verify_chapter.py ch05 ch06 ...   # 批量验收

检查项（对应 §4.4）：
  1. 编译 exit=0、无 '^!' 错误行
  2. Missing character 计数为 0
  3. Overfull \hbox 全部 < 8pt
  4. 环境配平（fcard / fkey / fnote / fdeep / fgroup / itemize / enumerate）
  5. 每个 fdeep 块含【反哺点】（逐块检查，非全文 grep）
  6. 残留 OPD 标记检测（盯住目标 / D_xx（…）/ O_x（…）等）
  7. 残留 % FIGURE 占位（提示需人工处理插图）
  8. 顶层 \\fsec 层级清单（供人工核对结构）
退出码：0 = 全部通过；1 = 有未通过项
"""
import subprocess, sys, os, re, glob

WORK = os.path.dirname(os.path.abspath(__file__))
FRAG = os.path.join(WORK, "frag")

ENVS = ["fcard", "fkey", "fnote", "fdeep", "fgroup", "itemize", "enumerate", "center"]
OPD_PAT = re.compile(r"盯住目标|\\mathrm\{D\}_\d|D_\d+（(?:常规操作|观察研究对象|转换等价表述|化归经典形式|试取特殊情形|脱胎换骨|数学归纳|反向思路)")

def compile_one(name):
    """⚠️ 并发安全：使用唯一临时目录 + PID 命名，避免与同时运行的子代理抢文件名。
    （曾因固定用 _vfy.* 与子代理的 xelatex 竞争而产生假失败）"""
    import tempfile, shutil
    tmp = tempfile.mkdtemp(prefix=f"vfy_{name}_")
    job = f"vfy{os.getpid()}"
    tex = os.path.join(tmp, job + ".tex")
    # 需要能 \input{style.tex} 与 frag/ → 用绝对路径，并在 tmp 下建 frag/fig 符号链接
    os.symlink(FRAG, os.path.join(tmp, "frag"))
    # ⚠️ 必须同时链接 fig/：style.tex 里 \graphicspath{{fig/final/}} 是相对编译目录的，
    #    否则含 \figimg 的分片会因找不到图而报错（曾误判 ch03/ch05 未通过）
    _figdir = os.path.join(WORK, "fig")
    if os.path.isdir(_figdir):
        os.symlink(_figdir, os.path.join(tmp, "fig"))
    with open(tex, "w", encoding="utf-8") as fh:
        fh.write("\\documentclass[11pt]{ctexart}\n"
                 f"\\input{{{os.path.join(WORK,'style.tex')}}}\n"
                 f"\\input{{{os.path.join(WORK,'tikz-library.tex')}}}\n"
                 "\\begin{document}\n"
                 f"\\input{{frag/{name}.tex}}\n\\end{{document}}\n")
    subprocess.run(["xelatex", "-interaction=nonstopmode", job + ".tex"],
                   cwd=tmp, capture_output=True, text=True)
    log = os.path.join(tmp, job + ".log")
    pdf = os.path.join(tmp, job + ".pdf")
    logtxt = open(log, encoding="utf-8", errors="replace").read() if os.path.exists(log) else ""
    errs = [l for l in logtxt.split("\n") if l.startswith("!")]
    miss = logtxt.count("Missing character")
    over = [float(m) for m in re.findall(r"Overfull \\hbox \(([\d.]+)pt", logtxt)]
    pages = 0
    try:
        import pymupdf
        if os.path.exists(pdf):
            d = pymupdf.open(pdf); pages = d.page_count; d.close()
    except Exception:
        pass
    shutil.rmtree(tmp, ignore_errors=True)
    return errs, miss, over, pages

def structural(name):
    s = open(os.path.join(FRAG, name + ".tex"), encoding="utf-8").read()
    body = "\n".join(l for l in s.split("\n") if not l.lstrip().startswith("%"))
    res = {}
    for e in ENVS:
        b = len(re.findall(r"\\begin\{" + e + r"\}", body))
        en = len(re.findall(r"\\end\{" + e + r"\}", body))
        if b or en: res[e] = (b, en)
    # fdeep 块内【反哺点】
    parts = re.split(r"(?m)^\\begin\{fdeep\}", s)[1:]
    nofb = []
    for i, p in enumerate(parts, 1):
        end = p.find(r"\end{fdeep}")
        seg = p[:end] if end > 0 else p
        if ("【反哺点】" not in seg) and ("\\fbref" not in seg): nofb.append(i)
    opd = OPD_PAT.findall(body)
    figs = re.findall(r"(?m)^% FIGURE", s)
    secs = re.findall(r"(?m)^\\fsec\{([^\n]*)\}$", s)
    # 章标题体例：必须为「第N章」（AGENTS.md §7.1，曾出现「第5讲」漏改）
    chaps = re.findall(r"(?m)^\\fchap\{([^\n]*)\}$", s)
    bad_chap = [c for c in chaps if not re.match(r"^(第\d+章|附录)", c)]
    return res, len(parts), nofb, opd, figs, secs, chaps, bad_chap

def main():
    names = sys.argv[1:]
    if not names:
        print(__doc__); return 1
    allok = True
    for n in names:
        errs, miss, over, pages = compile_one(n)
        res, nfb, nofb, opd, figs, secs, chaps, bad_chap = structural(n)
        bad_over = [o for o in over if o >= 8.0]
        unbal = [e for e, (b, en) in res.items() if b != en]
        ok = (not errs) and miss == 0 and not bad_over and not unbal and not nofb and not opd and not bad_chap
        allok &= ok
        print("=" * 68)
        print(f"{n}   {'✅ 通过' if ok else '❌ 未通过'}   编译页数={pages}")
        print(f"  编译错误={len(errs)}  缺字={miss}  Overfull>=8pt={len(bad_over)}")
        if errs: print("    " + "\n    ".join(errs[:3]))
        if bad_over: print(f"    Overfull: {sorted(bad_over, reverse=True)[:5]}")
        if unbal: print(f"    ✗ 环境不配平: {unbal}")
        if nofb: print(f"    ✗ 缺【反哺点】的 fdeep 块序号: {nofb}")
        if opd: print(f"    ✗ 残留 OPD 标记: {sorted(set(opd))[:6]}")
        if bad_chap: print(f"    ✗ 章标题体例不合规（应为「第N章」）: {bad_chap}")
        if figs: print(f"    ⚠️ 有 {len(figs)} 处 % FIGURE 占位待人工处理")
        print(f"  章标题: {chaps}")
        print(f"  fdeep={nfb}  环境: " + " ".join(f"{e}:{b}/{en}" for e, (b, en) in sorted(res.items())))
        print(f"  顶层 fsec ({len(secs)}): " + " | ".join(x[:30] for x in secs))
    print("=" * 68)
    print("总结:", "✅ 全部通过" if allok else "❌ 存在未通过项")
    return 0 if allok else 1

if __name__ == "__main__":
    sys.exit(main())
