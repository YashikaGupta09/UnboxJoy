export default function TextInput({ question, value = "", onChange }) {
  const common = {
    id: question.id,
    value,
    placeholder: question.placeholder,
    maxLength: question.maxLength,
    onChange: (e) => onChange(e.target.value),
    className:
      "w-full rounded-2xl border-2 border-mist bg-white px-4 py-3.5 text-lg placeholder:text-ink/35 focus:border-ink focus:outline-none",
  };

  return (
    <div>
      {question.type === "textarea" ? (
        <textarea rows={5} {...common} />
      ) : (
        <input type="text" autoComplete="off" {...common} />
      )}
      {question.maxLength && (
        <p className="mt-2 text-right text-sm text-ink/50">
          {value.length}/{question.maxLength}
        </p>
      )}
    </div>
  );
}
