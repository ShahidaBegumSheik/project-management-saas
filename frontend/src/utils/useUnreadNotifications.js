import { useEffect, useState } from "react";
import api from "../api/client";

export default function useUnreadNotifications() {
  const [count, setCount] = useState(0);

  useEffect(() => {
    let active = true;
    api
      .get("/notifications/unread-count")
      .then((res) => {
        if (active) setCount(res.data.unread_count || 0);
      })
      .catch(() => undefined);

    return () => {
      active = false;
    };
  }, []);

  return count;
}
