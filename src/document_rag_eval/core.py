from dataclasses import dataclass, asdict
import hashlib, json, re
from pathlib import Path

@dataclass
class ParsedBlock:
    document_id: str; source_path: str; content: str; locator: dict; block_type: str

@dataclass
class Chunk:
    chunk_id: str; document_id: str; content: str; locator: dict; block_type: str

def tokens(s):
    words=set(re.findall(r"[a-z0-9_]+", s.lower()))
    for run in re.findall(r"[\u4e00-\u9fff]+", s): words.update(run[i:i+2] for i in range(len(run)-1)); words.update(run)
    return words
def stable_id(*parts): return hashlib.sha1("|".join(map(str,parts)).encode()).hexdigest()[:12]
def dump_jsonl(path, rows):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text("".join(json.dumps(asdict(r) if hasattr(r,'__dataclass_fields__') else r, ensure_ascii=False)+"\n" for r in rows), encoding='utf-8')
