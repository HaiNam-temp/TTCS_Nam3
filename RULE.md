# 🧩 RULE.md — Quy tắc và Kiến trúc Code

## 1. Tổng quan cấu trúc dự án

```
app/
├── apis/          # Khai báo các endpoint (router)
├── core/          # Cấu hình chung, constant, middleware, bảo mật, logging, ...
├── db/            # Cấu hình và khởi tạo database
│   └── database.py
├── model/         # Định nghĩa các entity (ORM models)
│   └── product.py
├── repositories/  # Xử lý truy vấn cơ sở dữ liệu
├── schemas/       # Định nghĩa request/response (Pydantic models)
├── services/      # Chứa logic nghiệp vụ
└── utils/         # Hàm tiện ích, helper chung
```

---

## 2. Quy tắc phân tầng

### 2.1. Tầng Schemas
- **Thư mục:** `app/schemas`
- **Mục đích:** Định nghĩa request, response, và data validation.
- **Dùng:** `Pydantic` để kiểm tra dữ liệu đầu vào và định nghĩa cấu trúc dữ liệu trả về.
- **Quy tắc đặt tên:**
  - Request: `SomethingRequest`
  - Response: `SomethingResponse`
  - Schema chung: `SomethingSchema`

**Ví dụ:**
```python
from pydantic import BaseModel

class ProductRequest(BaseModel):
    name: str
    price: float

class ProductResponse(BaseModel):
    id: int
    name: str
    price: float
```

---

### 2.2. Tầng APIs
- **Thư mục:** `app/apis`
- **Mục đích:** Định nghĩa các endpoint RESTful và ánh xạ đến service tương ứng.
- **Không viết logic nghiệp vụ hay truy vấn database tại đây.**
- **Chỉ gọi sang tầng services.**
- **Quy tắc đặt tên:**
  - File: `ten_module_api.py`
  - Route: snake_case

**Ví dụ:**
```python
from fastapi import APIRouter, Depends
from app.schemas.product_schema import ProductRequest, ProductResponse
from app.services.product_service import create_product_service

router = APIRouter(prefix="/product", tags=["Product"])

@router.post("/create", response_model=ProductResponse)
def create_product(request: ProductRequest):
    return create_product_service(request)
```

---

### 2.3. Tầng Services
- **Thư mục:** `app/services`
- **Mục đích:** Xử lý logic nghiệp vụ (business logic).
- **Gọi đến repository để truy xuất dữ liệu.**
- **Không chứa logic của API hay chi tiết DB.**
- **Quy tắc đặt tên:**
  - File: `ten_module_service.py`
  - Hàm: snake_case

**Ví dụ:**
```python
from app.repositories.product_repository import insert_product
from app.schemas.product_schema import ProductRequest, ProductResponse

def create_product_service(request: ProductRequest) -> ProductResponse:
    product = insert_product(request)
    return ProductResponse(**product.__dict__)
```

---

### 2.4. Tầng Repositories
- **Thư mục:** `app/repositories`
- **Mục đích:** Thực hiện các thao tác truy vấn cơ sở dữ liệu (CRUD).
- **Không chứa logic nghiệp vụ.**
- **Là tầng duy nhất tương tác với ORM hoặc raw SQL.**
- **Quy tắc đặt tên:**
  - File: `ten_module_repository.py`
  - Hàm: bắt đầu bằng `get_`, `insert_`, `update_`, `delete_`

**Ví dụ:**
```python
from app.model.product import Product
from app.db.database import SessionLocal

db = SessionLocal()

def insert_product(request):
    new_product = Product(name=request.name, price=request.price)
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product
```

---

### 2.5. Tầng Model
- **Thư mục:** `app/model`
- **Mục đích:** Định nghĩa các bảng trong cơ sở dữ liệu bằng ORM (SQLAlchemy).
- **Không chứa logic nghiệp vụ hay hàm xử lý.**
- **Quy tắc đặt tên class:** PascalCase

**Ví dụ:**
```python
from sqlalchemy import Column, Integer, String, Float
from app.db.database import Base

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
```

---

## 3. Quy tắc đặt tên hàm và biến
| Loại | Quy tắc | Ví dụ |
|------|----------|--------|
| Hàm | snake_case | get_product_by_id() |
| Biến | snake_case | product_name, user_id |
| Class | PascalCase | ProductService, UserSchema |
| File | snake_case | product_repository.py |
| Folder | snake_case | product_images |

---

## 4. Nguyên tắc khác
- ❌ Không import chéo giữa các tầng (ví dụ `api` không import từ `repository`).
- ✅ Dòng chảy chuẩn: **API → Service → Repository → Model**
- 🔹 Validate dữ liệu bằng `schemas` trước khi xử lý.
- 🔹 Tránh lặp code — dùng `utils` cho helper dùng chung.

---

## 5. Ví dụ luồng xử lý đầy đủ
```
POST /product/create
      ↓
apis/product_api.py → services/product_service.py → repositories/product_repository.py → model/product.py
```
## Nơi code 
code trong ./app và code đầy đủ theo luồng api , service , repository, model, schemas
