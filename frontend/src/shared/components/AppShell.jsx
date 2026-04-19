import { NavLink, useNavigate } from "react-router-dom";

import { useAuth } from "../../features/auth/AuthContext";

const navItems = [
  { to: "/", label: "Trang chủ" },
  { to: "/search", label: "Tìm kiếm" },
  { to: "/chat", label: "Trợ lý AI" },
  { to: "/settings", label: "Cài đặt" },
  { to: "/admin", label: "Quản trị" },
];

export function AppShell({ children }) {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  function onLogout() {
    logout();
    navigate("/login");
  }

  return (
    <div className="app-layout">
      <aside className="sidebar">
        <h1 className="brand">PriceComp</h1>
        <p className="brand-subtitle">So sánh giá thông minh</p>
        <nav className="nav-list">
          {navItems.map((item) => (
            <NavLink
              key={item.to}
              to={item.to}
              className={({ isActive }) => (isActive ? "nav-link active" : "nav-link")}
            >
              {item.label}
            </NavLink>
          ))}
        </nav>
        <div className="profile-panel">
          <p className="profile-name">{user?.username || "Khách"}</p>
          <p className="profile-role">{user?.is_admin ? "Quản trị viên" : "Người dùng"}</p>
          <button className="btn btn-danger" onClick={onLogout}>Đăng xuất</button>
        </div>
      </aside>
      <main className="content">{children}</main>
    </div>
  );
}
