"""Local-only Flask application. Run python app.py; open http://127.0.0.1:5000."""
from flask import Flask,request,jsonify,render_template,Response
import json, os, csv, io
from engine import Engine,ROOT,read
app=Flask(__name__); app.config['MAX_CONTENT_LENGTH']=32768
engine=Engine(database=os.environ.get('SAFETRACE_DB'))
@app.before_request
def protect():
    # Host restriction and JSON-only mutations protect this loopback demo from browser-origin writes.
    if request.host.split(':')[0] not in ['127.0.0.1','localhost']:return jsonify(error='Loopback host required'),403
    if request.method in ['POST','PUT','DELETE']:
        origin=request.headers.get('Origin')
        if origin and origin not in ['http://'+request.host]:return jsonify(error='Cross-origin mutation refused'),403
        if not request.is_json:return jsonify(error='JSON content required'),415
        if not isinstance(request.get_json(silent=True),dict):return jsonify(error='JSON object required'),400
@app.errorhandler(ValueError)
def bad(e):return jsonify(error=str(e)),400
@app.errorhandler(413)
def large(e):return jsonify(error='Request exceeds 32 KiB'),413
@app.get('/')
def index():return render_template('index.html')
@app.get('/api/knowledge')
def knowledge():return jsonify(chunks=engine.chunks,examples=engine.examples)
@app.get('/api/status')
def status():return jsonify(engine=engine.config['version'],model=engine.model_status(),default_mode='evidence',data='SYNTHETIC',rules=engine.config['rules_status'])
@app.post('/api/ask')
def ask():
    d=request.get_json();return jsonify(engine.ask(d.get('query'),d.get('mode','evidence')))
@app.post('/api/hara')
def hara():
    d=request.get_json();return jsonify(engine.create_case(d.get('example_id'),d.get('s'),d.get('e'),d.get('c'),d.get('rationale')))
@app.get('/api/cases')
def cases():return jsonify(cases=engine.cases(),audit=engine.audit())
@app.post('/api/review')
def review():
    d=request.get_json();return jsonify(engine.review(d.get('id'),d.get('reviewer'),d.get('decision'),d.get('reason')))
@app.post('/api/update')
def update():
    d=request.get_json();return jsonify(engine.update(d.get('id'),d.get('field'),d.get('text')))
@app.get('/api/export')
def export():
    buf=io.StringIO();writer=csv.writer(buf);fields=['id','source_id','item','scenario','hazard','s','e','c','candidate_asil','goal','fsr','tsr','test','review_status','rule_version']
    writer.writerow(fields)
    for c in engine.cases():
        vals=[str(c.get(f,'')) for f in fields]
        writer.writerow(["'"+v if v[:1] in ['=','+','-','@'] else v for v in vals])
    return Response(buf.getvalue(),mimetype='text/csv',headers={'Content-Disposition':'attachment; filename=SafeTrace_Traceability.csv'})
@app.get('/api/evaluation')
def evaluation():
    file=ROOT/'Evaluation_Results/metrics.json'
    return jsonify(read(file) if file.exists() else {'status':'Run python evaluate.py'})
if __name__=='__main__':app.run(host='127.0.0.1',port=5000,debug=False)
