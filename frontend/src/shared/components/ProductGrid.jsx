import { ProductCard } from "./ProductCard";

export function ProductGrid({ items, emptyText = "Chưa có sản phẩm phù hợp." }) {
  if (!items?.length) {
    return <p className="empty-state">{emptyText}</p>;
  }

  return (
    <div className="card-grid product-grid">
      {items.map((item) => (
        <ProductCard key={item.id} item={item} />
      ))}
    </div>
  );
}
