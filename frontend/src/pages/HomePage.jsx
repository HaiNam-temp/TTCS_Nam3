import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

import { listNewestProductsApi } from "../shared/api/productApi";
import { AppShell } from "../shared/components/AppShell";
import { PageSectionHeader } from "../shared/components/PageSectionHeader";
import { ProductGrid } from "../shared/components/ProductGrid";

export function HomePage() {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    async function loadProducts() {
      setLoading(true);
      setError("");
      try {
        const result = await listNewestProductsApi(8);
        setProducts(result || []);
      } catch (err) {
        setError(err.message || "Không thể tải sản phẩm từ cơ sở dữ liệu.");
      } finally {
        setLoading(false);
      }
    }

    loadProducts();
  }, []);

  return (
    <AppShell>
      <section className="hero">
        <h2>Chào mừng đến với PriceComp</h2>
        <p>
          Tìm kiếm sản phẩm tốt với giá thấp nhất 
        </p>
      </section>

      <section className="card-grid">
        <Link to="/search" className="feature-card">
          <h3>Tìm sản phẩm</h3>
          <p>Tra cứu nhanh các sản phẩm theo từ khóa.</p>
        </Link>
        <Link to="/chat" className="feature-card">
          <h3>Trợ lý AI</h3>
          <p>Trợ giúp bạn tìm kiếm và so sánh sản phẩm một cách thông minh.</p>
        </Link>
        <Link to="/admin" className="feature-card">
          <h3>Bảng điều khiển quản trị</h3>
        </Link>
      </section>

      <section className="panel panel-products">
        <PageSectionHeader
          title="Danh sách sản phẩm mới nhất"
          subtitle="Danh sách các sản phẩm mới nhất với giá tốt"
          action={
            <Link className="btn btn-ghost" to="/search">
              Xem tất cả
            </Link>
          }
        />

        {loading ? <p>Đang tải sản phẩm...</p> : null}
        {error ? <p className="text-error">{error}</p> : null}
        {!loading && !error ? (
          <ProductGrid
            items={products}
            emptyText="Chưa có sản phẩm trong cơ sở dữ liệu. Bạn có thể vào trang Quản trị để chạy crawl."
          />
        ) : null}
      </section>
    </AppShell>
  );
}
