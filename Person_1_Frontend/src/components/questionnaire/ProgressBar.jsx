export default function ProgressBar({ step, total }) {
  const pct = Math.round(((step + 1) / total) * 100);
  return (
    <div>
      <div className="mb-2 flex justify-between text-sm font-semibold text-ink/60">
        <span>Question {step + 1} of {total}</span>
        <span>{pct}%</span>
      </div>
      <div
        className="h-2 overflow-hidden rounded-full bg-mist"
        role="progressbar"
        aria-valuenow={pct}
        aria-valuemin={0}
        aria-valuemax={100}
      >
        <div className="h-full rounded-full bg-rose transition-all duration-300" style={{ width: `${pct}%` }} />
      </div>
    </div>
  );
}
