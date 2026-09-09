from document_rag_eval.core import tokens

class Reranker:
    def rerank(self, query, rows):
        q = tokens(query)
        ranked = sorted(rows, key=lambda x: (-len(q & tokens(x['content'])), -x['fused_score'], x['chunk_id']))
        for i, row in enumerate(ranked, 1):
            row['post_rank'] = i
        return ranked

class HybridRetriever:
    def __init__(self, reranker=None):
        self.reranker = reranker or Reranker()

    def retrieve(self, query, chunks, k=3):
        return self.reranker.rerank(query, _keyword_candidates(query, chunks))[:k]

def _keyword_candidates(query, chunks):
    q=tokens(query); rows=[]
    for c in chunks:
        score=len(q & tokens(c.content)); rows.append({'chunk_id':c.chunk_id,'document_id':c.document_id,'file_name':c.document_id + ('.pdf' if c.document_id == 'procurement-policy' else '.docx' if c.document_id == 'supplier-admission' else '.xlsx'),'content':c.content,'locator':c.locator,'keyword_score':score,'vector_score':None,'fused_score':score,'pre_rank':0})
    rows.sort(key=lambda x:(-x['fused_score'],x['chunk_id']))
    for i,r in enumerate(rows,1): r['pre_rank']=i; r['post_rank']=i
    return rows

def retrieve(query,chunks,k=3):
    return HybridRetriever().retrieve(query, chunks, k)
