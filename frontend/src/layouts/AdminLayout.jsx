import { Bell, CreditCard, LayoutDashboard, Send, Users } from "lucide-react";
import { Outlet, useLocation } from "react-router-dom";
import Sidebar from "../components/Sidebar";
import Topbar from "../components/Topbar";
import { useAuth } from "../contexts/AuthContext";
import useUnreadNotifications from "../utils/useUnreadNotifications";

const navItems = [
  { to: "/admin", label: "Dashboard", icon: LayoutDashboard, end: true },
  { to: "/admin/users", label: "Users", icon: Users },
  { to: "/admin/subscriptions", label: "Subscriptions", icon: CreditCard },
  { to: "/admin/mapping", label: "User Mapping", icon: Bell },
  { to: "/admin/notifications", label: "Send Alerts", icon: Send },
];

const headerMap = {
  "/admin": ["Admin Panel", "Monitor users, subscriptions, and platform analytics."],
  "/admin/users": ["Users", "Paginated visibility into all registered users."],
  "/admin/subscriptions": ["Subscriptions", "Review plan status and operational billing information."],
  "/admin/mapping": ["User ↔ Subscription Map", "Inspect each user alongside their current plan."],
  "/admin/notifications": ["System Notifications", "Send global or targeted system messages."],
};

export default function AdminLayout() {
  const { user, logout } = useAuth();
  const location = useLocation();
  const [title, subtitle] = headerMap[location.pathname] || headerMap["/admin"];
  const unreadCount = useUnreadNotifications();

  return (
    <div className="flex min-h-screen bg-slate-50">
      <Sidebar title="Admin Panel" subtitle="Operations and analytics" items={navItems} />
      <main className="min-w-0 flex-1 p-4 sm:p-6 lg:p-8">
        <Topbar title={title} subtitle={subtitle} onLogout={logout} unreadCount={unreadCount} userEmail={user?.email} />
        <Outlet />
      </main>
    </div>
  );
}
