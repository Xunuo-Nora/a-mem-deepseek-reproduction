import bootstrap
import nltk
for name in ['punkt','punkt_tab','wordnet']:
 nltk.download(name,download_dir=bootstrap.os.environ['NLTK_DATA'],quiet=True)
from sentence_transformers import SentenceTransformer
m=SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2',device='cpu')
assert m.encode(['test']).shape==(1,384)
print('Embedding model ready on CPU')
