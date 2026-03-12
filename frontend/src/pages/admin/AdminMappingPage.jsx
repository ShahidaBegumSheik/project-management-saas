import { useEffect, useState } from "react";
import api from "../../api/client";
import Badge from "../../components/Badge";
import Card from "../../components/Card";
import Loader from "../../components/Loader";
import { useToast } from "../../contexts/ToastContext";
import { getErrorMessage } from "../../utils/formatters";

export default function AdminMappingPage() {
  const { push } = useToast();
  const [loading, setLoading] = useState(true);
  const [rows, setRows] = useState([]);

  useEffect(() => {
    api.get("/admin/user-subscriptions")
      .then((res) => setRows(res.data))
      .catch((error) => push(getErrorMessage(error), "error"))
      .finally(() => setLoading(false));
  }, [push]);

  if (loading) return <Loader label="Loading user-subscription mapping..." />;

  return (
    <Card title="User to subscription mapping" subtitle="Required operational mapping between users and their plans.">
      <div className="overflow-x-auto">
        <table className="min-w-full text-left text-sm">
          <thead>
            <tr className="border-b border-slate-200 text-slate-500">
              <th className="pb-3 pr-4 font-medium">User ID</th>
              <th className="pb-3 pr-4 font-medium">Email</th>
              <th className="pb-3 pr-4 font-medium">Plan</th>
              <th className="pb-3 pr-4 font-medium">Status</th>
            </tr>
          </thead>
          <tbody>
            {rows.map((row) => (
              <tr key={row.user_id} className="border-b border-slate-100 last:border-0">
                <td className="py-3 pr-4">{row.user_id}</td>
                <td className="py-3 pr-4">{row.email}</td>
                <td className="py-3 pr-4"><Badge tone={row.plan === "pro" ? "success" : "neutral"}>{row.plan}</Badge></td>
                <td className="py-3 pr-4"><Badge tone="info">{row.status}</Badge></td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </Card>
  );
}
