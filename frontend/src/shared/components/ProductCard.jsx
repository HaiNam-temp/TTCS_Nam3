function formatPrice(value) {
  if (value === null || value === undefined || Number.isNaN(Number(value))) {
    return "Chưa có giá";
  }

  return new Intl.NumberFormat("vi-VN", {
    style: "currency",
    currency: "VND",
    maximumFractionDigits: 0,
  }).format(Number(value));
}

function formatRating(value) {
  if (value === null || value === undefined || Number.isNaN(Number(value))) {
    return "Chưa có";
  }

  return `${Number(value).toFixed(1)}/5`;
}

export function ProductCard({ item }) {
  return (
    <article className="product-card">
      <div className="product-card-image-wrap">
        {item.image ? (
          <img className="product-card-image" src={item.image} alt={item.name} loading="lazy" />
        ) : (
          <div className="product-card-image-fallback">Không có ảnh</div>
        )}
      </div>

      <h3 className="product-card-title">{item.name}</h3>
      <p className="product-card-price">{formatPrice(item.price)}</p>

      <div className="product-card-meta">
        <span>Đánh giá: {formatRating(item.rating)}</span>
        <span>Lượt review: {item.review_count ?? 0}</span>
      </div>

      <a href={item.url} target="_blank" rel="noreferrer" className="product-card-link">
        Xem chi tiết
      </a>
    </article>
  );
}
