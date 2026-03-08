import { Navigate, Route, Routes } from "react-router-dom";
import RequireAuth from "./guards/RequireAuth";
import RequireAdmin from "./guards/RequireAdmin";
import AppLayout from "./layouts/AppLayout";
import AdminLayout from "./layouts/AdminLayout";
import Login from "./pages/Login";
import Register from "./pages/Register";
import Projects from "./pages/Projects";
import Billing from "./pages/Billing";
import AdminUsers from "./pages/AdminUsers";
import AdminSubscriptions from "./pages/AdminSubscriptions";
import AdminMapping from "./pages/AdminMapping";
import MockCheckout from "./pages/MockCheckout";
import MockPortal from "./pages/MockPortal";

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<Navigate to="/login" replace />} />
      <Route path="/login" element={<Login />} />
      <Route path="/register" element={<Register />} />
      <Route path="/mock-checkout" element={<MockCheckout />} />
      <Route path="/mock-portal" element={<MockPortal />} />

      <Route element={<RequireAuth />}>
        <Route path="/app" element={<AppLayout />}>
          <Route index element={<Navigate to="/app/projects" replace />} />
          <Route path="projects" element={<Projects />} />
          <Route path="billing" element={<Billing />} />
        </Route>
      </Route>

      <Route element={<RequireAdmin />}>
        <Route path="/admin" element={<AdminLayout />}>
          <Route index element={<Navigate to="/admin/users" replace />} />
          <Route path="users" element={<AdminUsers />} />
          <Route path="subscriptions" element={<AdminSubscriptions />} />
          <Route path="mapping" element={<AdminMapping />} />
        </Route>
      </Route>

      <Route path="*" element={<div className="p-8 text-center text-lg">Not found</div>} />
    </Routes>
  );
}
