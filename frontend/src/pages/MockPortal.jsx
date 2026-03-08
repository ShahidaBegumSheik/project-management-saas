import { useNavigate, useSearchParams } from "react-router-dom";
import Card from "../components/Card";

export default function MockPortal() {
  const navigate = useNavigate();
  const [params] = useSearchParams();
  const userId = params.get("user_id");

  return (
    <div className="mx-auto mt-10 max-w-xl">
      <Card title="Mock Billing Portal" subtitle="Simulated customer portal for development">
        <p className="text-sm text-slate-600">User ID: {userId || "-"}</p>
        <p className="mt-4 text-sm text-slate-500">
          In a real Stripe integration, users would manage payment methods, invoices, and plan changes here.
        </p>
        <div className="mt-6">
          <button
            onClick={() => navigate("/app/billing")}
            className="rounded-xl bg-slate-900 px-4 py-2 font-semibold text-white hover:bg-slate-800"
          >
            Back to Billing
          </button>
        </div>
      </Card>
    </div>
  );
}
