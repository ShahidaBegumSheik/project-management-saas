import { useEffect, useState } from "react";
import Card from "../components/Card";
import { api } from "../api/client";

export default function Billing() {
  const [billing, setBilling] = useState(null);
  const [err, setErr] = useState("");

  async function loadBilling() {
    try {
      const res = await api.get("/billing/me");
      setBilling(res.data);
    } catch (e) {
      setErr(e?.response?.data?.detail || "Could not load billing");
    }
  }

  async function upgrade() {
    try {
      const res = await api.post("/billing/checkout/pro");
      window.location.href = res.data.url;
    } catch (e) {
      setErr(e?.response?.data?.detail || "Checkout failed");
    }
  }

  async function openPortal() {
    try {
      const res = await api.post("/billing/portal");
      window.location.href = res.data.url;
    } catch (e) {
      setErr(e?.response?.data?.detail || "Portal failed");
    }
  }

  async function cancelPlan() {
    try {
      await api.post("/billing/cancel");
      await loadBilling();
    } catch (e) {
      setErr(e?.response?.data?.detail || "Cancel failed");
    }
  }

  useEffect(() => {
    loadBilling();
  }, []);

  return (
    <div className="grid gap-6">
      <Card title="Billing" subtitle="Manage your current subscription">
        {err && <div className="mb-4 rounded-xl bg-red-50 px-3 py-2 text-sm text-red-700">{err}</div>}

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

            <div className="mt-4 grid gap-4 md:grid-cols-2">
              <div className="rounded-2xl border p-4">
                <p className="text-sm text-slate-500">Stripe customer ID</p>
                <p className="mt-1 break-all text-sm">{billing.stripe_customer_id || "-"}</p>
              </div>

              <div className="rounded-2xl border p-4">
                <p className="text-sm text-slate-500">Stripe subscription ID</p>
                <p className="mt-1 break-all text-sm">{billing.stripe_subscription_id || "-"}</p>
              </div>
            </div>

            <div className="mt-6 flex flex-wrap gap-3">
              <button
                onClick={upgrade}
                className="rounded-xl bg-slate-900 px-4 py-2 font-semibold text-white hover:bg-slate-800"
              >
                Upgrade to Pro
              </button>
              <button
                onClick={openPortal}
                className="rounded-xl border px-4 py-2 font-semibold text-slate-700 hover:bg-slate-50"
              >
                Manage in Stripe Portal
              </button>
              <button
                onClick={cancelPlan}
                className="rounded-xl border border-red-300 px-4 py-2 font-semibold text-red-700 hover:bg-red-50"
              >
                Cancel Subscription
              </button>
            </div>

            <p className="mt-4 text-sm text-slate-500">
              This frontend works with the current mock Stripe backend flow. Clicking upgrade redirects to a mock checkout route.
            </p>
          </>
        )}
      </Card>
    </div>
  );
}
