import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Callable, Dict, List, Tuple

from logger_config import get_logger

from backend.crawlers import crawl_cellphones, crawl_dienthoaivui, crawl_lazada, crawl_tiki
from backend.schemas import CrawlProductsResponse, CrawlSourceResult
from backend.services.product_service import ProductService

logger = get_logger(__name__)

CrawlerFn = Callable[[str], List[Dict]]


class CrawlService:
    def __init__(self, product_service: ProductService):
        self.product_service = product_service
        self._sources: List[Tuple[str, CrawlerFn]] = [
            ("tiki", crawl_tiki),
            ("lazada", crawl_lazada),
            ("cellphones", crawl_cellphones),
            ("dienthoaivui", crawl_dienthoaivui),
        ]

    def crawl_and_store(self, query: str, limit: int) -> CrawlProductsResponse:
        logger.info("[crawl_service.py][crawl_and_store] Start business=crawl and store query=%s", query)
        start = time.time()
        products: List[Dict] = []
        source_results: List[CrawlSourceResult] = []

        try:
            with ThreadPoolExecutor(max_workers=len(self._sources)) as executor:
                future_to_source = {
                    executor.submit(crawl_fn, query): source_name
                    for source_name, crawl_fn in self._sources
                }
                for future in as_completed(future_to_source):
                    source_name = future_to_source[future]
                    try:
                        source_products = future.result() or []
                        if limit > 0:
                            source_products = source_products[:limit]
                        products.extend(source_products)
                        source_results.append(CrawlSourceResult(source=source_name, count=len(source_products)))
                    except Exception as exc:
                        logger.exception(
                            "[crawl_service.py][crawl_and_store] Source failed source=%s", source_name
                        )
                        source_results.append(CrawlSourceResult(source=source_name, count=0, error=str(exc)))

            inserted = self.product_service.save_crawled_products(products)
            elapsed = round(time.time() - start, 2)
            logger.info(
                "[crawl_service.py][crawl_and_store] End status=success total_products=%s inserted=%s elapsed_seconds=%s",
                len(products),
                inserted,
                elapsed,
            )

            return CrawlProductsResponse(
                query=query,
                total_products=len(products),
                inserted_products=inserted,
                elapsed_seconds=elapsed,
                sources=source_results,
            )
        except Exception:
            logger.exception("[crawl_service.py][crawl_and_store] End status=error query=%s", query)
            raise
