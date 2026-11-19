import { useQuestionnaire } from "../../context/QuestionnaireContext.jsx";
import { questions } from "../../data/questions.js";
import { isAnswered } from "../../utils/validation.js";
import ProgressBar from "./ProgressBar.jsx";
import QuestionCard from "./QuestionCard.jsx";

export default function Questionnaire() {
  const { state, dispatch } = useQuestionnaire();
  const q = questions[state.step];
  const value = state.answers[q.id];
  const isLast = state.step === questions.length - 1;
  const canContinue = isAnswered(q, value);

  return (
    <section className="mx-auto max-w-2xl px-5 py-10 sm:py-14">
      <ProgressBar step={state.step} total={questions.length} />

      <div className="mt-10 min-h-[22rem]">
        <QuestionCard
          question={q}
          value={value}
          onChange={(v) => dispatch({ type: "SET_ANSWER", id: q.id, value: v })}
        />
      </div>

      <div className="mt-10 flex items-center justify-between">
        <button
          onClick={() => dispatch({ type: "BACK" })}
          className="rounded-full px-5 py-3 font-semibold text-ink/70 transition hover:bg-mist/60"
        >
          Back
        </button>

        <div className="flex items-center gap-3">
          {!q.required && !value && (
            <button
              onClick={() => dispatch({ type: "NEXT" })}
              className="rounded-full px-5 py-3 font-semibold text-ink/70 transition hover:bg-mist/60"
            >
              Skip
            </button>
          )}
          <button
            onClick={() => dispatch({ type: "NEXT" })}
            disabled={!canContinue}
            className="rounded-full bg-ink px-7 py-3 font-semibold text-lilac transition hover:bg-ink/85 disabled:cursor-not-allowed disabled:opacity-30"
          >
            {isLast ? "See my summary" : "Next"}
          </button>
        </div>
      </div>
    </section>
  );
}
