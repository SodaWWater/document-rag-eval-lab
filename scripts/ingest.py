import sys,json
from pathlib import Path
sys.path.insert(0,'src')
from document_rag_eval.ingestion import parse_file
from document_rag_eval.chunking import make_chunks
root=Path(__file__).parents[1]; blocks=[]
for p in sorted((root/'data/samples').iterdir()): blocks.extend(parse_file(p))
chunks=make_chunks(blocks)
out=root/'results/examples/chunks.jsonl'; out.parent.mkdir(parents=True,exist_ok=True)
out.write_text(chr(10).join(json.dumps(c.__dict__,ensure_ascii=False) for c in chunks)+chr(10),encoding='utf-8')
print(json.dumps({'blocks':len(blocks),'chunks':len(chunks),'path':str(out)},ensure_ascii=False))
