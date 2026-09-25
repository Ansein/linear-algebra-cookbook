# 分片转录计划

> 每个分片起一个**后台**子代理。prompt 模板见 SKILL.md 第 4 节 / `references/subagent-prompt.md`。

所有子代理的 prompt 必须包含：

1. 项目绝对路径
2. **第一步 `read` `_work/TRANSCRIBE-SPEC.md`**
3. 本片图片清单（整页 + 上下半页）
4. 「逐页全部看完，不许跳页」
5. 输出 `_work/frag/<片名>.tex`，然后自检编译（exit=0 且无 `!`）
6. 结构化回复：路径 / 覆盖页数 / 自检结果 / **不确定清单**

---

## xiandai — 线性代数蓝本  (源: 线代9讲强化.pdf)

| 分片 | 页范围 | 整页图 | 半页图 |
|---|---|---|---|
| `ch01_a` | 12-16 | `_work/pages/线代9讲强化_pNN.png` | `_work/pages/线代9讲强化_pNNT.png` / `...B.png` |
| `ch01_b` | 17-20 | `_work/pages/线代9讲强化_pNN.png` | `_work/pages/线代9讲强化_pNNT.png` / `...B.png` |

- 跳过页（封面/目录，子代理不要转写）: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
- 内容页范围: 12-121
