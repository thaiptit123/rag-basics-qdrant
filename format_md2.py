import re

with open('bai_1_qdrant_tutorial.md', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Fix Title
text = text.replace('# Xây dựng Search API với Qdrant: Retrieval, Top-k và Metadata Filtering trong RAG', '# Retrieval, top-k và metadata filtering với Qdrant.')

# 2. Add Intro for RAG Basics
intro_text = """Trong các bài viết trước thuộc chuỗi **RAG Basics**, chúng ta đã nắm được tổng quan về hệ thống RAG và cách bóc tách, xử lý văn bản. Bước tiếp theo và cũng là "trái tim" của hệ thống truy xuất chính là Vector Database. Trong bài này, chúng ta sẽ cùng tìm hiểu Qdrant — một trong những cơ sở dữ liệu vector phổ biến nhất hiện nay, và thực hành xây dựng một API tìm kiếm văn bản đơn giản.

# Bài viết này dành cho ai? {-}"""
text = text.replace('# Bài viết này dành cho ai? {-}', intro_text)

# 3. Fix "RAG Advanced" to "RAG Basics"
text = text.replace('RAG Advanced', 'RAG Basics')

# 4. Fix Duplicate Headers
text = text.replace('## Khởi tạo Qdrant Client và tạo Collection Khởi tạo Qdrant Client và tạo Collection', '## Khởi tạo Qdrant Client và tạo collection')
text = text.replace('## Biến đổi dữ liệu và insert vào Qdrant Biến đổi dữ liệu và insert vào Qdrant', '## Biến đổi dữ liệu và insert vào Qdrant')
text = text.replace('## Viết API Search với Metadata Filter Viết API Search với Metadata Filter', '## Viết API search với metadata filter')

# 5. Fix Capitalization and dashes
text = text.replace('—', '—') # It is already an em-dash, but just to be sure.
text = text.replace(' - ', ' — ') # Replace en-dash with spaces to em-dash
text = text.replace('# Vận hành và xử lý sự cố (Troubleshooting & Production Checklist)', '# Vận hành và xử lý sự cố')

# 6. Outro - rewrite conclusion
old_outro = """Với Qdrant, chúng ta không chỉ có một cỗ máy "so khớp từ ngữ" mà là một hệ thống "hiểu ý nghĩa" và "tuân thủ luật lệ" (nhờ Payload Filter). RAG khi được xây trên nền tảng này sẽ hạn chế tối đa tình trạng "ảo giác".
Chào mừng bạn đến với kỹ thuật Reranking trong bài tiếp theo!"""
new_outro = """Với Qdrant, chúng ta không chỉ có một cỗ máy "so khớp từ ngữ" đơn thuần, mà là một hệ thống biết "hiểu ý nghĩa" văn bản và "tuân thủ luật lệ" thông qua Payload Filter. Khi kho dữ liệu ngày một lớn lên, sự kết hợp giữa Vector Search và Metadata Filtering chính là "chìa khoá" để chặn đứng hiện tượng "ảo giác" (hallucination) cho LLM.

Tuy nhiên, liệu 5 hoặc 10 kết quả trả về từ Qdrant đã là phiên bản hoàn hảo nhất để đưa cho LLM đọc chưa? Câu trả lời là chưa. Ở bài viết tiếp theo của chuỗi RAG Basics, chúng ta sẽ khám phá kỹ thuật **Reranking với Cross-Encoder** — "vũ khí bí mật" giúp chấm điểm và sắp xếp lại các kết quả này một lần nữa với độ chính xác kinh ngạc!"""
text = text.replace(old_outro, new_outro)

# 7. Add References
references = """
# Tài liệu tham khảo

1. [Qdrant Documentation](https://qdrant.tech/documentation/)
2. [Payload Filtering - Qdrant](https://qdrant.tech/documentation/concepts/filtering/)
3. [Mô hình tiếng Việt keepitreal/vietnamese-sbert](https://huggingface.co/keepitreal/vietnamese-sbert)
4. [Hướng dẫn Snapshot của Qdrant](https://qdrant.tech/documentation/manage-data/snapshots/)
"""
text = text.replace('COVERPAGEENDMARKER', 'COVERPAGEENDMARKER\n\n' + "> [!WARNING]\n> Dữ liệu pháp luật dùng trong bài chỉ mang tính chất minh hoạ thuật toán, không có giá trị tham khảo pháp lý.\n")
# Insert references before the author tag at the very end
if '*Tác giả:' in text:
    text = text.replace('*Tác giả:', references + '\n*Tác giả:')

# Write back
with open('bai_1_qdrant_tutorial.md', 'w', encoding='utf-8') as f:
    f.write(text)

print("Formatted MD successfully")
