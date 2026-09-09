import sys,json,argparse
from pathlib import Path
sys.path.insert(0,'src')
from document_rag_eval.core import Chunk
from document_rag_eval.retrieval import retrieve
from document_rag_eval.citation import citations
root=Path(__file__).parents[1]; ap=argparse.ArgumentParser(); ap.add_argument('--query',required=True); a=ap.parse_args()
chunks=[Chunk(**json.loads(x)) for x in (root/'results/examples/chunks.jsonl').read_text(encoding='utf-8').splitlines()]
rows=retrieve(a.query,chunks); answer_context=[{'locator':r['locator'],'content':r['content'],'file_name':r['file_name']} for r in rows]; result={'query':a.query,'candidates':rows,'reranked':rows,'answer_context':answer_context,'citations':citations(rows)}
(root/'results/examples/query.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8'); print(json.dumps(result,ensure_ascii=False,indent=2))
