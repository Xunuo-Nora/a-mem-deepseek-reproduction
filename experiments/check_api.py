from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI
import json, os
root=Path(__file__).resolve().parents[1]
load_dotenv(root/'.env')
if not os.getenv('OPENAI_API_KEY'): raise SystemExit('API key is empty')
c=OpenAI(timeout=60,max_retries=0)
try:
 models=[m.id for m in c.models.list().data]
 print(json.dumps({'available_models':models}))
 model='deepseek-chat' if 'deepseek-chat' in models else models[0]
 r=c.chat.completions.create(model=model,messages=[{'role':'user','content':'Reply with exactly READY'}],max_tokens=32)
 result={'model':r.model,'requested_model':model,'reply':r.choices[0].message.content,'usage':r.usage.model_dump()}
 (root/'results/connectivity.json').write_text(json.dumps(result,indent=2))
 print(json.dumps(result))
except Exception as e:
 print('Connection failed:',type(e).__name__,getattr(e,'status_code',None))
 raise SystemExit(1)
