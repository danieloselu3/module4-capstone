"""python -m services.triage.rag_smoke : ground one answer in the small doc set, stub mode."""
from services.rag.retriever import Retriever, grounded_answer

if __name__ == '__main__':
    r = Retriever()
    out = grounded_answer('My child has a fever since yesterday', r)
    assert out['grounded'] and out['sources'][0] == 'faq-fever', out
    print(f'rag smoke OK ({len(r.docs)} docs):', out)
