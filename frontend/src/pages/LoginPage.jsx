import { useState } from "react";
import { Navigate } from "react-router-dom";

import { useAuth } from "../features/auth/AuthContext";

export function LoginPage() {
  const { isAuthenticated, login, register } = useAuth();
  const [mode, setMode] = useState("login");
  const [error, setError] = useState("");
  const [message, setMessage] = useState("");
  const [busy, setBusy] = useState(false);

  async function onLoginSubmit(event) {
    event.preventDefault();
    setBusy(true);
    setError("");
    setMessage("");

    const form = new FormData(event.currentTarget);
    try {
      await login(form.get("username"), form.get("password"));
    } catch (err) {
      setError(err.message || "Đăng nhập thất bại");
    } finally {
      setBusy(false);
    }
  }

  async function onRegisterSubmit(event) {
    event.preventDefault();
    setBusy(true);
    setError("");
    setMessage("");

    const form = new FormData(event.currentTarget);
    const password = form.get("password");
    const confirm = form.get("confirm");
    if (password !== confirm) {
      setError("Mật khẩu xác nhận không khớp");
      setBusy(false);
      return;
    }

    try {
      await register({
        username: form.get("username"),
        email: form.get("email"),
        password,
        full_name: form.get("full_name") || null,
      });
      setMessage("Đăng ký thành công, vui lòng đăng nhập");
      setMode("login");
    } catch (err) {
      setError(err.message || "Đăng ký thất bại");
    } finally {
      setBusy(false);
    }
  }

  if (isAuthenticated) {
    return <Navigate to="/" replace />;
  }

  return (
    <div className="auth-wrap">
      <div className="auth-card">
        <h2>Cổng PriceComp</h2>
        <p>Đăng nhập để dùng tìm kiếm, chat và quản trị dữ liệu sản phẩm.</p>

        <div className="auth-tabs">
          <button
            className={mode === "login" ? "tab active" : "tab"}
            onClick={() => setMode("login")}
          >
            Đăng nhập
          </button>
          <button
            className={mode === "register" ? "tab active" : "tab"}
            onClick={() => setMode("register")}
          >
            Đăng ký
          </button>
        </div>

        {mode === "login" ? (
          <form className="form" onSubmit={onLoginSubmit}>
            <input name="username" placeholder="Tên đăng nhập" required />
            <input name="password" type="password" placeholder="Mật khẩu" required />
            <button className="btn" disabled={busy} type="submit">
              {busy ? "Đang xử lý..." : "Đăng nhập"}
            </button>
          </form>
        ) : (
          <form className="form" onSubmit={onRegisterSubmit}>
            <input name="username" placeholder="Tên đăng nhập" required />
            <input name="email" type="email" placeholder="Email" required />
            <input name="full_name" placeholder="Họ và tên (không bắt buộc)" />
            <input name="password" type="password" placeholder="Mật khẩu" required />
            <input name="confirm" type="password" placeholder="Xác nhận mật khẩu" required />
            <button className="btn" disabled={busy} type="submit">
              {busy ? "Đang xử lý..." : "Đăng ký"}
            </button>
          </form>
        )}

        {error ? <p className="text-error">{error}</p> : null}
        {message ? <p className="text-success">{message}</p> : null}
      </div>
    </div>
  );
}
