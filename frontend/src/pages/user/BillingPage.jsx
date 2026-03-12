import { useEffect, useState } from "react";
import api from "../../api/client";
import Button from "../../components/Button";
import Card from "../../components/Card";
import Loader from "../../components/Loader";
import { useToast } from "../../contexts/ToastContext";
import { getErrorMessage, titleCase } from "../../utils/formatters";

function loadRazorpayScript() {
  return new Promise((resolve) => {
    if (window.Razorpay) return resolve(true);
    const script = document.createElement("script");
    script.src = "https://checkout.razorpay.com/v1/checkout.js";
    script.onload = () => resolve(true);
    script.onerror = () => resolve(false);
    document.body.appendChild(script);
  });
}

export default function BillingPage() {
  const { push } = useToast();
  const [loading, setLoading] = useState(true);
  const [processing, setProcessing] = useState(false);
  const [subscription, setSubscription] = useState(null);

  async function loadSubscription() {
    setLoading(true);
    try {
      const { data } = await api.get("/billing/me");
      setSubscription(data);
    } catch (error) {
      push(getErrorMessage(error), "error");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => { loadSubscription(); }, []);

  async function upgrade() {
    setProcessing(true);
    try {
      const loaded = await loadRazorpayScript();
      if (!loaded) throw new Error("Unable to load Razorpay checkout script");
      const { data: order } = await api.post("/billing/checkout/pro");
      const razorpay = new window.Razorpay({
        key: order.key_id,
        amount: order.amount,
        currency: order.currency,
        name: order.company_name,
        description: order.description,
        order_id: order.order_id,
        theme: { color: "#4f46e5" },
        handler: async (response) => {
          try {
            await api.post("/billing/verify-payment", response);
            push("Subscription upgraded to Pro", "success");
            await loadSubscription();
          } catch (error) {
            push(getErrorMessage(error), "error");
          }
        },
      });
      razorpay.open();
    } catch (error) {
      push(getErrorMessage(error), "error");
    } finally {
      setProcessing(false);
    }
  }

  async function cancelPlan() {
    if (!window.confirm("Cancel your subscription and move back to Free plan?")) return;
    setProcessing(true);
    try {
      await api.post("/billing/cancel");
      push("Subscription cancelled", "success");
      await loadSubscription();
    } catch (error) {
      push(getErrorMessage(error), "error");
    } finally {
      setProcessing(false);
    }
  }

  if (loading) return <Loader label="Loading billing details..." />;

  const isPro = subscription?.plan === "pro";

  return (
    <div className="grid gap-6 xl:grid-cols-[1.1fr_0.9fr]">
      <div className="grid gap-6 md:grid-cols-2">
        <Card title="Free plan" subtitle="Good for initial usage with server-enforced project limits.">
          <p className="mb-5 text-sm text-slate-500">Create up to 3 projects, use the full user panel, and upgrade when ready.</p>
          <ul className="mb-6 space-y-2 text-sm text-slate-600">
            <li>• Max 3 projects</li>
            <li>• Team collaboration support</li>
            <li>• Notifications and activity tracking</li>
          </ul>
          <Button variant="secondary" onClick={cancelPlan} disabled={processing}>Switch to Free</Button>
        </Card>
        <Card title="Pro plan" subtitle="Upgrade using Razorpay checkout and unlock unlimited project growth." className="border-brand-100 bg-brand-50/50">
          <p className="mb-5 text-sm text-slate-600">Use your backend's live Razorpay flow for checkout and payment verification.</p>
          <ul className="mb-6 space-y-2 text-sm text-slate-600">
            <li>• Unlimited projects</li>
            <li>• Billing notifications and invoices</li>
            <li>• Pro analytics friendly workflow</li>
          </ul>
          <Button onClick={upgrade} disabled={processing || isPro}>{processing ? "Processing..." : isPro ? "Already on Pro" : "Upgrade to Pro"}</Button>
        </Card>
      </div>

      <Card title="Current billing status" subtitle="Synchronized with backend subscription state.">
        <div className="space-y-4">
          {[
            ["Plan", titleCase(subscription?.plan || "free")],
            ["Status", titleCase(subscription?.status || "active")],
            ["Provider", subscription?.provider || "—"],
            ["Order ID", subscription?.razorpay_order_id || "—"],
            ["Payment ID", subscription?.razorpay_payment_id || "—"],
          ].map(([label, value]) => (
            <div key={label} className="rounded-2xl bg-slate-50 px-4 py-3">
              <p className="text-sm text-slate-500">{label}</p>
              <p className="mt-1 font-medium text-slate-900">{value}</p>
            </div>
          ))}
        </div>
      </Card>
    </div>
  );
}
