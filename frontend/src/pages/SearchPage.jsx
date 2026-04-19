import { useState } from "react";

import { searchProductsApi } from "../shared/api/productApi";
import { AppShell } from "../shared/components/AppShell";
import { PageSectionHeader } from "../shared/components/PageSectionHeader";
import { ProductGrid } from "../shared/components/ProductGrid";

export function SearchPage() {
  const [query, setQuery] = useState("");
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function onSubmit(event) {
    event.preventDefault();
    if (!query.trim()) {
      return;
    }

    setLoading(true);
    setError("");
    try {
      const products = await searchProductsApi(query.trim());
      setItems(products || []);
    } catch (err) {
      setError(err.message || "Tìm kiếm thất bại");
    } finally {
      setLoading(false);
    }
  }

  return (
    <AppShell>
      <PageSectionHeader
        title="Tra cứu sản phẩm"
        subtitle="Tìm theo tên hoặc đường dẫn sản phẩm đã lưu trong cơ sở dữ liệu."
      />

      <form className="inline-form" onSubmit={onSubmit}>
        <input
          value={query}
          onChange={(event) => setQuery(event.target.value)}
          placeholder="Nhập từ khóa sản phẩm, ví dụ: iPhone 15"
        />
        <button className="btn" type="submit">Tìm kiếm</button>
      </form>

      {loading ? <p>Đang tìm kiếm...</p> : null}
      {error ? <p className="text-error">{error}</p> : null}

      {!loading ? <ProductGrid items={items} emptyText="Không tìm thấy sản phẩm phù hợp." /> : null}
    </AppShell>
  );
}
