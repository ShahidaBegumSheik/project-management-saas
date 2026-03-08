export default function Card({ title, subtitle, children }) {
  return (
    <div className="rounded-2xl border bg-white p-6 shadow-sm">
      {title && <h2 className="text-lg font-semibold text-slate-900">{title}</h2>}
      {subtitle && <p className="mt-1 text-sm text-slate-500">{subtitle}</p>}
      <div className={title || subtitle ? "mt-4" : ""}>{children}</div>
    </div>
  );
}
