import { Link, Outlet, useNavigate } from "react-router-dom";
import { clearAuth, getRole } from "../api/client";

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

export default function AppLayout() {
  const navigate = useNavigate();
  const role = getRole();

  function logout() {
    clearAuth();
    navigate("/login");
  }

  return (
    <div className="min-h-screen bg-slate-50">
      <header className="border-b bg-white">
        <div className="mx-auto flex max-w-6xl items-center justify-between px-4 py-4">
          <div>
            <h1 className="text-xl font-bold text-slate-900">Stripe Fast API</h1>
            <p className="text-sm text-slate-500">Project Management SaaS</p>
          </div>
          <div className="flex items-center gap-2">
            <NavLink to="/app/projects">Projects</NavLink>
            <NavLink to="/app/billing">Billing</NavLink>
            {role === "admin" && <NavLink to="/admin/users">Admin</NavLink>}
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
