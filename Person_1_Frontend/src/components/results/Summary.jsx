import { useMemo, useState } from "react";
import { useQuestionnaire } from "../../context/QuestionnaireContext.jsx";
import { buildResponse } from "../../utils/buildResponse.js";
import { submitResponse } from "../../services/api.js";
import { questions } from "../../data/questions.js";

const labelFor = (id, v) =>
  questions.find((q) => q.id === id)?.options?.find((o) => o.value === v)?.label ?? v;

export default function Summary() {
  const { state, dispatch } = useQuestionnaire();
  const response = useMemo(() => buildResponse(state.answers), [state.answers]);
  const json = JSON.stringify(response, null, 2);

  const [status, setStatus] = useState("idle"); // idle | sending | done | error
  const [copied, setCopied] = useState(false);

  async function handleSubmit() {
    setStatus("sending");
    try {
      await submitResponse(response);
      setStatus("done");
    } catch {
      setStatus("error");
    }
  }

  async function copy() {
    try {
      await navigator.clipboard.writeText(json);
      setCopied(true);
      setTimeout(() => setCopied(false), 1500);
    } catch {
      /* clipboard blocked */
    }
  }

  function download() {
    const url = URL.createObjectURL(new Blob([json], { type: "application/json" }));
    const a = document.createElement("a");
    a.href = url;
    a.download = "unboxjoy-response.json";
    a.click();
    URL.revokeObjectURL(url);
  }

  const rows = [
    ["For", `${response.recipient.name} (${labelFor("relationship", response.recipient.relationship)})`],
    ["Occasion", labelFor("occasion", response.occasion)],
    ["Memory", response.favouriteMemory],
    ["Experiences", response.experiences.map((v) => labelFor("experiences", v)).join(", ")],
    ["Senses", response.senses.map((v) => labelFor("senses", v)).join(", ")],
    ["Feelings", response.emotions.map((v) => labelFor("emotions", v)).join(", ")],
    ["Budget", `₹${response.budget.amount.toLocaleString("en-IN")}`],
    ["Avoid", response.avoid || "Nothing"],
  ];

  return (
    <section className="mx-auto max-w-2xl px-5 py-10 sm:py-14">
      <h2 className="text-3xl font-extrabold sm:text-4xl">
        Here's what we know about {response.recipient.name || "them"}
      </h2>
      <p className="mt-2 text-ink/70">Check it over. You can go back and change anything.</p>

      <dl className="mt-8 divide-y divide-mist rounded-2xl bg-white ring-1 ring-mist">
        {rows.map(([k, v]) => (
          <div key={k} className="grid gap-1 px-5 py-4 sm:grid-cols-[8rem_1fr]">
            <dt className="font-semibold text-ink/60">{k}</dt>
            <dd>{v}</dd>
          </div>
        ))}
      </dl>

      <div className="mt-8 flex flex-wrap gap-3">
        <button
          onClick={handleSubmit}
          disabled={status === "sending" || status === "done"}
          className="rounded-full bg-rose px-7 py-3 font-semibold text-white shadow-lg shadow-rose/30 transition hover:brightness-110 disabled:opacity-50"
        >
          {status === "sending" ? "Building…" : status === "done" ? "Sent" : "Build my gift box"}
        </button>
        <button
          onClick={() => dispatch({ type: "EDIT" })}
          className="rounded-full border-2 border-ink/20 px-6 py-3 font-semibold transition hover:border-ink"
        >
          Edit answers
        </button>
      </div>

      {status === "done" && (
        <p className="mt-4 rounded-xl bg-saffron/25 px-4 py-3" role="status">
          Your answers were sent. The gift box recommendation will appear here once the recommendation service is connected.
        </p>
      )}
      {status === "error" && (
        <p className="mt-4 rounded-xl bg-rose/15 px-4 py-3" role="alert">
          We couldn't reach the server. Check your connection and try again.
        </p>
      )}

      <details className="mt-10 rounded-2xl bg-ink p-5 text-lilac">
        <summary className="cursor-pointer font-semibold">Developer view: response JSON</summary>
        <pre className="mt-4 max-h-80 overflow-auto text-sm">{json}</pre>
        <div className="mt-4 flex gap-3">
          <button onClick={copy} className="rounded-full bg-lilac px-4 py-2 text-sm font-semibold text-ink">
            {copied ? "Copied" : "Copy JSON"}
          </button>
          <button onClick={download} className="rounded-full bg-lilac px-4 py-2 text-sm font-semibold text-ink">
            Download JSON
          </button>
        </div>
      </details>

      <button
        onClick={() => dispatch({ type: "RESET" })}
        className="mt-8 text-sm font-semibold text-ink/60 underline"
      >
        Start over
      </button>
    </section>
  );
}
