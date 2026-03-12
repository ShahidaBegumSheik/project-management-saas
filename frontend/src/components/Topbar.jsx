import { Bell } from "lucide-react";
import Button from "./Button";

export default function Topbar({ title, subtitle, unreadCount = 0, onLogout, userEmail }) {
  return (
    <div className="mb-6 flex flex-col gap-4 rounded-3xl border border-slate-200 bg-white p-5 shadow-soft sm:flex-row sm:items-center sm:justify-between">
      <div>
        <h2 className="text-2xl font-semibold text-slate-900">{title}</h2>
        <p className="mt-1 text-sm text-slate-500">{subtitle}</p>
      </div>
      <div className="flex items-center gap-3">
        <div className="flex items-center gap-2 rounded-2xl bg-slate-100 px-3 py-2 text-sm text-slate-600">
          <Bell className="h-4 w-4" />
          <span>{unreadCount} unread</span>
        </div>
        <div className="rounded-2xl border border-slate-200 px-4 py-2 text-sm text-slate-600">{userEmail}</div>
        <Button variant="secondary" onClick={onLogout}>Logout</Button>
      </div>
    </div>
  );
}
