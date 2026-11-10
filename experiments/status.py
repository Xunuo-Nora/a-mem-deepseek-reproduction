import json,re
from pathlib import Path
r=Path(__file__).resolve().parents[1]/'results'
text=(r/'study_run.log').read_text(errors='replace')
notes=re.findall(r'Memory (\d+)/369',text)
calls=[json.loads(l) for l in (r/'study_calls.jsonl').read_text().splitlines()]
p=r/'predictions.jsonl'
print(json.dumps({'notes':int(notes[-1]) if notes else 0,'answers':len(p.read_text().splitlines()) if p.exists() else 0,'calls':len(calls),'peak_cost_upper_cny':round(sum((x['usage']['prompt_tokens']*2+x['usage']['completion_tokens']*8)/1e6 for x in calls),4),'last_log_lines':text.splitlines()[-2:]},ensure_ascii=False))
