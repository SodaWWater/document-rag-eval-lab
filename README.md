# Document RAG Eval Lab

一个基于开源 RAG 项目学习与二次开发的个人文档问答实验。

项目以采购制度、供应商准入和流程文档为案例，关注从结构化解析、来源定位到检索、重排和引用展示的完整链路。

## 项目内容

- PDF、DOCX、XLSX 的结构化解析适配
- 保留来源坐标的 Chunk 数据结构
- 可扩展的 HybridRetriever 接口,当前基于关键词基线实现、可替换 Reranker
- Citation 展示、Gold Set、Bad Case 回归和离线评测

RAGFlow 是源码学习参考，不复制其完整源码，也不把上游能力计为本项目已实现能力。上游版本、许可证和学习边界记录在 `docs/learning-boundary.md`。

项目使用自建或许可证明确的样本，不包含未授权文档。运行命令、评测结果和演示截图均以仓库中可复现的脚本与原始输出为准。

## 运行

```powershell
python -m unittest discover -s tests -v
python scripts/ingest.py
python scripts/query.py --query "金额超过一万元的待审批订单如何处理"
python scripts/evaluate.py
```

结果写入 `results/examples/`，包括带来源坐标的 chunks、候选与 citations，以及 Recall@3/MRR 摘要。当前关键词检索未启用向量模型，`vector_score` 明确为 `null`；本地结果不代表生产系统效果。
