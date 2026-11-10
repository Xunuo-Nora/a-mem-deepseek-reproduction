"""Validate completeness, then summarize paired experiments without API calls."""
import json,statistics,csv
from pathlib import Path
from collections import defaultdict
root=Path(__file__).resolve().parents[1];out=root/'results'
m=json.loads((out/'manifest.json').read_text())
rows=[json.loads(l) for l in (out/'predictions.jsonl').read_text().splitlines()]
expected={(t,k,q) for t in range(m['trials']) for k in m['ks'] for q in m['question_indices']}
actual=[(r['trial'],r['k'],r['question_index']) for r in rows]
assert len(actual)==len(set(actual)), 'Duplicate experiment rows'
assert set(actual)==expected, f'Incomplete: {len(set(actual))}/{len(expected)}'
assert all(0<=r['f1']<=1 for r in rows)
if (out/'study_calls.jsonl').exists():
 calls=[json.loads(l) for l in (out/'study_calls.jsonl').read_text().splitlines()]
else:
 with (out/'usage.csv').open(newline='') as f:
  calls=[{'phase':r['phase'], 'k':int(r['k']) if r['k'] else None,
          'usage':{'prompt_tokens':int(r['prompt_tokens']),
                   'completion_tokens':int(r['completion_tokens'])}}
         for r in csv.DictReader(f)]
summary={'sample_id':m['sample_id'],'questions':len(m['question_indices']),'arms':{},'build':{}}
for k in m['ks']:
 a=[r for r in rows if r['k']==k]
 trial_means=[statistics.mean(r['f1'] for r in a if r['trial']==t) for t in range(m['trials'])]
 c=[r for r in calls if r['phase']=='qa' and r['k']==k]
 summary['arms'][str(k)]={'f1_mean':statistics.mean(trial_means),'f1_sample_variance':statistics.variance(trial_means),'f1_trial_means':trial_means,'exact_match':statistics.mean(r['exact_match'] for r in a),'mean_seconds':statistics.mean(r['seconds'] for r in a),'prompt_tokens':sum(r['usage']['prompt_tokens'] for r in c),'completion_tokens':sum(r['usage']['completion_tokens'] for r in c),'by_category':{str(cat):statistics.mean(r['f1'] for r in a if r['category']==cat) for cat in sorted({r['category'] for r in a})}}
b=[r for r in calls if r['phase']=='build']
summary['build']={'calls':len(b),'prompt_tokens':sum(r['usage']['prompt_tokens'] for r in b),'completion_tokens':sum(r['usage']['completion_tokens'] for r in b)}
summary['cost_peak_no_cache_upper_cny']=sum((r['usage']['prompt_tokens']*2+r['usage']['completion_tokens']*8)/1e6 for r in calls)
summary['paired_f1_delta_k5_minus_k10']=summary['arms']['5']['f1_mean']-summary['arms']['10']['f1_mean']
(out/'summary.json').write_text(json.dumps(summary,indent=2))
with (out/'predictions.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
print(json.dumps(summary,indent=2))
