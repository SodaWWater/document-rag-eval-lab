import sys,unittest
from pathlib import Path
sys.path.insert(0,'src')
from document_rag_eval.ingestion import parse_file
from document_rag_eval.chunking import make_chunks
from document_rag_eval.retrieval import retrieve
class TestRAG(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.root=Path(__file__).parents[1]; cls.blocks=[]
  for p in (cls.root/'data/samples').iterdir(): cls.blocks += parse_file(p)
  cls.chunks=make_chunks(cls.blocks)
 def test_three_formats_and_locators(self):
  self.assertTrue(any(x.source_path.endswith('.pdf') and 'page' in x.locator for x in self.blocks)); self.assertTrue(any(x.source_path.endswith('.docx') and ('paragraph_index' in x.locator or 'table_index' in x.locator) for x in self.blocks)); self.assertTrue(any(x.source_path.endswith('.xlsx') and 'sheet' in x.locator for x in self.blocks))
 def test_stable_chunk_and_citation(self):
  self.assertEqual(make_chunks(self.blocks)[0].chunk_id,self.chunks[0].chunk_id); r=retrieve('金额 待审批',self.chunks); self.assertIn('vector_score',r[0]); self.assertIsNone(r[0]['vector_score']); self.assertIn('locator',r[0])
if __name__=='__main__': unittest.main()
