import { AppShell } from "../shared/components/AppShell";
import { useAuth } from "../features/auth/AuthContext";

export function SettingsPage() {
  const { user } = useAuth();

  return (
    <AppShell>
      <h2>Cài đặt</h2>
      <section className="panel">
        <h3>Hồ sơ</h3>
        <p>Tên đăng nhập: {user?.username}</p>
        <p>Email: {user?.email}</p>
        <p>Vai trò: {user?.is_admin ? "Quản trị viên" : "Người dùng"}</p>
      </section>

      <section className="panel">
        <h3>Mật khẩu</h3>
        <p>Backend hiện tại chưa mở endpoint đổi mật khẩu. Khi bạn bổ sung endpoint, trang này đã sẵn sàng để kết nối API.</p>
      </section>
    </AppShell>
  );
}
