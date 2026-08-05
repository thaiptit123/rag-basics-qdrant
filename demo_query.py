from qdrant_client import QdrantClient
from qdrant_client.models import Filter, FieldCondition, MatchValue
from sentence_transformers import SentenceTransformer

# Load model (make sure main.py has already inserted the data)
print("Loading model...")
model = SentenceTransformer('keepitreal/vietnamese-sbert')
print("Model loaded.")

client = QdrantClient(url="http://localhost:6333")
COLLECTION_NAME = "legal_documents"

query_text = "Thành lập công ty"
query_vector = model.encode(query_text).tolist()

scenarios = [
    {"name": "No filter, top-k=1, thresh=0.3", "top_k": 1, "thresh": 0.3, "topic": None},
    {"name": "No filter, top-k=3, thresh=0.3", "top_k": 3, "thresh": 0.3, "topic": None},
    {"name": "No filter, top-k=3, thresh=0.6", "top_k": 3, "thresh": 0.6, "topic": None},
    {"name": "Filter LuatDatDai, top-k=3, thresh=0.6", "top_k": 3, "thresh": 0.6, "topic": "LuatDatDai"},
    {"name": "Filter LuatKinhDoanh, top-k=3, thresh=0.6", "top_k": 3, "thresh": 0.6, "topic": "LuatKinhDoanh"},
]

for s in scenarios:
    print(f"--- Scenario: {s['name']} ---")
    query_filter = None
    if s["topic"]:
        query_filter = Filter(must=[FieldCondition(key="topic", match=MatchValue(value=s["topic"]))])
        
    res = client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_vector,
        query_filter=query_filter,
        limit=s["top_k"],
        score_threshold=s["thresh"]
    ).points
    
    print(f"Results Count: {len(res)}")
    for hit in res:
        print(f"  Score: {hit.score:.4f} | Text: {hit.payload['text']}")
    print("")
