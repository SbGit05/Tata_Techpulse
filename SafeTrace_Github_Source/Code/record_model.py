import urllib.request,json,subprocess
from engine import ROOT
url='http://127.0.0.1:11434/api/tags'
with urllib.request.urlopen(url,timeout=10) as r:data=json.load(r)
try:data['ollama_version']=subprocess.check_output(['ollama','--version'],text=True).strip()
except OSError:data['ollama_version']='Check ollama --version manually'
(ROOT/'Model_Prompts_Config/model_manifest_local.json').write_text(json.dumps(data,indent=2))
print('Recorded local model names and digests. Compare with submitted manifest.')
