"""Download the exact author-provided dataset snapshot (no model calls)."""
from pathlib import Path
import hashlib,urllib.request
root=Path(__file__).resolve().parents[1]
target=root/'data/locomo10.json';target.parent.mkdir(exist_ok=True)
url='https://raw.githubusercontent.com/WujiangXu/A-mem/f9a173dec325d84fcc97e7828775c7b241c33466/data/locomo10.json'
if not target.exists():
 with urllib.request.urlopen(url) as response:target.write_bytes(response.read())
print(hashlib.sha256(target.read_bytes()).hexdigest())
