import sys,unittest
from pathlib import Path
sys.path.insert(0,'src')
from document_rag_eval.ingestion import parse_file
from document_rag_eval.chunking import make_chunks
from document_rag_eval.retrieval import retrieve, HybridRetriever
from document_rag_eval.citation import citations
from document_rag_eval.evaluation import evaluate
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
 def test_query_returns_citations_with_filename(self):
  rows=retrieve('金额 待审批',self.chunks); cs=citations(rows); self.assertTrue(cs); self.assertTrue(cs[0]['file_name'].endswith('.pdf'))
 def test_hybrid_retriever_contract(self):
  row=HybridRetriever().retrieve('金额 待审批',self.chunks)[0]
  self.assertIsNone(row['vector_score']); self.assertIn('pre_rank',row); self.assertIn('post_rank',row)
 def test_gold_metrics_are_computed_from_output(self):
  rows=retrieve('供应商准入条件',self.chunks); gold=[{'query_id':'hit','query':'供应商准入条件','relevant_chunk_ids':[rows[0]['chunk_id']]},{'query_id':'miss','query':'不存在内容','relevant_chunk_ids':['missing']}]
  result=evaluate(gold,{'hit':rows,'miss':retrieve('不存在内容',self.chunks)}); self.assertEqual(result['details'][0]['hit_rank'],1); self.assertTrue(result['details'][1]['bad_case']); self.assertEqual(result['recall_at_3'],0.5)
 def test_query_output_contains_real_context(self):
  rows=retrieve('金额 待审批',self.chunks); answer_context=[{'locator':r['locator'],'content':r['content'],'file_name':r['file_name']} for r in rows]
  self.assertTrue(answer_context); self.assertIsInstance(answer_context,list); self.assertIn('locator',answer_context[0]); self.assertIn('content',answer_context[0]); self.assertTrue(any('金额' in item['content'] or '待审批' in item['content'] or '审批' in item['content'] for item in answer_context)); self.assertTrue(any('.pdf' in item['file_name'] or '.docx' in item['file_name'] or '.xlsx' in item['file_name'] for item in answer_context))
if __name__=='__main__': unittest.main()
