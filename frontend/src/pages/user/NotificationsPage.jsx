import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../../api/client";
import Card from "../../components/Card";
import Button from "../../components/Button";
import Loader from "../../components/Loader";
import { useToast } from "../../contexts/ToastContext";
import { formatDate, getErrorMessage } from "../../utils/formatters";


export default function NotificationsPage() {
  const { push } = useToast();
  const navigate = useNavigate();


  const [notifications, setNotifications] = useState([]);
  const [unreadCount, setUnreadCount] = useState(0);
  const [loading, setLoading] = useState(true);


  async function loadNotifications() {
    const res = await api.get("/notifications");
    setNotifications(res.data);
  }


  async function loadUnreadCount() {
    const res = await api.get("/notifications/unread-count");
    setUnreadCount(res.data.unread_count);
  }


  async function loadAll() {
    setLoading(true);
    try {
      await Promise.all([loadNotifications(), loadUnreadCount()]);
    } catch (error) {
      push(getErrorMessage(error), "error");
    } finally {
      setLoading(false);
    }
  }


  useEffect(() => {
    loadAll();
  }, []);


  async function markOneRead(id) {
    await api.patch(`/notifications/${id}/read`);
    await loadAll();
  }


  async function markAllRead() {
    await api.patch("/notifications/read-all");
    push("All notifications marked as read", "success");
    await loadAll();
  }


  async function openNotification(notification) {
    try {
      if (!notification.is_read) {
        await api.patch(`/notifications/${notification.id}/read`);
      }


      await loadAll();


      if (notification.link) {
        const url = new URL(notification.link, window.location.origin);
        navigate(`${url.pathname}${url.search}`);
      }
    } catch (error) {
      push(getErrorMessage(error), "error");
    }
  }


  if (loading) return <Loader label="Loading notifications..." />;


  return (
    <Card
      title="In-app notifications"
      subtitle={`Unread count: ${unreadCount}`}
      action={<Button variant="secondary" onClick={markAllRead}>Mark all as read</Button>}
    >
      <div className="space-y-3">
        {notifications.length ? (
          notifications.map((notification) => (
            <button
              key={notification.id}
              type="button"
              onClick={() => openNotification(notification)}
              className={`w-full rounded-2xl border p-4 text-left transition ${
                notification.is_read
                  ? "border-slate-200 bg-white"
                  : "border-blue-200 bg-blue-50"
              }`}
            >
              <div className="flex items-start justify-between gap-3">
                <div>
                  <p className="font-semibold text-slate-900">{notification.title}</p>
                  <p className="mt-1 text-sm text-slate-600">{notification.message}</p>
                  <p className="mt-2 text-xs text-slate-500">{formatDate(notification.created_at)}</p>
                </div>


                <span
                  className={`rounded-full px-2 py-1 text-xs font-medium ${
                    notification.is_read
                      ? "bg-slate-100 text-slate-600"
                      : "bg-blue-100 text-blue-700"
                  }`}
                >
                  {notification.is_read ? "Read" : "Unread"}
                </span>
              </div>
            </button>
          ))
        ) : (
          <p className="text-sm text-slate-500">No notifications available.</p>
        )}
      </div>
    </Card>
  );
}