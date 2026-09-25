# 考研线性代数蓝本

[![License: CC BY-NC-SA 4.0](https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc-sa/4.0/)
[![Release](https://img.shields.io/github/v/release/Ansein/linear-algebra-cookbook)](https://github.com/Ansein/linear-algebra-cookbook/releases/latest)
[![Issues](https://img.shields.io/github/issues/Ansein/linear-algebra-cookbook)](https://github.com/Ansein/linear-algebra-cookbook/issues)

以《线性代数9讲》（张宇）为骨架、《全国硕士研究生招生考试数学考试大纲》为范围边界，
用北大《高等代数》第五版与樊启斌《高等代数典型问题与方法》补充**深化知识**，
用 LaTeX 重排而成的单册考研复习蓝本。

## ⬇️ 下载

**[📕 考研线性代数蓝本 v1.0.0（167 页，1.4 MB）](https://github.com/Ansein/linear-algebra-cookbook/releases/latest)**
—— 或直接下载：
[`kaoyan-linear-algebra-cookbook-v1.0.0.pdf`](https://github.com/Ansein/linear-algebra-cookbook/releases/download/v1.0.0/kaoyan-linear-algebra-cookbook-v1.0.0.pdf)

```bash
curl -L -o 考研线性代数蓝本.pdf \
  https://github.com/Ansein/linear-algebra-cookbook/releases/download/v1.0.0/kaoyan-linear-algebra-cookbook-v1.0.0.pdf
```

仓库内也保留了源码同名成品 [`考研线性代数蓝本.pdf`](考研线性代数蓝本.pdf)（与 Release 附件字节一致）。

## 特点

- **以考纲为边界**：只收考纲六节（行列式／矩阵／向量／线性方程组／特征值与特征向量／二次型）范围内的内容；考纲原文见附录 C
- **以 9 讲为骨架**：章节结构对应 9 讲，但按考纲重新组织，剔除 OPD 方法论与纯重复练习
- **深化知识就近嵌入**：每章穿插 **155 个灰底「深化拓展」框**，用高等代数的视角回答「为什么」，每条都标注 `【反哺点】`（服务哪条考纲、如何让解题更快更准）
- **重点补强第 6 章**：实测 9 讲「向量空间（仅数学一）」**止于坐标变换公式**，全讲没有内积、施密特正交化、规范正交基、正交矩阵——而这四项都是考纲明确要求。该章深化框最多（26 个）
- **第 8 章为深化示范章**：特征子空间、代数重数 vs 几何重数、最小多项式、不变子空间、根子空间分解、**Jordan 块为何不能相似对角化**、相似不变量清单、实对称正交对角化

## 目录

| 章 | 标题 | 起始页 |
|---|---|---|
| 1 | 行列式 | 5 |
| 2 | 余子式和代数余子式的计算 | 24 |
| 3 | 矩阵运算 | 34 |
| 4 | 矩阵的秩 | 66 |
| 5 | 线性方程组 | 80 |
| 6 | 向量组与向量空间 | 97 |
| 7 | 特征值与特征向量 | 114 |
| 8 | 相似理论 | 123 |
| 9 | 二次型 | 141 |
| 附录 | A 三种关系对照表 / B 常用结论速查 / C 考纲原文 | 163 |

## 如何编译

需要 TeX Live（`xelatex`）与 Python 3。仓库中**不含**源扫描件（体积大），
但成品 PDF 与全部 LaTeX 源码已提交，可直接编译：

```bash
cd _work
xelatex -interaction=nonstopmode xiandai.tex
# 目录/书签需多遍编译，建议用流水线脚本：
python3 ~/.agents/skills/pdf-latex-retypeset/scripts/build.py . --config ../config.json
```

## 仓库结构

```
.
├── 考研线性代数蓝本.pdf      ← 成品（167 页）
├── AGENTS.md                ← 仓库规则：两条核心决定、验收清单、踩坑记录
├── OUTLINE.md               ← 知识补充大纲 + 进度台账 + 逐章施工记录
├── config.json              ← 构建配置（单册）
└── _work/
    ├── style.tex            ← 设计系统（宏、配色、fdeep 灰底框）
    ├── xiandai.tex          ← 主控文档
    ├── frag/                ← 逐章 LaTeX 源码（ch01–ch09 + appendix）
    ├── fig/final/           ← 由源书裁切的 10 张插图
    ├── TRANSCRIBE-SPEC.md   ← 转录规范（供子代理阅读）
    ├── verify_chapter.py    ← 单章验收脚本
    ├── check_bookmarks.py   ← PDF 书签页码校验
    └── safe_write.py        ← 并发写入守卫
```

## 验收标准

每章须通过（`AGENTS.md §4.4`）：

- 编译 `exit=0`、`grep '^!'` 为空
- `Missing character` 计数为 0
- `Overfull \hbox` 全部 `< 8pt`
- 无漏转、无重复（尤其分片接缝页）
- 每个深化框含 `【反哺点】`

机械核查：
```bash
python3 _work/verify_chapter.py ch01 ch02 ch03 ch04 ch05 ch06 ch07 ch08 ch09 appendix
python3 _work/check_bookmarks.py
```

当前状态：**10/10 通过；12/12 书签页码准确；155/155 深化框含反哺点；正文 OPD 残留 0。**

## 排版体例

| 项目 | 规定 |
|---|---|
| 中文引号 | 只用 `“”`（不用 ASCII `"`，不用 `「」`） |
| 蓝 `\key{}` | 「要记住名字」：定理/定义/性质名、方法名 |
| 红 `\warn{}` `\must{}` | 「会做错」：易错点、陷阱、必记结论 |
| 金 `\fbref{}` | `【反哺点】` 标签 |

## 反馈与贡献 — 欢迎提 Issue 🙌

**发现任何问题都欢迎开 Issue，不必客气。** 这份蓝本是逐页看图转录 + 手工重排的产物，
虽然每章都过了自动验收（编译、缺字、溢出、书签页码、反哺点齐全），
但**机器查不出内容错误**。尤其欢迎以下类型：

| 类型 | 例子 |
|---|---|
| 🐛 **内容错误** | 公式抄错、上下标错、结论有误、定理条件漏写 |
| ✏️ **笔误 / 排版** | 错别字、引号或标点异常、公式断行难看、颜色用得不合适 |
| 📐 **数学表述** | 某处「反哺点」没讲清楚、某个深化点其实反哺不了解题 |
| 💡 **内容建议** | 某考点讲得太浅 / 太深、该补的深化知识没补、某段可以删 |
| 🔗 **失效链接** | 下载链接、徽章、交叉引用 |

提 Issue 时如果方便，请附上**页码**（PDF 页脚上的页码即可），这样定位最快。

> 提 Issue 不需要懂 LaTeX。只描述「哪一页、哪里不对、应该是什么」就够了。

**关于 Pull Request**：欢迎，但请先开 Issue 讨论——因为正文改动可能牵涉排版体例
（见下方「排版体例」），先对齐再动手更省事。

## 许可协议

本仓库采用 **[CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/deed.zh-Hans)**
（署名—非商业性使用—相同方式共享 4.0 国际）许可协议，全文见 [`LICENSE`](LICENSE)。

> **您可以**：自由复制、发行、改编本作品。
> **条件是**：署名、**不得用于商业目的**、改编作品须以相同协议分发。

### ⚠️ 来源材料与版权归属

本作品是**学习笔记性质的衍生整理**，正文内容转录、整理、重组自以下材料。
这些来源材料的著作权归各自作者与出版者所有，**不在本协议授权范围内**：

| 来源 | 用途 |
|---|---|
| 《线性代数9讲》（张宇） | 全书章节骨架与例题来源 |
| 《全国硕士研究生招生考试数学考试大纲》 | 收录范围边界的依据（附录 C 为其原文，著作权归教育部教育考试院） |
| 《高等代数》第五版（王萼芳、石生明，高等教育出版社） | 深化拓展内容的主要来源 |
| 《高等代数典型问题与方法》（樊启斌） | 深化拓展内容的补充来源 |

**本协议的授权范围仅限于本项目作者独立完成的部分**：LaTeX 排版代码、设计系统、
构建与校验脚本、知识点的取舍与重新组织、深化条目的撰写与「反哺点」评注、
以及全部图表的重绘与裁切。

**免责声明**：本作品仅供个人学习、研究与交流使用，不得用于任何商业目的。
若来源材料的权利人认为本作品的使用方式不当，请联系作者，将立即删除相关内容。

## 说明

- 源扫描件（9 讲、考纲、北大教材、樊启斌教辅）**未提交**，需自行获取
- 深化材料中的每条结论都在 `OUTLINE.md` 中记录了来源（含印刷页）
- `AGENTS.md` 记录了本项目踩过的坑与对策（含一次因脚本失误导致的全库 `$` 丢失与恢复过程）
