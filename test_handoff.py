import os
import unittest.mock as mock

print('=== MEMBER 2 HANDOFF CHECKLIST ===')

# [1] All 6 files exist
files = [
    'app/retrieval/rewrite.py',
    'app/retrieval/hybrid.py',
    'app/retrieval/reranker.py',
    'app/retrieval/guardrails.py',
    'app/retrieval/llm.py',
    'app/retrieval/pipeline.py'
]
all_exist = all(os.path.exists(f) for f in files)
print(f'[1] All 6 files exist: {all_exist}')

# [2] Index PDF first
from app.indexing.pipeline import process_document
indexed = process_document('C:/Users/praga/Downloads/report aiml.pdf')
doc_id = indexed['doc_id']

# [3] Contract check
from app.retrieval.pipeline import process_query
r = process_query('What is this document about?', doc_id)
contract_ok = 'answer' in r and 'sources' in r and 'confidence' in r
print(f'[2] Contract (answer, sources, confidence): {contract_ok}')

# [4] Sources never empty when answer returned
sources_ok = len(r['sources']) > 0
print(f'[3] Sources not empty: {sources_ok}')

# [5] Confidence > 0
conf_ok = r['confidence'] > 0
print(f'[4] Confidence > 0: {conf_ok}')

# [6] Guardrail triggers fallback
from app.retrieval.guardrails import validate_chunks
guardrail_ok = validate_chunks([]) == False
print(f'[5] Guardrail triggers on empty chunks: {guardrail_ok}')

# [7] Fallback response shape
with mock.patch('app.retrieval.pipeline.retrieve_chunks', return_value=[]):
    r2 = process_query('test', doc_id)
    fallback_ok = (
        r2['answer'] == 'No relevant info found' and
        r2['sources'] == [] and
        r2['confidence'] == 0
    )
    print(f'[6] Fallback response correct: {fallback_ok}')

# [8] No hardcoded doc_id
print(f'[7] No hardcoded doc_id: manual check — confirm pipeline.py uses only doc_id param')

# [9] Real retrieval working
hybrid_ok = len(r['sources']) >= 2
print(f'[8] Real Qdrant+BM25 retrieval working: {hybrid_ok}')

print()
print('=== DONE ===')