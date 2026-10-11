"""SafeTrace HARA: synthetic educational retrieval and workflow engine."""
from pathlib import Path
import json, sqlite3, hashlib, uuid, re, time, urllib.request, urllib.error
from datetime import datetime, timezone
import numpy as np
import faiss
from sklearn.feature_extraction.text import TfidfVectorizer
ROOT = Path(__file__).resolve().parents[1]

def utc(): return datetime.now(timezone.utc).isoformat()
def read(path): return json.loads(path.read_text(encoding='utf-8'))

def quality(text):
    issues=[]
    if not re.search(r'\bshall\b',text,re.I): issues.append('Missing shall statement')
    if re.search(r'\b(fast|appropriate|adequate|quickly|normally)\b',text,re.I): issues.append('Vague wording requires review')
    if not re.search(r'\d|reject|disable|suppress',text,re.I): issues.append('No measurable or binary acceptance criterion')
    return issues

class Engine:
    def __init__(self, root=ROOT, database=None):
        self.root=Path(root)
        self.config=read(self.root/'Model_Prompts_Config/config.json')
        self.chunks=read(self.root/'Input_Data/knowledge.json')
        self.examples=read(self.root/'Input_Data/hazards.json')
        self.by_id={c['id']:c for c in self.chunks}
        self.vectorizer=TfidfVectorizer(ngram_range=(1,2),stop_words='english',norm='l2',dtype=np.float32)
        texts=[c['title']+' '+c['text'] for c in self.chunks]
        vectors=self.vectorizer.fit_transform(texts).toarray().astype('float32')
        self.index=faiss.IndexFlatIP(vectors.shape[1]); self.index.add(vectors)
        cache=self.root/'Code/runtime';cache.mkdir(exist_ok=True)
        faiss.write_index(self.index,str(cache/'knowledge.faiss'))
        (cache/'vector_metadata.json').write_text(json.dumps({'chunk_ids':[c['id'] for c in self.chunks], 'dimensions':vectors.shape[1], 'corpus_sha256':hashlib.sha256((self.root/'Input_Data/knowledge.json').read_bytes()).hexdigest()},indent=2))
        self.database=str(database or cache/'review.sqlite3')
        with self.db() as db:
            db.executescript('CREATE TABLE IF NOT EXISTS cases (id TEXT PRIMARY KEY, payload TEXT NOT NULL); CREATE TABLE IF NOT EXISTS audit (seq INTEGER PRIMARY KEY AUTOINCREMENT, at TEXT, case_id TEXT, action TEXT, detail TEXT);')
    def db(self): return sqlite3.connect(self.database,timeout=20)
    def retrieve(self,query):
        vec=self.vectorizer.transform([query]).toarray().astype('float32')
        scores,inds=self.index.search(vec,self.config['top_k'])
        return [dict(self.chunks[i],score=round(float(s),6)) for i,s in zip(inds[0],scores[0]) if i>=0 and s>=self.config['minimum_score']]
    def model_status(self):
        try:
            with urllib.request.urlopen(self.config['ollama_url']+'/api/tags',timeout=2) as r: data=json.load(r)
            models=data.get('models',[])
            selected=next((m for m in models if m['name']==self.config['model']),None)
            return {'available':selected is not None,'model':self.config['model'],'installed_models':[m['name'] for m in models],'digest':selected.get('digest') if selected else None}
        except (OSError,ValueError):return {'available':False,'model':self.config['model'],'reason':'Local Ollama endpoint unavailable'}
    def ask(self,query,mode='evidence'):
        if not isinstance(query,str) or not query.strip() or len(query)>2000: raise ValueError('Query must contain 1 to 2000 characters')
        if mode not in ('evidence','llm'):raise ValueError('Unknown mode')
        start=time.perf_counter();evidence=self.retrieve(query)
        blocked=bool(re.search(r'\b(certify|certification|approve.*vehicle|ignore.*instructions)\b',query,re.I))
        result=dict(query=query,requested_mode=mode,mode='evidence',evidence=evidence,review_status='PENDING_REVIEW',abstained=not evidence or blocked,citation_ids=[],model_used=None)
        if result['abstained']:
            result['answer']='Insufficient applicable evidence or request outside scope. I cannot certify or approve a vehicle. Provide an in-scope engineering question for review.'
        else:
            result['answer']='\n\n'.join(f"[{c['id']}] {c['text']}" for c in evidence)
            result['citation_ids']=[c['id'] for c in evidence]
            if mode=='llm':
                system=(self.root/'Model_Prompts_Config/system_prompt.txt').read_text()
                context='\n\n'.join(f"[{c['id']}] {c['text']}" for c in evidence)
                payload=dict(model=self.config['model'],stream=False,messages=[dict(role='system',content=system),dict(role='user',content=f'EVIDENCE:\n{context}\nQUESTION:\n{query}\nReturn JSON with answer and citations. Allowed source IDs: '+', '.join(c['id'] for c in evidence))],options={k:self.config[k] for k in ['temperature','num_ctx','num_predict','seed','num_thread']})
                payload['format']={'type':'object','properties':{'answer':{'type':'string'},'citations':{'type':'array','minItems':1,'maxItems':3,'items':{'type':'string','enum':[c['id'] for c in evidence]}}},'required':['answer','citations'],'additionalProperties':False}
                try:
                    request=urllib.request.Request(self.config['ollama_url']+'/api/chat',data=json.dumps(payload).encode(),headers={'Content-Type':'application/json'})
                    with urllib.request.urlopen(request,timeout=180) as response:data=json.load(response)
                    raw=data['message']['content']; result['model_attempt']={'raw_answer':raw,'citation_validation':'PENDING'}
                    structured=json.loads(raw)
                    answer=structured.get('answer');ids=structured.get('citations')
                    if not isinstance(answer,str) or not answer.strip() or not isinstance(ids,list) or any(not isinstance(i,str) for i in ids):raise ValueError('Malformed structured model response')
                    permitted={c['id'] for c in evidence}
                    if not ids or not set(ids)<=permitted:raise ValueError('Missing or invalid evidence citation; model response withheld')
                    result['model_attempt']['citation_validation']='VALID_IDS_ONLY'
                    answer=answer+' '+ ' '.join('['+i+']' for i in sorted(set(ids)))
                    result.update(answer=answer,mode='llm',citation_ids=sorted(set(ids)),model_used=self.config['model'],faithfulness='UNVERIFIED_DRAFT',model_timing_ns=data.get('eval_duration'))
                except (OSError,ValueError,KeyError,AttributeError,TypeError) as exc:
                    result['fallback_reason']=f'Local model failed or citation validation failed: {type(exc).__name__}. Evidence mode returned instead.'
        result['latency_ms']=round((time.perf_counter()-start)*1000,3)
        return result
    def classify(self,s,e,c):
        # Booleans are deliberately rejected despite being Python ints.
        for v,limit in [(s,3),(e,4),(c,3)]:
            if type(v) is not int or not 0<=v<=limit:raise ValueError('S/E/C must be integer ratings in the configured ranges')
        return {'candidate_asil':self.config['rules'][f'{s},{e},{c}'],'rule_version':self.config['rules_version'],'rule_status':self.config['rules_status'],'notice':'Synthetic demo lookup; expert approval required. This is not a safety determination.'}
    def trace(self,case):
        fields=['hazard','goal','fsr','tsr','test']
        missing=[f for f in fields if not str(case.get(f,'')).strip()]
        return dict(completeness_percent=round(100*(len(fields)-len(missing))/len(fields),1),missing=missing,chain=[{'id':case['id']+'-'+f.upper(),'kind':f,'text':case.get(f,'')} for f in fields],notice='Structural completeness only; semantic validity not assessed')
    def create_case(self,example_id,s,e,c,rationale):
        if not isinstance(rationale,str) or not 10<=len(rationale.strip())<=2000:raise ValueError('Provide a rationale of 10 to 2000 characters')
        r=next((r for r in self.examples if r['id']==example_id),None)
        if not r:raise ValueError('Unknown synthetic example')
        case=dict(r);case.update(self.classify(s,e,c));case.update(id='CASE-'+uuid.uuid4().hex[:8],source_id=example_id,s=s,e=e,c=c,rationale=rationale,review_status='PENDING_REVIEW',created_at=utc(),revision=1)
        case['quality_issues']={'fsr':quality(case['fsr']),'tsr':quality(case['tsr'])};case['traceability']=self.trace(case)
        self.save(case,'CREATE','Synthetic reference selected; student ratings recorded')
        return case
    def save(self,case,action,detail):
        with self.db() as db:
            db.execute('INSERT OR REPLACE INTO cases VALUES (?,?)',(case['id'],json.dumps(case)))
            db.execute('INSERT INTO audit(at,case_id,action,detail) VALUES (?,?,?,?)',(utc(),case['id'],action,detail))
    def cases(self):
        with self.db() as db:return [json.loads(r[0]) for r in db.execute('SELECT payload FROM cases ORDER BY rowid DESC')]
    def get(self,id):
        with self.db() as db:r=db.execute('SELECT payload FROM cases WHERE id=?',(id,)).fetchone()
        if not r:raise ValueError('Unknown case')
        return json.loads(r[0])
    def review(self,id,reviewer,decision,reason):
        if decision not in ['STUDENT_REVIEWED','REJECTED']:raise ValueError('Review decision invalid')
        if not isinstance(reviewer,str) or not 2<=len(reviewer.strip())<=100 or not isinstance(reason,str) or not 10<=len(reason.strip())<=1000:raise ValueError('Reviewer and reason required')
        case=self.get(id)
        if decision=='STUDENT_REVIEWED' and case['traceability']['missing']:raise ValueError('Complete traceability before student review')
        case.update(review_status=decision,reviewer=reviewer,review_reason=reason,reviewed_at=utc());self.save(case,'REVIEW',json.dumps(dict(reviewer=reviewer,decision=decision,reason=reason)));return case
    def update(self,id,field,text):
        if field not in ['goal','fsr','tsr','test']:raise ValueError('Only goal, FSR, TSR and test can be edited')
        if not isinstance(text,str) or len(text)>2000:raise ValueError('Text must be at most 2000 characters')
        case=self.get(id);case[field]=text;case['revision']+=1;case['review_status']='PENDING_REVIEW'
        for k in ['reviewer','review_reason','reviewed_at']:case.pop(k,None)
        case['traceability']=self.trace(case);case['quality_issues']={'fsr':quality(case['fsr']),'tsr':quality(case['tsr'])}
        case['change_impact']=['goal','fsr','tsr','test'][['goal','fsr','tsr','test'].index(field):]
        self.save(case,'UPDATE',f'{field} edited; review invalidated; downstream links require review');return case
    def audit(self):
        with self.db() as db:return [dict(seq=r[0],at=r[1],case_id=r[2],action=r[3],detail=r[4]) for r in db.execute('SELECT * FROM audit ORDER BY seq')]
