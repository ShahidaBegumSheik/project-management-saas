import { Navigate, Outlet } from "react-router-dom";
import { getRole, getToken } from "../api/client";

export default function RequireAdmin() {
  const token = getToken();
  const role = getRole();

  if (!token) {
    return <Navigate to="/login" replace />;
  }

  return role === "admin" ? <Outlet /> : <Navigate to="/app/projects" replace />;
}
