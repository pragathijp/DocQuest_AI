import json
import sys
import os

sys.path.insert(0, os.path.abspath("."))

from app.retrieval.hybrid import retrieve_chunks

with open("tests/evaluation_questions.json", "r") as f:
    questions = json.load(f)

print(f"Loaded {len(questions)} evaluation questions")

DOC_ID = "8decdd4e-77fb-401f-89be-a4644181c285"

print(f"Evaluating document: {DOC_ID}")

for item in questions:
    question = item["question"]

    chunks = retrieve_chunks(
        question,
        DOC_ID
    )

    retrieved_text = " ".join(
        chunk["chunk"].lower()
        for chunk in chunks
    )

    hits = 0

    for keyword in item["expected_keywords"]:
        if keyword.lower() in retrieved_text:
            hits += 1

    print("\n" + "=" * 60)
    print(f"Question: {question}")
    print(f"Retrieved Chunks: {len(chunks)}")
    print(f"Keyword Hits: {hits}/{len(item['expected_keywords'])}")

    for i, chunk in enumerate(chunks[:3], start=1):
        print(f"\n--- Chunk {i} ---")
        print(chunk["chunk"][:300])