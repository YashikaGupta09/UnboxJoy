import { useMemo, useState } from "react";
import { useQuestionnaire } from "../../context/QuestionnaireContext.jsx";
import { buildResponse } from "../../utils/buildResponse.js";
import { submitResponse } from "../../services/api.js";
import { questions } from "../../data/questions.js";

// Where the Gift Box Builder (Person 4) is running.
const GIFT_BOX_URL = import.meta.env.VITE_GIFT_BOX_URL || "http://localhost:5002";

const labelFor = (id, v) =>
  questions.find((q) => q.id === id)?.options?.find((o) => o.value === v)?.label ?? v;

const rupees = (n) => `₹${Number(n).toLocaleString("en-IN")}`;

function Chips({ title, items = [], dark = false }) {
  if (!items.length) return null;
  return (
    <div>
      <h4 className="mb-2 font-display text-sm font-bold text-ink/60">{title}</h4>
      <ul className="flex flex-wrap gap-2">
        {items.map((item) => (
          <li
            key={item}
            className={`rounded-full px-3 py-1 text-sm font-semibold ${
              dark ? "bg-ink text-lilac" : "bg-saffron/30 text-ink"
            }`}
          >
            {item}
          </li>
        ))}
      </ul>
    </div>
  );
}

function ProfileCard({ profile }) {
  return (
    <div className="rounded-3xl bg-white p-6 ring-1 ring-mist sm:p-8">
      <h3 className="font-display text-xl font-bold">Their gift profile</h3>
      <p className="mt-3 text-lg leading-relaxed text-ink/80">{profile.summary}</p>
      <div className="mt-6 grid gap-5 sm:grid-cols-3">
        <Chips title="Personality" items={profile.personalityTraits} dark />
        <Chips title="Interests" items={profile.interests} />
        <Chips title="Emotional themes" items={profile.emotionalThemes} dark />
      </div>
    </div>
  );
}

function RecommendationCard({ item }) {
  return (
    <li className="flex flex-col rounded-2xl bg-white p-5 ring-1 ring-mist">
      <div className="flex items-start justify-between gap-3">
        <h4 className="font-display text-lg font-bold leading-snug">{item.name}</h4>
        <span className="shrink-0 rounded-full bg-rose px-3 py-1 text-sm font-bold text-white">
          {rupees(item.price)}
        </span>
      </div>
      <p className="mt-1 text-sm font-semibold text-ink/60">
        {item.brand}
        {item.category && <span className="capitalize"> · {item.category}</span>}
      </p>
      <p className="mt-3 flex-1 text-ink/80">{item.reason}</p>
    </li>
  );
}

export default function Summary() {
  const { state, dispatch } = useQuestionnaire();
  const response = useMemo(() => buildResponse(state.answers), [state.answers]);

  const [status, setStatus] = useState("idle"); // idle | sending | done | error
  const [result, setResult] = useState(null);

  async function handleSubmit() {
    setStatus("sending");
    setResult(null);
    try {
      const data = await submitResponse(response);
      if (!data?.profile || !Array.isArray(data.recommendations)) {
        throw new Error("Invalid recommendation response");
      }
      setResult(data);
      setStatus("done");
    } catch {
      setStatus("error");
    }
  }

  const rows = [
    ["For", `${response.recipient.name} (${labelFor("relationship", response.recipient.relationship)})`],
    ["Occasion", labelFor("occasion", response.occasion)],
    ["Memory", response.favouriteMemory],
    ["Experiences", response.experiences.map((v) => labelFor("experiences", v)).join(", ")],
    ["Senses", response.senses.map((v) => labelFor("senses", v)).join(", ")],
    ["Feelings", response.emotions.map((v) => labelFor("emotions", v)).join(", ")],
    ["Budget", rupees(response.budget.amount)],
    ["Avoid", response.avoid || "Nothing"],
  ];

  const recap = (
    <dl className="divide-y divide-mist rounded-2xl bg-white ring-1 ring-mist">
      {rows.map(([k, v]) => (
        <div key={k} className="grid gap-1 px-5 py-4 sm:grid-cols-[8rem_1fr]">
          <dt className="font-semibold text-ink/60">{k}</dt>
          <dd>{v}</dd>
        </div>
      ))}
    </dl>
  );

  /* ---------- Results view ---------- */
  if (status === "done" && result) {
    return (
      <section className="mx-auto max-w-4xl px-5 py-10 sm:py-14">
        <h2 className="text-3xl font-extrabold sm:text-4xl">
          Gift ideas for {response.recipient.name || "them"}
        </h2>
        <p className="mt-2 text-ink/70">
          Picked from your memories and what they love. Each one comes with a reason.
        </p>

        <div className="mt-8">
          <ProfileCard profile={result.profile} />
        </div>

        <ul className="mt-8 grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {result.recommendations.map((item, i) => (
            <RecommendationCard key={`${item.name}-${i}`} item={item} />
          ))}
        </ul>

        <div className="mt-10 rounded-3xl bg-ink p-6 text-lilac sm:p-8">
          <h3 className="font-display text-xl font-bold">Ready to pack the box?</h3>
          <p className="mt-2 text-lilac/80">
            Choose packaging, check your budget and add these gifts to a custom box.
          </p>
          <a
            href={GIFT_BOX_URL}
            className="mt-5 inline-block rounded-full bg-saffron px-7 py-3 font-semibold text-ink transition hover:brightness-105"
          >
            Open Gift Box Builder
          </a>
        </div>

        <details className="mt-8">
          <summary className="cursor-pointer font-semibold text-ink/70">Review your answers</summary>
          <div className="mt-4">{recap}</div>
        </details>

        <div className="mt-8 flex flex-wrap gap-4 text-sm font-semibold text-ink/70">
          <button onClick={() => dispatch({ type: "EDIT" })} className="underline">
            Edit answers
          </button>
          <button onClick={() => dispatch({ type: "RESET" })} className="underline">
            Start over
          </button>
        </div>
      </section>
    );
  }

  /* ---------- Review & submit view ---------- */
  return (
    <section className="mx-auto max-w-2xl px-5 py-10 sm:py-14">
      <h2 className="text-3xl font-extrabold sm:text-4xl">
        Here's what we know about {response.recipient.name || "them"}
      </h2>
      <p className="mt-2 text-ink/70">Check it over. You can go back and change anything.</p>

      <div className="mt-8">{recap}</div>

      <div className="mt-8 flex flex-wrap gap-3">
        <button
          onClick={handleSubmit}
          disabled={status === "sending"}
          className="rounded-full bg-rose px-7 py-3 font-semibold text-white shadow-lg shadow-rose/30 transition hover:brightness-110 disabled:opacity-60"
        >
          {status === "sending" ? "Finding gifts…" : status === "error" ? "Try again" : "Build my gift box"}
        </button>
        <button
          onClick={() => dispatch({ type: "EDIT" })}
          disabled={status === "sending"}
          className="rounded-full border-2 border-ink/20 px-6 py-3 font-semibold transition hover:border-ink disabled:opacity-50"
        >
          Edit answers
        </button>
      </div>

      {status === "sending" && (
        <p className="mt-4 rounded-xl bg-saffron/25 px-4 py-3" role="status">
          Reading your story and choosing gifts. This can take a few seconds.
        </p>
      )}
      {status === "error" && (
        <p className="mt-4 rounded-xl bg-rose/15 px-4 py-3" role="alert">
          We couldn't get gift ideas. Check that the recommendation server is running, then try again.
        </p>
      )}

      <button
        onClick={() => dispatch({ type: "RESET" })}
        className="mt-8 text-sm font-semibold text-ink/60 underline"
      >
        Start over
      </button>
    </section>
  );
}
