import { useEffect, useState } from "react";
import { useSearchParams } from "react-router-dom";
import Card from "../components/Card";
import { api } from "../api/client";

export default function Billing() {
  const [billing, setBilling] = useState(null);
  const [err, setErr] = useState("");
  const [successMsg, setSuccessMsg] = useState("");
  const [params] = useSearchParams();

  const checkoutStatus = params.get("checkout");

  async function loadBilling() {
    try {
      const res = await api.get("/billing/me");
      setBilling(res.data);
    } catch (e) {
      setErr(e?.response?.data?.detail || "Could not load billing");
    }
  }

  async function upgrade() {
    setErr("");
    setSuccessMsg("");
    try {
      const res = await api.post("/billing/checkout/pro");
      window.location.href = res.data.url;
    } catch (e) {
      setErr(e?.response?.data?.detail || "Checkout failed");
    }
  }

  async function cancelSubscription() {
    setErr("");
    setSuccessMsg("");

    const ok = window.confirm("Are you sure you want to cancel your Pro subscription?");
    if (!ok) return;

    try {
      const res = await api.post("/billing/mock-webhook/downgrade");
      setSuccessMsg(res.data.message || "Subscription cancelled successfully");
      await loadBilling();
    } catch (e) {
      setErr(e?.response?.data?.detail || "Cancellation failed");
    }
  }

  useEffect(() => {
    loadBilling();
  }, []);

  return (
    <div className="grid gap-6">
      <Card title="Billing" subtitle="Manage your current subscription">
        {checkoutStatus === "success" && (
          <div className="mb-4 rounded-xl bg-green-50 px-3 py-2 text-sm text-green-700">
            Payment successful. Your subscription has been upgraded to Pro.
          </div>
        )}

        {checkoutStatus === "failure" && (
          <div className="mb-4 rounded-xl bg-red-50 px-3 py-2 text-sm text-red-700">
            Payment failed. Your subscription was not upgraded.
          </div>
        )}

        {successMsg && (
          <div className="mb-4 rounded-xl bg-green-50 px-3 py-2 text-sm text-green-700">
            {successMsg}
          </div>
        )}

        {err && (
          <div className="mb-4 rounded-xl bg-red-50 px-3 py-2 text-sm text-red-700">
            {err}
          </div>
        )}

        {!billing ? (
          <p className="text-sm text-slate-500">Loading billing information...</p>
        ) : (
          <>
            <div className="grid gap-4 md:grid-cols-2">
              <div className="rounded-2xl border p-4">
                <p className="text-sm text-slate-500">Current plan</p>
                <p className="mt-1 text-xl font-semibold capitalize">{billing.plan}</p>
              </div>

              <div className="rounded-2xl border p-4">
                <p className="text-sm text-slate-500">Status</p>
                <p className="mt-1 text-xl font-semibold capitalize">{billing.status}</p>
              </div>
            </div>

            <div className="mt-6 flex flex-wrap gap-3">
              {billing.plan === "free" && (
                <button
                  onClick={upgrade}
                  className="rounded-xl bg-slate-900 px-4 py-2 font-semibold text-white hover:bg-slate-800"
                >
                  Upgrade to Pro
                </button>
              )}

              {billing.plan === "pro" && (
                <button
                  onClick={cancelSubscription}
                  className="rounded-xl border border-red-400 px-4 py-2 font-semibold text-red-700 hover:bg-red-50"
                >
                  Cancel Subscription
                </button>
              )}
            </div>
          </>
        )}
      </Card>
    </div>
  );
}

