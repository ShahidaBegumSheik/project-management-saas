import { useEffect, useMemo, useState } from "react";
import api from "../../api/client";
import Card from "../../components/Card";
import Loader from "../../components/Loader";
import StatCard from "../../components/StatCard";
import { MiniBarChart, MiniPieChart } from "../../components/Charts";
import { useToast } from "../../contexts/ToastContext";
import { getErrorMessage } from "../../utils/formatters";

export default function AdminDashboard() {
  const { push } = useToast();
  const [loading, setLoading] = useState(true);
  const [data, setData] = useState(null);
  const [users, setUsers] = useState([]);

  useEffect(() => {
    async function load() {
      try {
        const [analyticsRes, usersRes] = await Promise.all([
          api.get("/analytics/admin"),
          api.get("/admin/users"),
        ]);
        setData(analyticsRes.data);
        setUsers(usersRes.data.slice(0, 6));
      } catch (error) {
        push(getErrorMessage(error), "error");
      } finally {
        setLoading(false);
      }
    }
    load();
  }, [push]);

  const pieData = useMemo(() => [
    { name: "Free", value: data?.free_users || 0 },
    { name: "Pro", value: data?.pro_users || 0 },
  ], [data]);

  const registrationData = useMemo(() => [
    { name: "This Month", value: data?.registrations_this_month || 0 },
    { name: "Active Subs", value: data?.active_subscriptions || 0 },
    { name: "Teams", value: data?.teams_count || 0 },
  ], [data]);

  if (loading) return <Loader label="Loading admin analytics..." />;

  return (
    <div className="space-y-6">
      <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
        <StatCard label="Total Users" value={data?.total_users || 0} />
        <StatCard label="Active Subscriptions" value={data?.active_subscriptions || 0} accent="emerald" />
        <StatCard label="Monthly Registrations" value={data?.registrations_this_month || 0} accent="amber" />
        <StatCard label="Teams Count" value={data?.teams_count || 0} accent="slate" />
      </div>

      <div className="grid gap-6 xl:grid-cols-2">
        <Card title="Free vs Pro distribution" subtitle="Required admin visibility into plan split using Recharts.">
          <MiniPieChart data={pieData} />
        </Card>
        <Card title="Monthly growth snapshot" subtitle="Administrative KPI bars for new registrations and active subscriptions.">
          <MiniBarChart data={registrationData} />
        </Card>
      </div>

      <Card title="Latest users" subtitle="Quick operational visibility into recently available users.">
        <div className="overflow-x-auto">
          <table className="min-w-full text-left text-sm">
            <thead>
              <tr className="border-b border-slate-200 text-slate-500">
                <th className="pb-3 pr-4 font-medium">Email</th>
                <th className="pb-3 pr-4 font-medium">Role</th>
                <th className="pb-3 pr-4 font-medium">Status</th>
              </tr>
            </thead>
            <tbody>
              {users.map((user) => (
                <tr key={user.id} className="border-b border-slate-100 last:border-0">
                  <td className="py-3 pr-4 text-slate-700">{user.email}</td>
                  <td className="py-3 pr-4 text-slate-500">{user.role}</td>
                  <td className="py-3 pr-4 text-slate-500">{user.is_active ? "Active" : "Inactive"}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </Card>
    </div>
  );
}
