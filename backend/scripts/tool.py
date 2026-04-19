from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, SystemMessagePromptTemplate, PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_chroma import Chroma
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_classic.callbacks.base import BaseCallbackHandler

from operator import itemgetter
import json
from typing import List, Dict
import requests
import re
from datetime import datetime
import dotenv
import os
dotenv.load_dotenv()
from logger_config import get_logger
logger = get_logger(__name__)
# Initialize ChatOpenAI

# Initialize vector database for product data
PRODUCTS_CHROMA_PATH = "chroma_data/"

# Initialize embeddings with explicit API key
_vector_db = None
_embeddings = None
_chat_model = None

class StreamingCallbackHandler(BaseCallbackHandler):
    def on_llm_new_token(self, token: str, **kwargs):
        """In ra từng token khi model stream"""
        print(token, end="", flush=True)
# Initialize vector database
def get_embeddings():
    global _embeddings
    if _embeddings is None:
        _embeddings = OpenAIEmbeddings(
            openai_api_key=os.getenv("OPENAI_API_KEY"),
            model="text-embedding-ada-002"
        )
    return _embeddings

def get_vector_db():
    global _vector_db
    if _vector_db is None:
        embeddings = get_embeddings()
        _vector_db = Chroma(
            persist_directory=PRODUCTS_CHROMA_PATH,
            embedding_function=embeddings
        )
    return _vector_db

def get_chat_model():
    global _chat_model
    if _chat_model is None:
        _chat_model = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0,
            streaming=True,
            callbacks=[StreamingCallbackHandler()]
        )
    return _chat_model
# import split functions from their new modules
from create_chain_with_template import create_chain_with_template
from backend.Crawl_Data.crawl_tiki_product import crawl_tiki_product
# The scrapers expose functions named with plural `_products` (they return lists).
# Import the correct function names to avoid ImportError at startup.
from backend.Crawl_Data.scrape_cellphones_playwright import scrape_cellphones_products
from backend.Crawl_Data.scrape_dienthoaivui_playwright_search import scrape_dienthoaivui_products

product_search_template = """
Bạn là Sophie, trợ lý mua sắm chuyên phân tích sản phẩm.
Nhiệm vụ: Xem xét {context}, phân tích ngầm (Giá, Rating, Người bán) và đề xuất 15 sản phẩm hàng đầu.
Nếu không tìm thấy sản phẩm phù hợp, hãy trả lời: "Tôi sẽ tìm kiếm sản phẩm này trên các sàn thương mại điện tử."
"""

product_search_chain = create_chain_with_template(product_search_template)
price_comparison_template = """
Chào bạn, tôi là Sophie, chuyên gia phân tích dữ liệu mua sắm của bạn đây.

Tôi đã ghi nhận vai trò và yêu cầu phân tích. Đặc biệt, tôi hiểu rằng bạn muốn tôi tập trung chính vào yếu tố Giá cả và trình bày thông tin một cách ngắn gọn, súc tích hơn so với mẫu chi tiết ban đầu. Các yếu tố như rating, người bán và số lượng bán sẽ được dùng làm thông tin bổ sung.
💡 ĐỀ XUẤT CỦA SOPHIE (Tập trung vào Giá)
🥇 Lựa chọn TIẾT KIỆM (Rẻ nhất):

Sản phẩm: [Tên SP]

Giá: [Giá] VNĐ

Từ: [Tên người bán] (trên [Nền tảng])

Link: [URL]

Lưu ý: Đây là mức giá thấp nhất. Tuy nhiên, các chỉ số [rating/số lượng bán] đang ở mức [mô tả ngắn].

🥈 Lựa chọn CÂN BẰNG (Giá tốt + Uy tín):

Sản phẩm: [Tên SP]

Giá: [Giá] VNĐ

Thông tin: [X.X] Sao | Đã bán: [Số lượng]

Từ: [Tên người bán] (trên [Nền tảng])

Link: [URL]

Lý do ngắn gọn: Mức giá rất hợp lý so với số lượng bán và rating nhận được.

🥉 Lựa chọn PHỔ BIẾN (Bán chạy nhất):

Sản phẩm: [Tên SP]

Giá: [Giá] VNĐ

Thông tin: Đã bán: [Số lượng]

Từ: [Tên người bán] (trên [Nền tảng])

Link: [URL]

Lý do ngắn gọn: Ưu tiên hàng đầu nếu bạn cần sản phẩm đã được nhiều người tin dùng.
Tôi đã sẵn sàng! Bạn chỉ cần cung cấp cho tôi dữ liệu các sản phẩm (phần {context}) mà bạn muốn tôi phân tích nhé. Tôi sẽ đưa ra so sánh và đề xuất nhanh gọn ngay.
"""

price_comparison_chain = create_chain_with_template(price_comparison_template)

