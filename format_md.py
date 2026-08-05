import re

with open('bai_1_qdrant_tutorial.md', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Restructure the cover page elements
# Find "Đối tượng hướng tới"
match_target = re.search(r'## 1\. Đối tượng hướng tới\n(.*?)\n\n', text, re.DOTALL)
target_text = match_target.group(1) if match_target else ""

# Find "Mục tiêu và sản phẩm đầu ra"
match_goal = re.search(r'## 7\. Mục tiêu và sản phẩm đầu ra\n(.*?)\n\n> !\[Giao diện', text, re.DOTALL)
goal_text = match_goal.group(1) if match_goal else ""
if not goal_text:
    match_goal = re.search(r'## 7\. Mục tiêu và sản phẩm đầu ra\n(.*?)\n\n', text, re.DOTALL)
    goal_text = match_goal.group(1) if match_goal else ""

# Remove them from their original locations
text = re.sub(r'## 1\. Đối tượng hướng tới\n.*?\n\n', '', text, flags=re.DOTALL)
text = re.sub(r'## 7\. Mục tiêu và sản phẩm đầu ra\n.*?\n\n', '', text, flags=re.DOTALL)

# Insert them at the top as part of the cover page
cover_page = f"""# Xây dựng Search API với Qdrant: Retrieval, Top-k và Metadata Filtering trong RAG

## Bài viết này dành cho ai?
{target_text}

## Mục tiêu:
{goal_text}

---
"""

# Replace the original H1 title with cover page
text = re.sub(r'# Xây dựng Search API với Qdrant.*?\n\n', cover_page, text, count=1)

# Fix Glossary heading (no number)
text = text.replace('## 3. Bảng thuật ngữ', '## Bảng thuật ngữ {-}')

# Renumber sections
text = text.replace('## 4. Tổng quan', '## 1. Tổng quan')
text = text.replace('### 4.1.', '### 1.1.')
text = text.replace('### 4.2.', '### 1.2.')
text = text.replace('### 4.3.', '### 1.3.')

text = text.replace('## 5. Kiến trúc', '## 2. Kiến trúc')
text = text.replace('### 5.1.', '### 2.1.')
text = text.replace('### 5.2.', '### 2.2.')
text = text.replace('### 5.3.', '### 2.3.')
text = text.replace('### 5.4.', '### 2.4.')

text = text.replace('## 6. So sánh', '## 3. So sánh')

text = text.replace('## 8. Hướng dẫn', '## 4. Hướng dẫn')
text = text.replace('### 8.1.', '### 4.1.')
text = text.replace('### 8.2.', '### 4.2.')

text = text.replace('## 9. Thực hành', '## 5. Thực hành')
text = text.replace('### Bước 9.1:', '### 5.1. Khởi tạo Qdrant Client và tạo Collection')
text = text.replace('### Bước 9.2:', '### 5.2. Biến đổi dữ liệu và insert vào Qdrant')
text = text.replace('### Bước 9.3:', '### 5.3. Viết API Search với Metadata Filter')

text = text.replace('## 10. Phân tích', '## 6. Phân tích')
text = text.replace('## 11. Vận hành', '## 7. Vận hành')
text = text.replace('## 12. Tổng kết', '## 8. Tổng kết')

with open('bai_1_qdrant_tutorial.md', 'w', encoding='utf-8') as f:
    f.write(text)

print("Markdown formatted")
