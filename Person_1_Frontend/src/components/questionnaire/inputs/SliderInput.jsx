/** Single numeric slider (e.g. budget). */
export default function SliderInput({ question, value, onChange }) {
  const current = value ?? question.defaultValue ?? question.min;
  const fmt = (n) => `${question.prefix ?? ""}${Number(n).toLocaleString("en-IN")}`;

  return (
    <div className="rounded-2xl bg-white p-6 ring-1 ring-mist">
      <p className="text-center font-display text-4xl font-extrabold" aria-live="polite">
        {fmt(current)}
      </p>
      <input
        type="range"
        aria-label={question.title}
        min={question.min}
        max={question.max}
        step={question.step}
        value={current}
        onChange={(e) => onChange(Number(e.target.value))}
        className="mt-6 h-2 w-full cursor-pointer accent-rose"
      />
      <div className="mt-2 flex justify-between text-sm text-ink/60">
        <span>{fmt(question.min)}</span>
        <span>{fmt(question.max)}</span>
      </div>
    </div>
  );
}
