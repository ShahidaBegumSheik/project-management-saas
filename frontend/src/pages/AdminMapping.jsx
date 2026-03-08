import { useEffect, useState } from "react";
import Table from "../components/Table";
import { api } from "../api/client";

export default function AdminMapping() {
  const [rows, setRows] = useState([]);
  const [err, setErr] = useState("");

  useEffect(() => {
    (async () => {
      try {
        const res = await api.get("/admin/user-subscriptions");
        setRows(res.data);
      } catch (e) {
        setErr(e?.response?.data?.detail || "Could not load mapping");
      }
    })();
  }, []);

  return (
    <div className="grid gap-4">
      <h2 className="text-2xl font-bold">User → Subscription Mapping</h2>
      {err && <div className="rounded-xl bg-red-50 px-3 py-2 text-sm text-red-700">{err}</div>}
      <Table
        columns={[
          { key: "user_id", label: "User ID" },
          { key: "email", label: "Email" },
          { key: "plan", label: "Plan" },
          { key: "status", label: "Status" }
        ]}
        rows={rows}
      />
    </div>
  );
}
