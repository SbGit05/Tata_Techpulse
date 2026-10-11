"""Run frozen question set without labels entering the retriever. Optional --llm."""
import json,sys,platform,importlib.metadata,hashlib
from pathlib import Path
from engine import Engine,ROOT,read,utc
import numpy as np
engine=Engine();questions=read(ROOT/'Evaluation_Results/questions.json');rows=[]
mode='llm' if '--llm' in sys.argv else 'evidence'
for q in questions:
    out=engine.ask(q['query'],mode)
    hit=q['expected_source'] in [s['id'] for s in out['evidence']] if q['expected_source'] else None
    valid=all(cid in {s['id'] for s in out['evidence']} for cid in out['citation_ids'])
    passed=(out['abstained']==q['expected_abstain'] and (hit if not q['expected_abstain'] else True) and valid and (mode!='llm' or q['expected_abstain'] or out['mode']=='llm'))
    rows.append(dict(q,output=out,retrieval_hit=hit,citation_id_valid=valid,passed=bool(passed)))
    print(q['id'],'PASS' if passed else 'FAIL','sources',','.join(s['id'] for s in out['evidence']),'mode',out['mode'],flush=True)
in_scope=[r for r in rows if not r['expected_abstain']];ood=[r for r in rows if r['expected_abstain']];answered=[r for r in rows if not r['output']['abstained']]
lat=[r['output']['latency_ms'] for r in rows]
metrics=dict(run_at_utc=utc(),mode_requested=mode,questions=len(rows),in_scope=len(in_scope),out_of_scope=len(ood),passed=sum(r['passed'] for r in rows),failed=sum(not r['passed'] for r in rows),retrieval_hit_at_3_percent=round(100*sum(r['retrieval_hit'] for r in in_scope)/len(in_scope),2),abstention_accuracy_percent=round(100*sum(r['output']['abstained'] for r in ood)/len(ood),2),in_scope_answer_rate_percent=round(100*len([r for r in in_scope if not r['output']['abstained']])/len(in_scope),2),citation_id_validity_percent=round(100*sum(r['citation_id_valid'] for r in answered)/len(answered),2) if answered else None,latency_p50_ms=round(float(np.median(lat)),3),latency_p95_ms=round(float(np.percentile(lat,95)),3),llm_generated_answers=sum(r['output']['mode']=='llm' for r in rows),llm_status=engine.model_status(),configuration_sha256=hashlib.sha256((ROOT/'Model_Prompts_Config/config.json').read_bytes()).hexdigest(),prompt_sha256=hashlib.sha256((ROOT/'Model_Prompts_Config/system_prompt.txt').read_bytes()).hexdigest(),claim_faithfulness='NOT_EXPERT_ASSESSED',limitations=['Authored small synthetic corpus; no independent safety expert labels','Queries not used to fit vectorizer or select threshold','Citation ID validity does not prove model faithfulness','No production safety, time-saving or compliance claims'],corpus_sha256=hashlib.sha256((ROOT/'Input_Data/knowledge.json').read_bytes()).hexdigest(),question_set_sha256=hashlib.sha256((ROOT/'Evaluation_Results/questions.json').read_bytes()).hexdigest(),environment=dict(python=platform.python_version(),platform=platform.platform(),packages={p:importlib.metadata.version(p) for p in ['Flask','numpy','scikit-learn','faiss-cpu']}))
suffix='_llm' if mode=='llm' else ''
(ROOT/f'Evaluation_Results/answers{suffix}.json').write_text(json.dumps(rows,indent=2))
(ROOT/f'Evaluation_Results/metrics{suffix}.json').write_text(json.dumps(metrics,indent=2))
print(json.dumps(metrics,indent=2))
