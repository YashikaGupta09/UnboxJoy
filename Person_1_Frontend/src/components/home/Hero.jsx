import { useQuestionnaire } from "../../context/QuestionnaireContext.jsx";

const sampleChips = ["Scent", "Nostalgic", "Cosy nights", "Chai"];

export default function Hero() {
  const { state, dispatch } = useQuestionnaire();
  const hasProgress = Object.keys(state.answers).length > 0;

  return (
    <section className="mx-auto grid max-w-5xl items-center gap-12 px-5 py-16 md:grid-cols-2 md:py-24">
      <div>
        <h1 className="text-4xl font-extrabold leading-[1.05] tracking-tight sm:text-5xl lg:text-6xl">
          The best gifts start with a memory.
        </h1>
        <p className="mt-6 max-w-md text-lg leading-relaxed text-ink/75">
          Answer a few questions about the person you're buying for. We'll turn
          your story into a gift box of products from different brands, picked
          for how it should feel.
        </p>

        <div className="mt-8 flex flex-wrap items-center gap-4">
          <button
            onClick={() => dispatch({ type: "START" })}
            className="rounded-full bg-rose px-7 py-3.5 font-semibold text-white shadow-lg shadow-rose/30 transition hover:brightness-110"
          >
            {hasProgress ? "Continue your box" : "Start building"}
          </button>
          <span className="text-sm text-ink/60">Takes about 3 minutes</span>
        </div>
      </div>

      {/* The memorable element: a gift tag that turns a memory into picks */}
      <div className="relative mx-auto w-full max-w-sm" aria-hidden="true">
        <div className="-rotate-3 rounded-3xl bg-white p-6 shadow-xl ring-1 ring-mist">
          <div className="mb-4 flex items-center gap-2">
            <span className="h-3 w-3 rounded-full border-2 border-mist" />
            <span className="h-px flex-1 bg-mist" />
          </div>
          <p className="font-display text-sm font-bold text-ink/50">For Aanya</p>
          <p className="mt-2 font-display text-xl font-bold leading-snug">
            "Rainy evening at the hill station, sharing hot chai."
          </p>
          <div className="mt-5 flex flex-wrap gap-2">
            {sampleChips.map((c, i) => (
              <span
                key={c}
                className={`rounded-full px-3 py-1 text-sm font-semibold ${
                  i % 2 ? "bg-saffron/25 text-ink" : "bg-ink text-lilac"
                }`}
              >
                {c}
              </span>
            ))}
          </div>
        </div>
        <div className="absolute -bottom-5 -right-2 rotate-3 rounded-2xl bg-saffron px-4 py-3 text-sm font-bold shadow-lg">
          🕯️ Spiced chai candle + ☕ small-batch tea
        </div>
      </div>
    </section>
  );
}
