import { useEffect, useState } from "react";
import Table from "../components/Table";
import { api } from "../api/client";

export default function AdminSubscriptions() {
  const [rows, setRows] = useState([]);
  const [err, setErr] = useState("");

  useEffect(() => {
    (async () => {
      try {
        const res = await api.get("/admin/subscriptions");
        setRows(res.data);
      } catch (e) {
        setErr(e?.response?.data?.detail || "Could not load subscriptions");
      }
    })();
  }, []);

  return (
    <div className="grid gap-4">
      <h2 className="text-2xl font-bold">Subscriptions</h2>
      {err && <div className="rounded-xl bg-red-50 px-3 py-2 text-sm text-red-700">{err}</div>}
      <Table
        columns={[
          { key: "id", label: "ID" },
          { key: "user_id", label: "User ID" },
          { key: "plan", label: "Plan" },
          { key: "status", label: "Status" },
          { key: "stripe_customer_id", label: "Stripe Customer" },
          { key: "stripe_subscription_id", label: "Stripe Subscription" }
        ]}
        rows={rows}
      />
    </div>
  );
}
