export default function StatCard({ label, value, hint, accent = "brand" }) {
  const accentMap = {
    brand: "from-brand-500 to-indigo-600",
    emerald: "from-emerald-500 to-emerald-600",
    amber: "from-amber-400 to-orange-500",
    slate: "from-slate-700 to-slate-900",
  };

  return (
    <div className="overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-soft">
      <div className={`h-1.5 bg-gradient-to-r ${accentMap[accent] || accentMap.brand}`} />
      <div className="p-5">
        <p className="text-sm text-slate-500">{label}</p>
        <p className="mt-3 text-3xl font-bold text-slate-900">{value}</p>
        {hint ? <p className="mt-2 text-xs text-slate-500">{hint}</p> : null}
      </div>
    </div>
  );
}
