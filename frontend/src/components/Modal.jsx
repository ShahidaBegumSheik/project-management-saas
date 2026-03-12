export default function Modal({ open, title, onClose, children }) {
  if (!open) return null;
  return (
    <div className="fixed inset-0 z-40 flex items-center justify-center bg-slate-950/40 px-4" onClick={onClose}>
      <div className="w-full max-w-xl rounded-3xl bg-white p-6 shadow-soft" onClick={(e) => e.stopPropagation()}>
        <div className="mb-4 flex items-center justify-between">
          <h3 className="text-lg font-semibold text-slate-900">{title}</h3>
          <button className="rounded-full p-2 text-slate-500 hover:bg-slate-100" onClick={onClose}>✕</button>
        </div>
        {children}
      </div>
    </div>
  );
}
