import { useEffect, useMemo, useState } from "react";
import api from "../../api/client";
import Card from "../../components/Card";
import EmptyState from "../../components/EmptyState";
import Loader from "../../components/Loader";
import StatCard from "../../components/StatCard";
import { MiniBarChart, MiniPieChart } from "../../components/Charts";
import { useToast } from "../../contexts/ToastContext";
import { formatDate, getErrorMessage, titleCase } from "../../utils/formatters";

export default function UserDashboard() {
  const { push } = useToast();
  const [loading, setLoading] = useState(true);
  const [analytics, setAnalytics] = useState(null);
  const [projects, setProjects] = useState([]);
  const [subscription, setSubscription] = useState(null);

  useEffect(() => {
    async function load() {
      try {
        const [analyticsRes, projectsRes, billingRes] = await Promise.all([
          api.get("/analytics/owner"),
          api.get("/projects", { params: { page: 1, page_size: 20 } }),
          api.get("/billing/me"),
        ]);
        setAnalytics(analyticsRes.data);
        setProjects(projectsRes.data);
        setSubscription(billingRes.data);
      } catch (error) {
        push(getErrorMessage(error), "error");
      } finally {
        setLoading(false);
      }
    }
    load();
  }, [push]);

  const summaryData = useMemo(
    () => [
      { name: "Projects", value: analytics?.total_projects || 0 },
      { name: "Team Members", value: analytics?.team_members_count || 0 },
      { name: "Recent Activity", value: analytics?.recent_project_activity || 0 },
    ],
    [analytics]
  );

  const statusData = useMemo(
    () => [
      { name: subscription?.plan === "pro" ? "Pro" : "Free", value: 1 },
      { name: "Unread Notifications", value: analytics?.unread_notifications || 0 },
    ],
    [subscription, analytics]
  );

  if (loading) return <Loader label="Loading your dashboard..." />;

  return (
    <div className="space-y-6">
      <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
        <StatCard label="Total Projects" value={analytics?.total_projects || 0} hint="Free plan allows 3, Pro unlocks more." />
        <StatCard label="Subscription" value={titleCase(analytics?.active_subscription_status || subscription?.status || "free")} accent="emerald" />
        <StatCard label="Team Members" value={analytics?.team_members_count || 0} accent="amber" />
        <StatCard label="Unread Notifications" value={analytics?.unread_notifications || 0} accent="slate" />
      </div>

      <div className="grid gap-6 xl:grid-cols-[1.2fr_0.8fr]">
        <Card title="Project visibility" subtitle="The user panel clearly shows whether this account has projects or not.">
          {projects.length ? (
            <div className="space-y-3">
              {projects.map((project) => (
                <div key={project.id} className="flex items-center justify-between rounded-2xl border border-slate-200 px-4 py-3">
                  <div>
                    <p className="font-medium text-slate-900">{project.name}</p>
                    <p className="text-sm text-slate-500">{project.description || "No description"}</p>
                  </div>
                  <span className="text-sm text-slate-500">{formatDate(project.created_at)}</span>
                </div>
              ))}
            </div>
          ) : (
            <EmptyState title="No projects yet" message="This user currently has no projects. Create one from the Projects page to get started." />
          )}
        </Card>

        <Card title="Plan summary" subtitle="Quick visual view of plan and unread notification distribution.">
          <MiniPieChart data={statusData} />
        </Card>
      </div>

      <div className="grid gap-6 xl:grid-cols-2">
        <Card title="Activity metrics" subtitle="Recharts visualization for project, team, and recent activity counts.">
          <MiniBarChart data={summaryData} />
        </Card>
        <Card title="Current billing status" subtitle="Pulled directly from the billing API.">
          <div className="grid gap-4 sm:grid-cols-2">
            <div className="rounded-2xl bg-slate-50 p-4">
              <p className="text-sm text-slate-500">Plan</p>
              <p className="mt-2 text-xl font-semibold text-slate-900">{titleCase(subscription?.plan || "free")}</p>
            </div>
            <div className="rounded-2xl bg-slate-50 p-4">
              <p className="text-sm text-slate-500">Status</p>
              <p className="mt-2 text-xl font-semibold text-slate-900">{titleCase(subscription?.status || "active")}</p>
            </div>
            <div className="rounded-2xl bg-slate-50 p-4 sm:col-span-2">
              <p className="text-sm text-slate-500">Provider</p>
              <p className="mt-2 text-lg font-semibold text-slate-900">{subscription?.provider || "Not connected yet"}</p>
            </div>
          </div>
        </Card>
      </div>
    </div>
  );
}
