# Recommend System Documentation

Tài liệu này mô tả module content-based recommendation trong thư mục recommend_system.

## 1. Mục tiêu

- Cung cấp bộ hàm recommend theo hướng clean code.
- Cấu trúc đơn giản, gọi trực tiếp từ service backend.
- Dùng logging rõ nghĩa với log.info và log.error.

## 2. Kiến trúc tổng quan

Luồng xử lý chính:

1. Nhận danh sách item và lịch sử tương tác của user.
2. Trích xuất vector đặc trưng item bằng TF-IDF.
3. Xây user profile vector từ interaction có trọng số.
4. Tính điểm tương đồng cosine giữa user và item.
5. Lọc item đã xem, áp ngưỡng điểm, lấy top-k.
6. Trả kết quả recommendation đã sắp xếp.

## 3. Các thành phần chính

### 3.1 Domain Models

- File: models.py
- Vai trò: Định nghĩa dữ liệu đầu vào/đầu ra của thuật toán.

Các model:

- ItemContent
  - Input item content cho feature extraction.
  - Trường chính: item_id, title, description, categories, tags, metadata.
- UserInteraction
  - Input lịch sử user.
  - Trường chính: item_id, weight, timestamp.
- RecommendationResult
  - Output cuối cùng của pipeline.
  - Trường chính: item_id, score, reason.

### 3.2 Feature Extraction

- File: tfidf_feature_extractor.py
- Class chính: TfidfFeatureExtractor
- Vai trò: biến đổi item text thành vector TF-IDF chuẩn hóa.

Hàm chính:

- fit_transform(items)
  - Input: list[ItemContent]
  - Output: dict[str, SparseVector]
  - Hành vi:
    - Tokenize dữ liệu text item.
    - Tính document frequency, idf.
    - Tính tf-idf từng item.
    - Normalize vector theo L2.

### 3.3 User Profile Builder

- File: user_profile_builder.py
- Class chính: WeightedUserProfileBuilder
- Vai trò: gom các vector item user đã tương tác thành một user vector.

Hàm chính:

- build_profile(interactions, item_vectors)
  - Input:
    - interactions: list[UserInteraction]
    - item_vectors: dict[str, SparseVector]
  - Output: SparseVector
  - Hành vi:
    - Cộng có trọng số các item vector.
    - Chia trung bình theo tổng weight.
    - Normalize để dùng cho cosine scoring.

### 3.4 Similarity Scoring

- File: cosine_scorer.py
- Class chính: CosineSimilarityScorer
- Vai trò: tính điểm tương đồng user-item.

Hàm chính:

- score(user_vector, item_vectors)
  - Input:
    - user_vector: SparseVector
    - item_vectors: dict[str, SparseVector]
  - Output: dict[str, float]
  - Hành vi:
    - Tính cosine similarity cho từng item.

### 3.5 Candidate Filtering and Ranking

- File: candidate_filter.py
- Class chính: DefaultCandidateFilter
- Vai trò: loại item đã xem và trả top-k item có điểm cao nhất.

Hàm chính:

- select(scores, interactions, top_k, min_score)
  - Input:
    - scores: dict[item_id, score]
    - interactions: list[UserInteraction]
    - top_k: int
    - min_score: float
  - Output: list[RecommendationResult]
  - Hành vi:
    - Loại item đã có trong history.
    - Lọc theo min_score.
    - Sort giảm dần theo score.
    - Cắt top_k.

### 3.6 Service Orchestration

- File: recommendation_service.py
- Class chính: ContentBasedRecommendationService
- Vai trò: điều phối toàn bộ pipeline theo thứ tự xử lý chuẩn.

Hàm chính:

- recommend(items, interactions, top_k=10, min_score=0.0)
  - Input:
    - items: list[ItemContent]
    - interactions: list[UserInteraction]
    - top_k: số lượng gợi ý
    - min_score: ngưỡng điểm tối thiểu
  - Output:
    - list[RecommendationResult], đã được rank theo score giảm dần

## 4. Utility files

- text_preprocessor.py
  - normalize_text(value): chuẩn hóa text.
  - tokenize(value): tách token alphanumeric.

- vector_utils.py
  - l2_norm(vector): tính chuẩn L2.
  - normalize(vector): chuẩn hóa vector.
  - cosine_similarity(left, right): tính cosine.
  - add_scaled(target, source, scale): cộng vector có trọng số.

- types.py
  - SparseVector: kiểu dữ liệu vector thưa dùng chung toàn module.

- __init__.py
  - Export các class/model chính để import gọn.

- example_usage.py
  - Ví dụ chạy độc lập module recommend.

## 5. Logging convention

Module sử dụng logger_config.get_logger và log theo format:

- log.info
  - Start/Done của mỗi bước pipeline.
  - Quy mô dữ liệu (số item, số interaction, số kết quả).
- log.error
  - Input invalid.
  - Trường hợp không build được profile.
  - Lỗi tổng trong service.recommend kèm exc_info=True.

## 6. Cách dùng nhanh

Ví dụ tối giản:

1. Tạo items dạng ItemContent.
2. Tạo interactions dạng UserInteraction.
3. Khởi tạo ContentBasedRecommendationService.
4. Gọi recommend(items, interactions, top_k).
5. Nhận list RecommendationResult.

Tham khảo file example_usage.py để copy nhanh vào service/backend hiện tại.
