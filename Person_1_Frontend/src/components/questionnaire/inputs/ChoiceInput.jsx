/** Handles both "single" and "multi" questions as tappable cards. */
export default function ChoiceInput({ question, value, onChange }) {
  const multi = question.type === "multi";
  const selected = multi ? value ?? [] : value;
  const max = question.maxSelect ?? Infinity;

  const isSelected = (v) => (multi ? selected.includes(v) : selected === v);
  const atLimit = multi && selected.length >= max;

  function toggle(v) {
    if (!multi) return onChange(v);
    if (selected.includes(v)) return onChange(selected.filter((x) => x !== v));
    if (atLimit) return;
    onChange([...selected, v]);
  }

  return (
    <div
      role={multi ? "group" : "radiogroup"}
      aria-label={question.title}
      className="grid gap-3 sm:grid-cols-2"
    >
      {question.options.map((opt) => {
        const on = isSelected(opt.value);
        const disabled = !on && atLimit;
        return (
          <button
            key={opt.value}
            type="button"
            role={multi ? "checkbox" : "radio"}
            aria-checked={on}
            disabled={disabled}
            onClick={() => toggle(opt.value)}
            className={`flex items-center gap-3 rounded-2xl border-2 px-4 py-3.5 text-left font-semibold transition
              ${on ? "border-ink bg-ink text-lilac" : "border-mist bg-white hover:border-ink/40"}
              ${disabled ? "cursor-not-allowed opacity-40" : ""}`}
          >
            <span className="text-2xl" aria-hidden="true">{opt.emoji}</span>
            <span>{opt.label}</span>
          </button>
        );
      })}
    </div>
  );
}
