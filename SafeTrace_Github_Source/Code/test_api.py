import unittest,tempfile,json
from pathlib import Path
import app as module
from engine import Engine
class ApiTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.tmp=tempfile.TemporaryDirectory();module.engine=Engine(database=str(Path(cls.tmp.name)/'api.db'));cls.client=module.app.test_client()
 @classmethod
 def tearDownClass(cls):cls.tmp.cleanup()
 def test_gets(self):
  for p in ['/','/api/status','/api/knowledge','/api/cases','/api/evaluation','/api/export']:self.assertEqual(self.client.get(p).status_code,200,p)
 def test_json_required(self):self.assertEqual(self.client.post('/api/ask',data='query=hello').status_code,415)
 def test_object_required(self):self.assertEqual(self.client.post('/api/ask',json=[]).status_code,400)
 def test_origin_block(self):self.assertEqual(self.client.post('/api/ask',json={'query':'braking'},headers={'Origin':'http://evil.example'}).status_code,403)
 def test_host_block(self):self.assertEqual(self.client.get('/api/knowledge',headers={'Host':'evil.example'}).status_code,403)
 def test_invalid_query(self):self.assertEqual(self.client.post('/api/ask',json={}).status_code,400)
 def test_unknown_case(self):self.assertEqual(self.client.post('/api/review',json={'id':'bad','reviewer':'Tester','decision':'STUDENT_REVIEWED','reason':'Long enough review reason'}).status_code,400)
 def test_oversized(self):self.assertEqual(self.client.post('/api/ask',data='x'*40000,content_type='application/json').status_code,413)
 def test_full_workflow(self):
  d={'example_id':'H01','s':3,'e':4,'c':3,'rationale':'Synthetic assumptions for highway operation.'}
  r=self.client.post('/api/hara',json=d);self.assertEqual(r.status_code,200);id=r.json['id']
  r=self.client.post('/api/review',json={'id':id,'reviewer':'Test reviewer','decision':'STUDENT_REVIEWED','reason':'Checked source and traceability links.'});self.assertEqual(r.status_code,200)
  r=self.client.post('/api/update',json={'id':id,'field':'test','text':''});self.assertEqual(r.json['review_status'],'PENDING_REVIEW')
if __name__=='__main__':unittest.main(verbosity=2)
