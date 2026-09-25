#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
safe_write.py —— 只对"已 settle 的分片"执行写入的守卫脚本

## 为什么需要它
AGENTS.md §4.1b 规定：**子代理运行期间，主控不得编辑其负责的文件**。
本项目已因此踩坑两次：
  · 第 1 章：主控改了 ch01_b 的 OPD 标题，子代理判定为"外部误改"并**按原文恢复**，覆盖了修改。
  · 第 8 章：主控把裁决注释写入 deep_ch08_beida，而该子代理**仍在重写文件**，注释被反复冲掉。

根因：把"文件存在 + 编译通过"误当成"子代理已结束"。唯一可靠依据是 **settle 通知**，
或在无法取通知时，用**文件稳定性**做近似判定（连续 N 秒 md5 不变）。

## 用法
    # 检查某文件是否已稳定（可直接写入）
    python3 _work/safe_write.py check deep_ch08_beida

    # 追加裁决注释（稳定才写；不稳定则拒绝并退出码 1）
    python3 _work/safe_write.py append deep_ch08_beida --note-file /tmp/note.txt

    # 就地替换（稳定才写）
    python3 _work/safe_write.py replace deep_ch08_beida --old old.txt --new new.txt

## 稳定性判定
默认：连续 15 秒内 md5 不变，且文件大小 > 0。可用 --wait 调整总等待秒数。
退出码：0 = 已写入 / 1 = 拒绝写入（文件仍在变化）
"""
import argparse, hashlib, os, sys, time

FRAG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "frag")


def md5(path):
    h = hashlib.md5()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def is_stable(path, window=15.0, interval=3.0):
    """在 window 秒内反复取样，md5 始终不变则视为稳定（子代理可能已结束）"""
    if not os.path.exists(path):
        return False, "文件不存在"
    if os.path.getsize(path) == 0:
        return False, "文件为空"
    t0 = time.time()
    last = md5(path)
    samples = 1
    while time.time() - t0 < window:
        time.sleep(interval)
        cur = md5(path)
        samples += 1
        if cur != last:
            return False, f"仍在变化（{samples} 次取样中检测到 md5 改变）"
        last = cur
    return True, f"稳定（{samples} 次取样 / {window:.0f} 秒内 md5 不变）"


def resolve(name):
    if name.endswith(".tex"):
        return os.path.join(FRAG, name)
    return os.path.join(FRAG, name + ".tex")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("action", choices=["check", "append", "replace"])
    ap.add_argument("name", help="分片名（可带或不带 .tex）")
    ap.add_argument("--note-file", help="append: 要追加的文本文件")
    ap.add_argument("--old", help="replace: 含待替换文本的文件")
    ap.add_argument("--new", help="replace: 含替换文本的文件")
    ap.add_argument("--wait", type=float, default=15.0, help="稳定性观察窗口秒数（默认 15）")
    a = ap.parse_args()

    path = resolve(a.name)
    stable, why = is_stable(path, window=a.wait)
    print(f"[safe_write] {os.path.basename(path)}: {why}")
    if a.action == "check":
        print("→ " + ("可以安全写入" if stable else "**不要写入**（子代理可能仍在运行）"))
        return 0 if stable else 1
    if not stable:
        print("→ 拒绝写入：请等该子代理 settle 后再执行本命令（AGENTS.md §4.1b）")
        return 1

    if a.action == "append":
        if not a.note_file:
            print("append 需要 --note-file"); return 1
        note = open(a.note_file, encoding="utf-8").read()
        with open(path, "a", encoding="utf-8") as f:
            f.write(note)
        print(f"→ 已追加 {len(note)} 字符")
    else:
        if not (a.old and a.new):
            print("replace 需要 --old 与 --new"); return 1
        old = open(a.old, encoding="utf-8").read()
        new = open(a.new, encoding="utf-8").read()
        s = open(path, encoding="utf-8").read()
        if old not in s:
            print("→ 拒绝：未在目标文件中找到待替换文本"); return 1
        n = s.count(old)
        open(path, "w", encoding="utf-8").write(s.replace(old, new))
        print(f"→ 已替换 {n} 处")
    return 0


if __name__ == "__main__":
    sys.exit(main())
