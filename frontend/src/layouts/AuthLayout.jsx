import { Outlet } from "react-router-dom";


export default function AuthLayout() {
  return (
    <div className="grid min-h-screen lg:grid-cols-[1.2fr_0.8fr]">
      <div className="hidden bg-slate-950 px-10 py-14 text-white lg:block">
        <p className="text-xs font-semibold uppercase tracking-[0.3em] text-slate-400">
          Project Managment - SaaS
        </p>


        <div className="mt-12 max-w-xl">
          <h1 className="text-5xl font-bold leading-tight">
            User and Admin for Project management SaaS app.
          </h1>
          <p className="mt-6 text-lg text-slate-300">
            Application provides role-based dashboards, analytics charts, billing visibility, notifications,
            project activity, and collaboration.
          </p>


          <div className="mt-14 grid grid-cols-3 gap-6 text-sm text-slate-300">
            <div>
              <h3 className="font-semibold text-white">User Panel</h3>
              <p className="mt-2">Projects, teams, billing</p>
            </div>
            <div>
              <h3 className="font-semibold text-white">Admin Panel</h3>
              <p className="mt-2">Users, subscriptions, analytics</p>
            </div>
            <div>
              <h3 className="font-semibold text-white">Visual Dashboards</h3>
              <p className="mt-2">Tailwind + Recharts</p>
            </div>
          </div>
        </div>
      </div>


      <div className="flex items-center justify-center bg-slate-50 px-6 py-12">
        <Outlet />
      </div>
    </div>
  );
}