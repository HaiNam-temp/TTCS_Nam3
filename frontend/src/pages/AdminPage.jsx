import { useEffect, useState } from "react";

import { useAuth } from "../features/auth/AuthContext";
import { crawlProductsApi, deleteUserApi, getStatsApi, getUsersApi } from "../shared/api/adminApi";
import { AppShell } from "../shared/components/AppShell";

export function AdminPage() {
  const { token, user } = useAuth();
  const [stats, setStats] = useState(null);
  const [users, setUsers] = useState([]);
  const [query, setQuery] = useState("iphone 15");
  const [crawlResult, setCrawlResult] = useState(null);
  const [error, setError] = useState("");

  useEffect(() => {
    if (!user?.is_admin) {
      return;
    }
    loadData();
  }, [user]);

  async function loadData() {
    try {
      const [statsData, usersData] = await Promise.all([getStatsApi(token), getUsersApi(token)]);
      setStats(statsData);
      setUsers(usersData || []);
    } catch (err) {
      setError(err.message || "Tải dữ liệu quản trị thất bại");
    }
  }

  async function onDeleteUser(userId) {
    if (userId === user?.id) {
      return;
    }
    await deleteUserApi(token, userId);
    await loadData();
  }

  async function onCrawlSubmit(event) {
    event.preventDefault();
    setError("");
    try {
      const result = await crawlProductsApi(token, query, 20);
      setCrawlResult(result);
    } catch (err) {
      setError(err.message || "Crawl thất bại");
    }
  }

  if (!user?.is_admin) {
    return (
      <AppShell>
        <h2>Quản trị</h2>
        <p>Bạn không có quyền truy cập trang này.</p>
      </AppShell>
    );
  }

  return (
    <AppShell>
      <h2>Bảng điều khiển quản trị</h2>
      {error ? <p className="text-error">{error}</p> : null}

      <div className="card-grid">
        <article className="stat-card">
          <h3>Người dùng</h3>
          <p>{stats?.total_users ?? "-"}</p>
        </article>
        <article className="stat-card">
          <h3>Hội thoại</h3>
          <p>{stats?.total_conversations ?? "-"}</p>
        </article>
        <article className="stat-card">
          <h3>Tin nhắn</h3>
          <p>{stats?.total_messages ?? "-"}</p>
        </article>
        <article className="stat-card">
          <h3>Nền tảng</h3>
          <p>{stats?.total_platforms ?? "-"}</p>
        </article>
      </div>

      <section className="panel">
        <h3>Crawl sản phẩm theo lô</h3>
        <form className="inline-form" onSubmit={onCrawlSubmit}>
          <input value={query} onChange={(event) => setQuery(event.target.value)} />
          <button className="btn" type="submit">Chạy crawl</button>
        </form>
        {crawlResult ? (
          <div className="crawl-result">
            <p>Tổng sản phẩm thu thập: {crawlResult.total_products}</p>
            <p>Sản phẩm đã lưu mới: {crawlResult.inserted_products}</p>
            <p>Thời gian xử lý: {crawlResult.elapsed_seconds}s</p>
          </div>
        ) : null}
      </section>

      <section className="panel">
        <h3>Quản lý người dùng</h3>
        <div className="user-list">
          {users.map((item) => (
            <div key={item.id} className="user-row">
              <div>
                <strong>{item.username}</strong>
                <p>{item.email}</p>
              </div>
              <button className="btn btn-danger" onClick={() => onDeleteUser(item.id)} disabled={item.id === user.id}>
                Xóa
              </button>
            </div>
          ))}
        </div>
      </section>
    </AppShell>
  );
}
