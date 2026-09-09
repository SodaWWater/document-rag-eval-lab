def evaluate(gold, outputs, k=3):
    recalls=[]; mrrs=[]; details=[]
    for g in gold:
        ids=[x['chunk_id'] for x in outputs.get(g['query_id'],[])]; rel=set(g['relevant_chunk_ids']); hit=next((i+1 for i,x in enumerate(ids) if x in rel),None)
        recalls.append(1 if any(x in rel for x in ids[:k]) else 0); mrrs.append(1/hit if hit else 0); details.append({'query_id':g['query_id'],'hit_rank':hit,'bad_case':hit is None})
    return {'recall_at_3':sum(recalls)/len(recalls),'mrr':sum(mrrs)/len(mrrs),'details':details}
