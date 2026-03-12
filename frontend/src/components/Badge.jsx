import { titleCase } from "../utils/formatters";

const tones = {
  neutral: "bg-slate-100 text-slate-600",
  success: "bg-emerald-100 text-emerald-700",
  warning: "bg-amber-100 text-amber-700",
  danger: "bg-rose-100 text-rose-700",
  info: "bg-indigo-100 text-indigo-700",
};

export default function Badge({ children, tone = "neutral" }) {
  return <span className={`badge ${tones[tone] || tones.neutral}`}>{titleCase(children)}</span>;
}
