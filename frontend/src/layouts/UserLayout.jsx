import { BarChart3, Bell, BriefcaseBusiness, CreditCard, LayoutDashboard, Users } from "lucide-react";
import { Outlet, useLocation } from "react-router-dom";
import Sidebar from "../components/Sidebar";
import Topbar from "../components/Topbar";
import { useAuth } from "../contexts/AuthContext";
import useUnreadNotifications from "../utils/useUnreadNotifications";

const navItems = [
  { to: "/app", label: "Dashboard", icon: LayoutDashboard, end: true },
  { to: "/app/projects", label: "Projects", icon: BriefcaseBusiness },
  { to: "/app/teams", label: "Teams", icon: Users },
  { to: "/app/billing", label: "Billing", icon: CreditCard },
  { to: "/app/notifications", label: "Notifications", icon: Bell },
  { to: "/app", label: "Analytics", icon: BarChart3, end: true },
];

const headerMap = {
  "/app": ["User Panel", "Overview of projects, billing, teams, and recent platform activity."],
  "/app/projects": ["Projects", "Create and manage projects, and inspect their activity timeline."],
  "/app/teams": ["Teams", "Create teams for projects, invite collaborators, and review membership."],
  "/app/billing": ["Billing", "Upgrade to Pro, track billing status, and cancel if needed."],
  "/app/notifications": ["Notifications", "Read platform alerts and manage unread items."],
};

export default function UserLayout() {
  const { user, logout } = useAuth();
  const location = useLocation();
  const [title, subtitle] = headerMap[location.pathname] || headerMap["/app"];
  const unreadCount = useUnreadNotifications();

  return (
    <div className="flex min-h-screen bg-slate-50">
      <Sidebar title="User Panel" subtitle="Projects and collaboration" items={navItems} />
      <main className="min-w-0 flex-1 p-4 sm:p-6 lg:p-8">
        <Topbar title={title} subtitle={subtitle} onLogout={logout} unreadCount={unreadCount} userEmail={user?.email} />
        <Outlet />
      </main>
    </div>
  );
}
