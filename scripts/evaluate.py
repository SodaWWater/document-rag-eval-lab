import sys,json
from pathlib import Path
sys.path.insert(0,'src')
from document_rag_eval.core import Chunk
from document_rag_eval.retrieval import retrieve
from document_rag_eval.evaluation import evaluate
root=Path(__file__).parents[1]
chunks=[Chunk(**json.loads(x)) for x in (root/'results/examples/chunks.jsonl').read_text(encoding='utf-8').splitlines()]
gold=[json.loads(x) for x in (root/'data/gold/queries.jsonl').read_text(encoding='utf-8').splitlines()]
outs={g['query_id']:retrieve(g['query'],chunks) for g in gold}
result=evaluate(gold,outs)
(root/'results/examples/evaluation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
(root/'results/examples/evaluation.md').write_text(f"# Evaluation{chr(10)}{chr(10)}Recall@3: {result['recall_at_3']:.3f}{chr(10)}{chr(10)}MRR: {result['mrr']:.3f}{chr(10)}",encoding='utf-8')
print(json.dumps(result,ensure_ascii=False,indent=2))
