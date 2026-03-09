import { useState } from "react";
import { useNavigate, useSearchParams } from "react-router-dom";
import Card from "../components/Card";
import { api } from "../api/client";

export default function MockCheckout() {
  const navigate = useNavigate();
  const [params] = useSearchParams();
  const [err, setErr] = useState("");
  const userId = params.get("user_id");

  async function simulateSuccess() {
    setErr("");
    try {
      await api.post("/billing/mock-webhook/success");
      navigate("/app/billing?checkout=success");
    } catch (e) {
      setErr(e?.response?.data?.detail || "Payment simulation failed");
    }
  }

  async function simulateFailure() {
    setErr("");
    try {
      await api.post("/billing/mock-webhook/failure");
      navigate("/app/billing?checkout=failure");
    } catch (e) {
      setErr(e?.response?.data?.detail || "Payment simulation failed");
    }
  }

  return (
    <div className="mx-auto mt-10 max-w-xl">
      <Card title="Mock Checkout" subtitle="Simulated Stripe checkout page for development">
        <p className="text-sm text-slate-600">User ID: {userId || "-"}</p>
        {err && <div className="mt-4 rounded-xl bg-red-50 px-3 py-2 text-sm text-red-700">{err}</div>}
        <div className="mt-6 flex flex-wrap gap-3">
          <button
            onClick={simulateSuccess}
            className="rounded-xl bg-slate-900 px-4 py-2 font-semibold text-white hover:bg-slate-800">
            Simulate Payment Success
          </button>
          
          <button
            onClick={simulateFailure}
            className="rounded-xl bg-slate-900 px-4 py-2 font-semibold text-white hover:bg-slate-800">
            Simulate Payment Failure
          </button>

          <button
            onClick={() => navigate("/app/billing")}
            className="rounded-xl border px-4 py-2 font-semibold text-slate-700 hover:bg-slate-50">
            Cancel
          </button>
        </div>
      </Card>
    </div>
  );
}
