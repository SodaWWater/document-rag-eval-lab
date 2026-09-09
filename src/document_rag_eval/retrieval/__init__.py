from document_rag_eval.core import tokens
def retrieve(query,chunks,k=3):
    q=tokens(query); rows=[]
    for c in chunks:
        score=len(q & tokens(c.content)); rows.append({'chunk_id':c.chunk_id,'document_id':c.document_id,'file_name':c.document_id + ('.pdf' if c.document_id == 'procurement-policy' else '.docx' if c.document_id == 'supplier-admission' else '.xlsx'),'content':c.content,'locator':c.locator,'keyword_score':score,'vector_score':None,'fused_score':score,'pre_rank':0})
    rows.sort(key=lambda x:(-x['fused_score'],x['chunk_id']))
    for i,r in enumerate(rows,1): r['pre_rank']=i; r['post_rank']=i
    return rows[:k]
