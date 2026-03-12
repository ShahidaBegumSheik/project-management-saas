import { useEffect, useState } from "react";
import api from "../../api/client";
import Badge from "../../components/Badge";
import Card from "../../components/Card";
import Loader from "../../components/Loader";
import { useToast } from "../../contexts/ToastContext";
import { getErrorMessage } from "../../utils/formatters";

export default function AdminSubscriptionsPage() {
  const { push } = useToast();
  const [loading, setLoading] = useState(true);
  const [rows, setRows] = useState([]);

  useEffect(() => {
    api.get("/admin/subscriptions")
      .then((res) => setRows(res.data))
      .catch((error) => push(getErrorMessage(error), "error"))
      .finally(() => setLoading(false));
  }, [push]);

  if (loading) return <Loader label="Loading subscriptions..." />;

  return (
    <Card title="Subscriptions" subtitle="Administrative subscription monitoring table.">
      <div className="overflow-x-auto">
        <table className="min-w-full text-left text-sm">
          <thead>
            <tr className="border-b border-slate-200 text-slate-500">
              <th className="pb-3 pr-4 font-medium">User ID</th>
              <th className="pb-3 pr-4 font-medium">Plan</th>
              <th className="pb-3 pr-4 font-medium">Status</th>
              <th className="pb-3 pr-4 font-medium">Stripe Customer</th>
              <th className="pb-3 pr-4 font-medium">Stripe Subscription</th>
            </tr>
          </thead>
          <tbody>
            {rows.map((row) => (
              <tr key={row.id} className="border-b border-slate-100 last:border-0">
                <td className="py-3 pr-4">{row.user_id}</td>
                <td className="py-3 pr-4"><Badge tone={row.plan === "pro" ? "success" : "neutral"}>{row.plan}</Badge></td>
                <td className="py-3 pr-4"><Badge tone="info">{row.status}</Badge></td>
                <td className="py-3 pr-4 text-slate-500">{row.stripe_customer_id || "—"}</td>
                <td className="py-3 pr-4 text-slate-500">{row.stripe_subscription_id || "—"}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </Card>
  );
}
