import { useEffect, useState } from "react";
import api from "../../api/client";
import Badge from "../../components/Badge";
import Card from "../../components/Card";
import Loader from "../../components/Loader";
import { useToast } from "../../contexts/ToastContext";
import { formatDate, getErrorMessage } from "../../utils/formatters";

export default function AdminUsersPage() {
  const { push } = useToast();
  const [loading, setLoading] = useState(true);
  const [users, setUsers] = useState([]);

  useEffect(() => {
    api.get("/admin/users")
      .then((res) => setUsers(res.data))
      .catch((error) => push(getErrorMessage(error), "error"))
      .finally(() => setLoading(false));
  }, [push]);

  if (loading) return <Loader label="Loading users..." />;

  return (
    <Card title="Registered users" subtitle="Separated admin panel view with clean pagination-ready table styling.">
      <div className="overflow-x-auto">
        <table className="min-w-full text-left text-sm">
          <thead>
            <tr className="border-b border-slate-200 text-slate-500">
              <th className="pb-3 pr-4 font-medium">ID</th>
              <th className="pb-3 pr-4 font-medium">Email</th>
              <th className="pb-3 pr-4 font-medium">Role</th>
              <th className="pb-3 pr-4 font-medium">Active</th>
              <th className="pb-3 pr-4 font-medium">Created</th>
            </tr>
          </thead>
          <tbody>
            {users.map((user) => (
              <tr key={user.id} className="border-b border-slate-100 last:border-0">
                <td className="py-3 pr-4">{user.id}</td>
                <td className="py-3 pr-4">{user.email}</td>
                <td className="py-3 pr-4"><Badge tone={user.role === "admin" ? "info" : "neutral"}>{user.role}</Badge></td>
                <td className="py-3 pr-4"><Badge tone={user.is_active ? "success" : "danger"}>{user.is_active ? "active" : "inactive"}</Badge></td>
                <td className="py-3 pr-4 text-slate-500">{formatDate(user.created_at)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </Card>
  );
}
