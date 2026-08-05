from qdrant_client import QdrantClient
from qdrant_client.models import Filter, FieldCondition, MatchValue
from sentence_transformers import SentenceTransformer

# Load model (make sure main.py has already inserted the data)
print("Loading model...")
model = SentenceTransformer('keepitreal/vietnamese-sbert')
print("Model loaded.")

client = QdrantClient(url="http://localhost:6333")
COLLECTION_NAME = "legal_documents"

query_text = "Điều kiện bán đất nông nghiệp"
query_vector = model.encode(query_text).tolist()

scenarios = [
    {"name": "No filter, top-k=1, thresh=0.3", "top_k": 1, "thresh": 0.3, "topic": None, "year": None},
    {"name": "No filter, top-k=3, thresh=0.3", "top_k": 3, "thresh": 0.3, "topic": None, "year": None},
    {"name": "No filter, top-k=3, thresh=0.6", "top_k": 3, "thresh": 0.6, "topic": None, "year": None},
    {"name": "Filter ThuHoiDat, top-k=3, thresh=0.6", "top_k": 3, "thresh": 0.6, "topic": "ThuHoiDat", "year": None},
    {"name": "Filter ChuyenNhuong, top-k=3, thresh=0.6", "top_k": 3, "thresh": 0.6, "topic": "ChuyenNhuong", "year": None},
    {"name": "Filter Year=2024, top-k=2, thresh=0.5", "top_k": 2, "thresh": 0.5, "topic": None, "year": 2024},
]

for s in scenarios:
    print(f"--- Scenario: {s['name']} ---")
    query_filter = None
    must_conds = []
    if s["topic"]:
        must_conds.append(FieldCondition(key="topic", match=MatchValue(value=s["topic"])))
    if s["year"]:
        must_conds.append(FieldCondition(key="issuance_year", match=MatchValue(value=s["year"])))
    
    if must_conds:
        query_filter = Filter(must=must_conds)
        
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
