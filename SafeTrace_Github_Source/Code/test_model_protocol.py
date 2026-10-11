"""Protocol fixture tests; these are NOT real model-evaluation responses."""
import unittest,tempfile,json,io
from unittest.mock import patch
from pathlib import Path
from engine import Engine
class ModelProtocolTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.e=Engine(database=str(Path(self.tmp.name)/'test.db'))
 def tearDown(self):self.tmp.cleanup()
 def response(self,payload):return io.BytesIO(json.dumps({'message':{'content':payload}}).encode())
 def ask(self,payload):
  with patch('urllib.request.urlopen',return_value=self.response(payload)):
   return self.e.ask('How do we prevent unexpected contactor opening?','llm')
 def test_valid_structured_ids(self):
  r=self.ask(json.dumps({'answer':'The controller rejects unauthorized opening.','citations':['H10']}));self.assertEqual(r['mode'],'llm');self.assertIn('[H10]',r['answer'])
 def test_unknown_citation_falls_back(self):
  r=self.ask(json.dumps({'answer':'Invented.','citations':['K99']}));self.assertEqual(r['mode'],'evidence');self.assertIn('fallback_reason',r)
 def test_malformed_json_falls_back(self):self.assertEqual(self.ask('not json')['mode'],'evidence')
 def test_no_citations_falls_back(self):self.assertEqual(self.ask(json.dumps({'answer':'A draft.','citations':[]}))['mode'],'evidence')
 def test_model_unavailable_falls_back(self):
  with patch('urllib.request.urlopen',side_effect=OSError('unavailable')):
   self.assertEqual(self.e.ask('Unexpected contactor opening','llm')['mode'],'evidence')
if __name__=='__main__':unittest.main(verbosity=2)
