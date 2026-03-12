import { useEffect, useState } from "react";
import api from "../../api/client";
import Button from "../../components/Button";
import Card from "../../components/Card";
import Loader from "../../components/Loader";
import { useToast } from "../../contexts/ToastContext";
import { getErrorMessage } from "../../utils/formatters";

const initial = { user_id: "", title: "", message: "", type: "system" };

export default function AdminNotificationsPage() {
  const { push } = useToast();
  const [loading, setLoading] = useState(true);
  const [sending, setSending] = useState(false);
  const [users, setUsers] = useState([]);
  const [form, setForm] = useState(initial);

  useEffect(() => {
    api.get("/admin/users")
      .then((res) => setUsers(res.data))
      .catch((error) => push(getErrorMessage(error), "error"))
      .finally(() => setLoading(false));
  }, [push]);

  async function handleSubmit(event) {
    event.preventDefault();
    setSending(true);
    try {
      await api.post("/admin/notifications", {
        ...form,
        user_id: form.user_id ? Number(form.user_id) : null,
      });
      push("System notification sent", "success");
      setForm(initial);
    } catch (error) {
      push(getErrorMessage(error), "error");
    } finally {
      setSending(false);
    }
  }

  if (loading) return <Loader label="Loading notification recipients..." />;

  return (
    <Card title="Admin announcements" subtitle="Optional system notifications for one user or the whole platform.">
      <form className="grid gap-4 md:grid-cols-2" onSubmit={handleSubmit}>
        <label className="label block">
          Recipient
          <select className="input" value={form.user_id} onChange={(e) => setForm((prev) => ({ ...prev, user_id: e.target.value }))}>
            <option value="">All users</option>
            {users.map((user) => (
              <option key={user.id} value={user.id}>{user.email}</option>
            ))}
          </select>
        </label>
        <label className="label block">
          Type
          <select className="input" value={form.type} onChange={(e) => setForm((prev) => ({ ...prev, type: e.target.value }))}>
            <option value="system">System</option>
            <option value="info">Info</option>
            <option value="alert">Alert</option>
            <option value="billing">Billing</option>
          </select>
        </label>
        <label className="label block md:col-span-2">
          Title
          <input className="input" value={form.title} onChange={(e) => setForm((prev) => ({ ...prev, title: e.target.value }))} required />
        </label>
        <label className="label block md:col-span-2">
          Message
          <textarea className="input min-h-[140px]" value={form.message} onChange={(e) => setForm((prev) => ({ ...prev, message: e.target.value }))} required />
        </label>
        <div className="md:col-span-2 flex justify-end">
          <Button type="submit" disabled={sending}>{sending ? "Sending..." : "Send notification"}</Button>
        </div>
      </form>
    </Card>
  );
}
