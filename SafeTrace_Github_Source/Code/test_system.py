import tempfile,unittest,json
from pathlib import Path
from engine import Engine,ROOT,quality
class WorkflowTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.eng=Engine(database=str(Path(self.tmp.name)/'review.db'))
 def tearDown(self):self.tmp.cleanup()
 def create(self):return self.eng.create_case('H01',3,4,3,'Synthetic highway event ratings require expert validation.')
 def test_risk_boundaries(self):
  for s in range(4):
   for e in range(5):
    for c in range(4):self.assertIn(self.eng.classify(s,e,c)['candidate_asil'],['QM','A','B','C','D'])
  self.assertEqual(self.eng.classify(3,4,3)['candidate_asil'],'D')
  self.assertEqual(self.eng.classify(0,4,3)['candidate_asil'],'QM')
 def test_invalid_ratings(self):
  for t in [(4,4,3),(-1,1,1),(1,5,1),(1,1,4),(True,1,1),('3',4,3)]:
   with self.assertRaises(ValueError):self.eng.classify(*t)
 def test_create_and_review(self):
  c=self.create();self.assertEqual(c['review_status'],'PENDING_REVIEW');self.assertEqual(c['traceability']['completeness_percent'],100)
  c=self.eng.review(c['id'],'Test reviewer','STUDENT_REVIEWED','Checked source chain against synthetic reference.')
  self.assertEqual(c['review_status'],'STUDENT_REVIEWED');self.assertEqual(len(self.eng.audit()),2)
 def test_change_invalidates_review(self):
  c=self.create();self.eng.review(c['id'],'Test reviewer','STUDENT_REVIEWED','Checked the complete source chain.')
  c=self.eng.update(c['id'],'fsr','The controller shall reject an invalid request within 120 ms.')
  self.assertEqual(c['review_status'],'PENDING_REVIEW');self.assertNotIn('reviewer',c);self.assertEqual(c['revision'],2);self.assertEqual(c['change_impact'],['fsr','tsr','test'])
 def test_gap_blocks_review(self):
  c=self.create();c=self.eng.update(c['id'],'test','');self.assertEqual(c['traceability']['completeness_percent'],80)
  with self.assertRaises(ValueError):self.eng.review(c['id'],'Test reviewer','STUDENT_REVIEWED','Checked remaining links for the demo.')
 def test_rejection_logged(self):
  c=self.create();c=self.eng.review(c['id'],'Test reviewer','REJECTED','The scenario needs additional evidence.')
  self.assertEqual(c['review_status'],'REJECTED')
 def test_quality(self):
  self.assertTrue(quality('Respond quickly and appropriately'))
  self.assertEqual(quality('The monitor shall reject an invalid command within 100 ms.'),[])
 def test_abstention(self):self.assertTrue(self.eng.ask('Write a recipe for chocolate cake')['abstained'])
 def test_certification_block(self):self.assertTrue(self.eng.ask('Certify this vehicle as ISO compliant')['abstained'])
 def test_citations(self):
  out=self.eng.ask('What happens when braking torque is lost on a highway approach?')
  self.assertIn('H01',out['citation_ids']);self.assertFalse(out['abstained'])
 def test_db_persistence(self):
  c=self.create();other=Engine(database=self.eng.database);self.assertEqual(other.get(c['id'])['source_id'],'H01')
 def test_validation(self):
  for q in ['',None,'x'*2001]:
   with self.assertRaises(ValueError):self.eng.ask(q)
  with self.assertRaises(ValueError):self.eng.create_case('bad',3,4,3,'A sufficient synthetic rationale.')
  with self.assertRaises(ValueError):self.eng.create_case('H01',3,4,3,'short')
if __name__=='__main__':unittest.main(verbosity=2)
