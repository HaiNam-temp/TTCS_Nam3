from pathlib import Path
from typing import Dict, List
import importlib.util

from logger_config import get_logger

logger = get_logger(__name__)


def _load_module(module_name: str):
    crawler_path = Path(__file__).resolve().parents[1] / "Crawl_Data" / f"{module_name}.py"
    spec = importlib.util.spec_from_file_location(module_name, crawler_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load crawler module: {module_name}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def crawl_tiki(query: str) -> List[Dict]:
    logger.info("[providers.py][crawl_tiki] Start business=crawl tiki query=%s", query)
    try:
        module = _load_module("crawl_tiki_product")
        result = module.crawl_tiki_product(query)
        logger.info("[providers.py][crawl_tiki] End status=success count=%s", len(result or []))
        return result
    except Exception:
        logger.exception("[providers.py][crawl_tiki] End status=error query=%s", query)
        raise


def crawl_lazada(query: str) -> List[Dict]:
    logger.info("[providers.py][crawl_lazada] Start business=crawl lazada query=%s", query)
    try:
        module = _load_module("lazada_crawler_complete")
        crawler = module.LazadaCrawler()
        result = crawler.crawl_lazada_products(query)
        logger.info("[providers.py][crawl_lazada] End status=success count=%s", len(result or []))
        return result
    except Exception:
        logger.exception("[providers.py][crawl_lazada] End status=error query=%s", query)
        raise


def crawl_cellphones(query: str) -> List[Dict]:
    logger.info("[providers.py][crawl_cellphones] Start business=crawl cellphones query=%s", query)
    try:
        module = _load_module("scrape_cellphones_playwright")
        result = module.scrape_cellphones_products(query)
        logger.info("[providers.py][crawl_cellphones] End status=success count=%s", len(result or []))
        return result
    except Exception:
        logger.exception("[providers.py][crawl_cellphones] End status=error query=%s", query)
        raise


def crawl_dienthoaivui(query: str) -> List[Dict]:
    logger.info("[providers.py][crawl_dienthoaivui] Start business=crawl dienthoaivui query=%s", query)
    try:
        module = _load_module("scrape_dienthoaivui_playwright_search")
        result = module.scrape_dienthoaivui_products(query)
        logger.info("[providers.py][crawl_dienthoaivui] End status=success count=%s", len(result or []))
        return result
    except Exception:
        logger.exception("[providers.py][crawl_dienthoaivui] End status=error query=%s", query)
        raise
