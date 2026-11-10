from pathlib import Path
import os, sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
for name,folder in {'HF_HOME':'hf','TORCH_HOME':'torch','NLTK_DATA':'nltk','MPLCONFIGDIR':'matplotlib','XDG_CACHE_HOME':'xdg'}.items():
 p=ROOT/'.cache'/folder;p.mkdir(parents=True,exist_ok=True);os.environ[name]=str(p)
os.environ['LITELLM_LOCAL_MODEL_COST_MAP']='True'
from dotenv import load_dotenv
load_dotenv(ROOT/'.env')
