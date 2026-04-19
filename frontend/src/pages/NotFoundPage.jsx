import { Link } from "react-router-dom";

export function NotFoundPage() {
  return (
    <div className="screen-center">
      <div>
        <h2>404</h2>
        <p>Trang không tồn tại.</p>
        <Link to="/">Quay về trang chủ</Link>
      </div>
    </div>
  );
}
