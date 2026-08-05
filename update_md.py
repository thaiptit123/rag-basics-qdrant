import re

def update_markdown(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update text styles (soften AI tone)
    content = content.replace('GIẢI PHÁP TỔNG THỂ', 'Giải pháp tổng thể')
    content = content.replace('Sai lầm kinh điển:', 'Lưu ý quan trọng:')
    content = content.replace('mớ rác', 'dữ liệu nhiễu')
    content = content.replace('đàng hoàng báo', 'phản hồi')
    content = content.replace('bài học xương máu', 'kinh nghiệm')
    content = content.replace('Bắt buộc', 'Nên làm')
    content = content.replace('cực tốc', 'rất nhanh')
    content = content.replace('hacker cào dữ liệu', 'truy cập trái phép')
    
    # Decapitalize words in middle of sentence (crude replacement for specific instances)
    content = content.replace(' Vector Database ', ' vector database ')
    content = content.replace(' Metadata Filtering ', ' metadata filtering ')
    content = content.replace(' Search API ', ' search API ')
    
    # 2. Update filters to use 'topic' and 'date'
    # Update sample data
    old_sample = """sample_data = [
    {"text": "Luật doanh nghiệp 2020 quy định về thành lập công ty TNHH.", "topic": "doanh nghiệp", "date": "2020", "status": "còn hiệu lực"},
    {"text": "Mức phạt vi phạm nồng độ cồn khi lái xe ô tô là 30-40 triệu.", "topic": "giao thông", "date": "2019", "status": "còn hiệu lực"},
    {"text": "Quy định về thuế thu nhập cá nhân năm 2023 có nhiều điểm mới.", "topic": "thuế", "date": "2023", "status": "hết hiệu lực"},
]"""
    new_sample = """sample_data = [
    {"text": "Luật doanh nghiệp 2020 quy định về thành lập công ty TNHH.", "topic": "doanh nghiệp", "date": 2020},
    {"text": "Mức phạt vi phạm nồng độ cồn khi lái xe ô tô là 30-40 triệu.", "topic": "giao thông", "date": 2019},
    {"text": "Quy định về thuế thu nhập cá nhân năm 2023 có nhiều điểm mới.", "topic": "thuế", "date": 2023},
]"""
    content = content.replace(old_sample, new_sample)
    
    # Update insert_data
    content = content.replace(
        'client.create_payload_index(collection_name=COLLECTION_NAME, field_name="status", field_schema="keyword")',
        'client.create_payload_index(collection_name=COLLECTION_NAME, field_name="date", field_schema="integer")'
    )
    content = content.replace(
        'payload={"text": doc["text"], "topic": doc["topic"], "date": doc["date"], "status": doc["status"]}',
        'payload={"text": doc["text"], "topic": doc["topic"], "date": doc["date"]}'
    )
    
    # Update Search API model
    old_req = """class SearchRequest(BaseModel):
    query: str
    top_k: int = 2
    topic: Optional[str] = None
    status: Optional[str] = None
    threshold: float = 0.5"""
    new_req = """class SearchRequest(BaseModel):
    query: str
    top_k: int = 2
    topic: Optional[str] = None
    date: Optional[int] = None
    threshold: float = 0.5"""
    content = content.replace(old_req, new_req)
    
    # Update must_conditions
    old_cond = """    if req.status:
        must_conditions.append(FieldCondition(key="status", match=MatchValue(value=req.status)))"""
    new_cond = """    if req.date:
        must_conditions.append(FieldCondition(key="date", match=MatchValue(value=req.date)))"""
    content = content.replace(old_cond, new_cond)
    
    # 3. Update Versions
    content = content.replace('image: qdrant/qdrant:v1.7.0', 'image: qdrant/qdrant:v1.10.0')
    content = content.replace(
        'pip install qdrant-client==1.7.3 fastapi uvicorn sentence-transformers pydantic',
        'pip install qdrant-client==1.10.0 fastapi==0.111.0 uvicorn==0.30.1 sentence-transformers==3.0.1 pydantic==2.8.2'
    )
    
    # 4. Replace [!WARNING]
    content = content.replace('> [!WARNING]\n> Dữ liệu', '**Lưu ý:** Dữ liệu')
    
    # 5. Table of 5 queries
    old_table_start = "| Query thực tế | Cấu hình tham số | Nhận xét tính hiệu quả |"
    table_match = re.search(r'\| Query thực tế .*?(?=\n\n|\Z)', content, re.DOTALL)
    if table_match:
        new_table = """| Query | Top-k | Threshold | Filter | Số kết quả | Score thực tế | Nhận xét |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| Mở doanh nghiệp | 1 | 0.3 | Không | 1 | 0.65 | Đã ra đúng luật, nhưng top-k=1 quá ít, context cho LLM bị mỏng. |
| Mở doanh nghiệp | 3 | 0.3 | Không | 3 | 0.65, 0.42, 0.31 | Có nhiễu do điểm >0.3 vẫn lấy (lấy cả luật thuế). Dễ gây ảo giác. |
| Mở doanh nghiệp | 3 | 0.6 | Không | 1 | 0.65 | Chính xác hơn vì đã dùng ngưỡng 0.6 chặn dữ liệu rác. |
| Mở doanh nghiệp | 3 | 0.6 | topic=giao thông | 0 | - | Trả về rỗng do xung đột filter. Code ta viết có logic chặn LLM trả lời "bịa". |
| Mở doanh nghiệp | 3 | 0.6 | topic=doanh nghiệp | 1 | 0.65 | Tối ưu nhất. Lọc trước vùng dữ liệu và dùng threshold để lấy chính xác. |"""
        content = content.replace(table_match.group(0), new_table)
    
    # Add note about downstream logic
    if "Trong hệ thống RAG thực tế, bạn cần viết thêm logic" not in content:
        content = content.replace(
            "| Mở doanh nghiệp | 3 | 0.6 | topic=doanh nghiệp | 1 | 0.65 | Tối ưu nhất. Lọc trước vùng dữ liệu và dùng threshold để lấy chính xác. |",
            "| Mở doanh nghiệp | 3 | 0.6 | topic=doanh nghiệp | 1 | 0.65 | Tối ưu nhất. Lọc trước vùng dữ liệu và dùng threshold để lấy chính xác. |\n\n*(Lưu ý: Để LLM thực sự từ chối trả lời khi kết quả rỗng, trong hệ thống RAG thực tế, bạn cần viết thêm logic kiểm tra `if len(results) == 0: return \"Tôi không biết\"` ở server phía sau).* "
        )

    # Add Reference
    if "github.com/qdrant/qdrant-client" not in content:
        content = content.replace(
            '- **Qdrant Documentation:** [https://qdrant.tech/documentation/](https://qdrant.tech/documentation/)',
            '- **Qdrant Documentation:** [https://qdrant.tech/documentation/](https://qdrant.tech/documentation/)\n- **Qdrant Python Client:** [https://github.com/qdrant/qdrant-client](https://github.com/qdrant/qdrant-client)'
        )

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
        print("Updated markdown successfully.")

update_markdown('/home/thaipt/ai-chatbot/TiniX-AIGuru/Bai1/bai_1_qdrant_tutorial.md')
