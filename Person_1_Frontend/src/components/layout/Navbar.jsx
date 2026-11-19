import { useQuestionnaire } from "../../context/QuestionnaireContext.jsx";

export default function Navbar() {
  const { state, dispatch } = useQuestionnaire();

  return (
    <header className="border-b border-mist bg-lilac/90 backdrop-blur">
      <div className="mx-auto flex max-w-5xl items-center justify-between px-5 py-4">
        <button
          onClick={() => dispatch({ type: "RESET" })}
          className="font-display text-2xl font-extrabold tracking-tight"
          aria-label="UnboxJoy home"
        >
          Unbox<span className="text-rose">Joy</span>
        </button>

        {state.view === "home" && (
          <button
            onClick={() => dispatch({ type: "START" })}
            className="rounded-full bg-ink px-5 py-2 text-sm font-semibold text-lilac transition hover:bg-ink/85"
          >
            Build a gift box
          </button>
        )}
      </div>
    </header>
  );
}
