import bootstrap
import json,time
from pathlib import Path
from openai import OpenAI
ROOT=bootstrap.ROOT
usage=[]
# Instrument the upstream controller without changing prompts or decoding settings.
import memory_layer_robust as ml
original=ml.RobustOpenAIController.get_completion

def measured(self,prompt,temperature=0.7):
 start=time.monotonic()
 r=self.client.chat.completions.create(model=self.model,messages=[{'role':'system','content':self.SYSTEM_MESSAGE},{'role':'user','content':prompt}],temperature=1.0,max_tokens=4096,extra_body={"thinking":{"type":"disabled"}})
 item={'seconds':time.monotonic()-start,'usage':r.usage.model_dump(),'finish_reason':r.choices[0].finish_reason}
 usage.append(item)
 with (ROOT/'results/pilot_nonthinking_calls.jsonl').open('a') as f:f.write(json.dumps(item)+'\n')
 answer=r.choices[0].message.content
 if not answer or r.choices[0].finish_reason=='length':raise RuntimeError('Empty or truncated response in pilot')
 return answer
ml.RobustOpenAIController.get_completion=measured
from load_dataset import load_locomo_dataset
sample=load_locomo_dataset(str(ROOT/'data/locomo10.json'))[1]
a=ml.RobustAgenticMemorySystem(llm_backend='openai',llm_model='deepseek-flash')
start=time.monotonic()
n=0
for session in sample.conversation.sessions.values():
 for turn in session.turns:
  a.add_note('Speaker '+turn.speaker+'says : '+turn.text,time=session.date_time)
  n+=1
  print('Built',n,'notes',flush=True)
  if n==5:break
 if n==5:break
summary={'notes':n,'calls':len(usage),'seconds':time.monotonic()-start,'prompt_tokens':sum(x['usage']['prompt_tokens'] for x in usage),'completion_tokens':sum(x['usage']['completion_tokens'] for x in usage),'failures':dict(ml.FAILURES)}
(ROOT/'results/pilot_nonthinking_summary.json').write_text(json.dumps(summary,indent=2))
print(json.dumps(summary),flush=True)
