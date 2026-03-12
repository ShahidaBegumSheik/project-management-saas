import { Navigate, Outlet, useLocation } from "react-router-dom";
import { useAuth } from "../contexts/AuthContext";
import Loader from "../components/Loader";

export default function RequireAuth() {
  const { loading, token } = useAuth();
  const location = useLocation();

  if (loading) return <Loader label="Checking your session..." />;
  if (!token) return <Navigate to="/login" replace state={{ from: location }} />;
  return <Outlet />;
}