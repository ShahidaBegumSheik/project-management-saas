import { Navigate, Outlet } from "react-router-dom";
import Loader from "../components/Loader";
import { useAuth } from "../contexts/AuthContext";

export default function RequireRole({ role }) {
  const { loading, user } = useAuth();

  if (loading) return <Loader label="Checking permissions..." />;
  if (!user) return <Navigate to="/login" replace />;
  if (user.role !== role) {
    return <Navigate to={user.role === "admin" ? "/admin" : "/app"} replace />;
  }

  return <Outlet />;
}
