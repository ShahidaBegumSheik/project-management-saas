import { Navigate, Route, Routes } from "react-router-dom";
import RequireAuth from "./guards/RequireAuth";
import RequireRole from "./guards/RequireRole";
import AuthLayout from "./layouts/AuthLayout";
import UserLayout from "./layouts/UserLayout";
import AdminLayout from "./layouts/AdminLayout";
import LoginPage from "./pages/auth/LoginPage";
import RegisterPage from "./pages/auth/RegisterPage";
import UserDashboard from "./pages/user/UserDashboard";
import ProjectsPage from "./pages/user/ProjectsPage";
import TeamsPage from "./pages/user/TeamsPage";
import BillingPage from "./pages/user/BillingPage";
import NotificationsPage from "./pages/user/NotificationsPage";
import AdminDashboard from "./pages/admin/AdminDashboard";
import AdminUsersPage from "./pages/admin/AdminUsersPage";
import AdminSubscriptionsPage from "./pages/admin/AdminSubscriptionsPage";
import AdminMappingPage from "./pages/admin/AdminMappingPage";
import AdminNotificationsPage from "./pages/admin/AdminNotificationsPage";

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<Navigate to="/login" replace />} />
      <Route element={<AuthLayout />}>
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />
      </Route>

      <Route element={<RequireAuth />}>
        <Route element={<RequireRole role="user" />}>
          <Route path="/app" element={<UserLayout />}>
            <Route index element={<UserDashboard />} />
            <Route path="projects" element={<ProjectsPage />} />
            <Route path="teams" element={<TeamsPage />} />
            <Route path="billing" element={<BillingPage />} />
            <Route path="notifications" element={<NotificationsPage />} />
          </Route>
        </Route>

        <Route element={<RequireRole role="admin" />}>
          <Route path="/admin" element={<AdminLayout />}>
            <Route index element={<AdminDashboard />} />
            <Route path="users" element={<AdminUsersPage />} />
            <Route path="subscriptions" element={<AdminSubscriptionsPage />} />
            <Route path="mapping" element={<AdminMappingPage />} />
            <Route path="notifications" element={<AdminNotificationsPage />} />
          </Route>
        </Route>
      </Route>

      <Route path="*" element={<Navigate to="/login" replace />} />
    </Routes>
  );
}
