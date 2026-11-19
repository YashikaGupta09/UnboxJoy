/** Several two-sided sliders (e.g. Calm <-> Adventurous). Value is an object keyed by scale id. */
export default function SpectrumInput({ question, value, onChange }) {
  const current = { ...question.defaultValue, ...(value ?? {}) };

  return (
    <div className="space-y-4">
      {question.scales.map((s) => (
        <div key={s.id} className="rounded-2xl bg-white p-5 ring-1 ring-mist">
          <div className="mb-3 flex justify-between font-semibold">
            <span>{s.left}</span>
            <span>{s.right}</span>
          </div>
          <input
            type="range"
            min={1}
            max={10}
            step={1}
            aria-label={`${s.left} to ${s.right}`}
            value={current[s.id]}
            onChange={(e) => onChange({ ...current, [s.id]: Number(e.target.value) })}
            className="h-2 w-full cursor-pointer accent-rose"
          />
        </div>
      ))}
    </div>
  );
}
