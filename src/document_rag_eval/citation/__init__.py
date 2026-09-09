def citations(rows): return [{'document_id':r['document_id'],'file_name':r['document_id'],'chunk_id':r['chunk_id'],'locator':r['locator'],'snippet':r['content']} for r in rows]
