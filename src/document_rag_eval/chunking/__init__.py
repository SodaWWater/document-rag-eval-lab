from document_rag_eval.core import Chunk, stable_id
def make_chunks(blocks):
    return [Chunk(stable_id(b.document_id,b.locator,b.content),b.document_id,b.content,b.locator,b.block_type) for b in blocks]
