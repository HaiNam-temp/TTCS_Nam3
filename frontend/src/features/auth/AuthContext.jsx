import { createContext, useContext, useEffect, useMemo, useState } from "react";

import { loginApi, meApi, registerApi } from "../../shared/api/authApi";

const TOKEN_KEY = "pricecomp_token";
const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [token, setToken] = useState(localStorage.getItem(TOKEN_KEY));
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function bootstrap() {
      if (!token) {
        setLoading(false);
        return;
      }

      try {
        const profile = await meApi(token);
        setUser(profile);
      } catch {
        localStorage.removeItem(TOKEN_KEY);
        setToken(null);
        setUser(null);
      } finally {
        setLoading(false);
      }
    }

    bootstrap();
  }, [token]);

  async function login(username, password) {
    const data = await loginApi(username, password);
    localStorage.setItem(TOKEN_KEY, data.access_token);
    setToken(data.access_token);
    const profile = await meApi(data.access_token);
    setUser(profile);
  }

  async function register(payload) {
    return registerApi(payload);
  }

  function logout() {
    localStorage.removeItem(TOKEN_KEY);
    setToken(null);
    setUser(null);
  }

  const value = useMemo(
    () => ({ token, user, loading, login, register, logout, isAuthenticated: Boolean(token) }),
    [token, user, loading]
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used inside AuthProvider");
  }
  return context;
}
