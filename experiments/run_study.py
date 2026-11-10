"""Fixed-subset, paired retrieval-k study using upstream A-MEM memory implementation."""
import bootstrap
import argparse, json, time, random, pickle, hashlib, statistics
from collections import defaultdict
import memory_layer_robust as ml
from load_dataset import load_locomo_dataset
from llm_text_parsers import parse_plain_text_answer
ROOT=bootstrap.ROOT
p=argparse.ArgumentParser();p.add_argument('--pilot',action='store_true');args=p.parse_args()
out=ROOT/'results';out.mkdir(exist_ok=True)
state={'phase':'build','k':None,'trial':None,'question':None}
model=json.loads((out/'connectivity.json').read_text())['requested_model']

def measured(self,prompt,temperature=0.7):
 # Conservative peak pricing, ignoring cache discounts. Reserve the next request
 # using UTF-8 byte count as an upper token bound and the full output cap.
 spent=0.0
 ledger=out/'study_calls.jsonl'
 if ledger.exists():
  for line in ledger.read_text().splitlines():
   u=json.loads(line)['usage'];spent+=(u['prompt_tokens']*2+u['completion_tokens']*8)/1e6
 reserve=((len(prompt.encode('utf-8'))+len(self.SYSTEM_MESSAGE.encode('utf-8'))+1024)*2+4096*8)/1e6
 if spent+reserve>18:raise SystemExit('Budget guard: stop before estimated study cost exceeds CNY 18')
 start=time.monotonic()
 r=self.client.chat.completions.create(model=self.model,messages=[{'role':'system','content':self.SYSTEM_MESSAGE},{'role':'user','content':prompt}],temperature=1.0,max_tokens=4096,extra_body={"thinking":{"type":"disabled"}})
 with (out/'study_calls.jsonl').open('a') as f:
  f.write(json.dumps({**state,'seconds':time.monotonic()-start,'usage':r.usage.model_dump(),'finish_reason':r.choices[0].finish_reason})+'\n')
 text=r.choices[0].message.content
 if not text or r.choices[0].finish_reason=='length':raise RuntimeError('Empty or truncated completion')
 return text
ml.RobustOpenAIController.get_completion=measured
sample=load_locomo_dataset(str(ROOT/'data/locomo10.json'))[1]
a=ml.RobustAgenticMemorySystem(llm_backend='openai',llm_model=model)
cache=ROOT/'.cache/study_memory.pkl'
turns=[(s.date_time,t) for s in sample.conversation.sessions.values() for t in s.turns]
start_index=0
if cache.exists():
 with cache.open('rb') as f:saved=pickle.load(f)
 a.memories=saved['memories'];a.retriever=saved['retriever'];a.evo_cnt=saved['evo_cnt'];start_index=saved['index']
for i,(date,t) in enumerate(turns):
 if i<start_index:continue
 a.add_note('Speaker '+t.speaker+'says : '+t.text,time=date)
 if ml.FAILURES:raise RuntimeError('Upstream swallowed a failure: '+str(dict(ml.FAILURES)))
 with cache.open('wb') as f:pickle.dump({'memories':a.memories,'retriever':a.retriever,'evo_cnt':a.evo_cnt,'index':i+1},f)
 print(f'Memory {i+1}/{len(turns)}',flush=True)
bycat=defaultdict(list)
for i,q in enumerate(sample.qa):
 if q.category in [1,2,3,4]:bycat[q.category].append(i)
rng=random.Random(42)
indices=sorted(i for cat,items in sorted(bycat.items()) for i in rng.sample(items,min(10,len(items))))
manifest={'sample_id':sample.sample_id,'turns':len(turns),'question_indices':indices,'dataset_sha256':hashlib.sha256((ROOT/'data/locomo10.json').read_bytes()).hexdigest(),'model':model,'temperature':1.0,'max_tokens':4096,'thinking':'disabled','ks':[10,5],'trials':3,'memory_condition':'same fixed constructed memory','metric':'upstream token-set F1 and lowercase exact match'}
(out/'manifest.json').write_text(json.dumps(manifest,indent=2))
def tokens(x):return set(str(x).lower().replace('.',' ').replace(',',' ').replace('!',' ').replace('?',' ').split())
def score(pred,ref):
 x,y=tokens(pred),tokens(ref);common=len(x&y)
 return {'f1':2*common/(len(x)+len(y)) if x and y else 0,'exact_match':int(str(pred).strip().lower()==str(ref).strip().lower())}
done=set()
results=out/'predictions.jsonl'
if results.exists():
 for line in results.read_text().splitlines():
  r=json.loads(line);done.add((r['trial'],r['k'],r['question_index']))
state['phase']='qa'
for trial in range(3):
 for qi in indices:
  qa=sample.qa[qi]
  for k in ([10,5] if (trial+qi)%2==0 else [5,10]):
   if (trial,k,qi) in done:continue
   state.update(k=k,trial=trial,question=qi);start=time.monotonic()
   prompt=f'Given the following question, generate several keywords separated by commas.\n\nQuestion: {qa.question}\nKeywords:'
   from llm_text_parsers import parse_keywords_response
   query=parse_keywords_response(a.llm_controller.llm.get_completion(prompt))
   context=a.find_related_memories_raw(query,k=k)
   if qa.category==2:
    prompt=f'Based on the context: {context}, answer the following question. Use DATE of CONVERSATION to answer with an approximate date.\nPlease generate the shortest possible answer, using words from the conversation where possible, and avoid using any subjects.\nQuestion: {qa.question} Short answer:'
   elif qa.category==3:
    prompt=f'Based on the context: {context}, write an answer in the form of a short phrase for the following question. Answer with exact words from the context whenever possible.\nQuestion: {qa.question} Short answer:'
   else:
    prompt=f'Based on the context: {context}, write an answer in the form of a short phrase for the following question. Answer with exact words from the context whenever possible.\n\nQuestion: {qa.question} Short answer:'
   prediction=parse_plain_text_answer(a.llm_controller.llm.get_completion(prompt))
   row={'trial':trial,'k':k,'question_index':qi,'category':qa.category,'question':qa.question,'reference':qa.answer,'prediction':prediction,'seconds':time.monotonic()-start,**score(prediction,qa.answer)}
   with results.open('a') as f:f.write(json.dumps(row)+'\n')
   print(f'QA trial={trial} k={k} q={qi} F1={row["f1"]:.3f}',flush=True)
print('STUDY COMPLETE',flush=True)
