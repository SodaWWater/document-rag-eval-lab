def citations(rows):
    return [{'document_id':r['document_id'],'file_name':r.get('file_name', r['document_id'] + '.pdf'),'chunk_id':r['chunk_id'],'locator':r['locator'],'snippet':r['content']} for r in rows]
