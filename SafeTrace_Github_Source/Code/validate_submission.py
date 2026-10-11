from pathlib import Path
import hashlib,json
root=Path(__file__).resolve().parents[1]
required=['Synopsis','Input_Data','Code','Model_Prompts_Config','Evaluation_Results','Documentation','Video','Declarations']
for d in required:
 assert (root/d).is_dir(),f'Missing folder {d}'
for f in ['Input_Data/knowledge.json','Input_Data/hazards.json','Code/app.py','Model_Prompts_Config/config.json','Evaluation_Results/answers.json','Evaluation_Results/metrics.json']:
 assert (root/f).exists(),f'Missing {f}'
manifest=json.loads((root/'Documentation/checksums.json').read_text())
for rel,digest in manifest.items():
 assert hashlib.sha256((root/rel).read_bytes()).hexdigest()==digest,f'Changed file: {rel}'
print('Required folders, implementation files and release checksums verified.')
print('Manual signatures, student verification, Drive sharing and video are separate requirements.')
