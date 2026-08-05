from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance
from sentence_transformers import SentenceTransformer
from qdrant_client.models import PointStruct
import uuid
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from qdrant_client.models import Filter, FieldCondition, MatchValue
import uvicorn

client = QdrantClient(url="http://localhost:6333")
COLLECTION_NAME = "legal_documents"

def init_db():
    if not client.collection_exists(COLLECTION_NAME):
        # Khởi tạo không gian vector 768 chiều, dùng Cosine Similarity
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(size=768, distance=Distance.COSINE),
        )
        print(f"Đã tạo collection {COLLECTION_NAME} thành công!")

init_db()

# Load model embedding tiếng Việt chuyên dụng
model = SentenceTransformer('keepitreal/vietnamese-sbert')

# Dữ liệu giả lập
sample_data = [
    {"text": "Quy định về thu hồi đất vì mục đích quốc phòng, an ninh và phát triển kinh tế.", "topic": "ThuHoiDat", "issuance_year": 2024},
    {"text": "Điều kiện chuyển nhượng quyền sử dụng đất nông nghiệp.", "topic": "ChuyenNhuong", "issuance_year": 2024},
    {"text": "Hạn mức giao đất ở tại nông thôn và đô thị.", "topic": "HanMucDat", "issuance_year": 2013},
]

def insert_data():
    # Tạo Payload Index trước khi insert để tối ưu tốc độ lọc
    client.create_payload_index(collection_name=COLLECTION_NAME, field_name="topic", field_schema="keyword")
    client.create_payload_index(collection_name=COLLECTION_NAME, field_name="issuance_year", field_schema="integer")

    points = []
    for doc in sample_data:
        # Bước Ingest & Embed: Biến chữ thành mảng số 768 chiều
        vector = model.encode(doc["text"]).tolist()
        
        # Đóng gói. Dùng uuid5 băm từ nội dung văn bản để luôn sinh ra 1 ID cố định
        # Giúp tránh trùng lặp dữ liệu (duplicate) nếu bạn vô tình chạy lại hàm này nhiều lần
        point_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, doc["text"]))
        
        point = PointStruct(
            id=point_id, 
            vector=vector,
            payload={"text": doc["text"], "topic": doc["topic"], "issuance_year": doc["issuance_year"]} # Đây chính là Metadata
        )
        points.append(point)
        
    client.upsert(collection_name=COLLECTION_NAME, points=points)
    print("Đã tạo Payload Index và insert toàn bộ dữ liệu mẫu!")

insert_data()

collection_info = client.get_collection(COLLECTION_NAME)
print("\nPayload schema:")
for field_name, field_schema in collection_info.payload_schema.items():
    print(f"- {field_name}: {field_schema.data_type.value}")

app = FastAPI(title="Qdrant Search API")

class SearchRequest(BaseModel):
    query: str
    top_k: int = 2
    topic: Optional[str] = None
    issuance_year: Optional[int] = None
    threshold: float = 0.5

@app.post("/search")
def search_documents(req: SearchRequest):
    # 1. Embed câu hỏi của người dùng ra vector
    query_vector = model.encode(req.query).tolist()
    
    # 2. Xây dựng cấu trúc Lọc (Pre-filtering)
    must_conditions = []
    if req.topic:
        must_conditions.append(FieldCondition(key="topic", match=MatchValue(value=req.topic)))
    if req.issuance_year is not None:
        must_conditions.append(
            FieldCondition(
                key="issuance_year",
                match=MatchValue(value=req.issuance_year),
            )
        )
        
    query_filter = Filter(must=must_conditions) if must_conditions else None
        
    # 3. Tiến hành tìm kiếm trong Qdrant
    search_result = client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_vector,
        query_filter=query_filter,
        limit=req.top_k,
        score_threshold=req.threshold
    ).points
    
    return {
        "query": req.query,
        "results": [
            {"score": hit.score, "text": hit.payload["text"], "topic": hit.payload["topic"], "issuance_year": hit.payload["issuance_year"]} 
            for hit in search_result
        ]
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=1810)
