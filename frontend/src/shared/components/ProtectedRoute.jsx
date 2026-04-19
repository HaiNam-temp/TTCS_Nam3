import { Navigate } from "react-router-dom";

import { useAuth } from "../../features/auth/AuthContext";

export function ProtectedRoute({ children, adminOnly = false }) {
  const { isAuthenticated, user, loading } = useAuth();

  if (loading) {
    return <div className="screen-center">Dang tai...</div>;
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  if (adminOnly && !user?.is_admin) {
    return <Navigate to="/" replace />;
  }

  return children;
}
