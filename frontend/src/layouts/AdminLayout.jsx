import { Link, Outlet, useNavigate } from "react-router-dom";
import { clearAuth } from "../api/client";

function NavLink({ to, children }) {
  return (
    <Link
      to={to}
      className="rounded-lg px-3 py-2 text-sm font-medium text-slate-700 hover:bg-slate-100"
    >
      {children}
    </Link>
  );
}

export default function AdminLayout() {
  const navigate = useNavigate();

  function logout() {
    clearAuth();
    navigate("/login");
  }

  return (
    <div className="min-h-screen bg-slate-50">
      <header className="border-b bg-white">
        <div className="mx-auto flex max-w-6xl items-center justify-between px-4 py-4">
          <div>
            <h1 className="text-xl font-bold text-slate-900">Admin Panel</h1>
            <p className="text-sm text-slate-500">Platform Monitoring</p>
          </div>
          <div className="flex items-center gap-2">
            <NavLink to="/admin/users">Users</NavLink>
            <NavLink to="/admin/subscriptions">Subscriptions</NavLink>
            <NavLink to="/admin/mapping">Mapping</NavLink>
            <NavLink to="/app/projects">Back to App</NavLink>
            <button
              onClick={logout}
              className="rounded-lg border px-3 py-2 text-sm font-medium text-slate-700 hover:bg-slate-50"
            >
              Logout
            </button>
          </div>
        </div>
      </header>

      <main className="mx-auto max-w-6xl px-4 py-8">
        <Outlet />
      </main>
    </div>
  );
}
