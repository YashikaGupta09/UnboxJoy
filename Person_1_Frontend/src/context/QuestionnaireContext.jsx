import { createContext, useContext, useEffect, useMemo, useReducer } from "react";
import { questions } from "../data/questions.js";
import { isAnswered } from "../utils/validation.js";

const STORAGE_KEY = "unboxjoy:answers";

function loadSaved() {
  try {
    const raw = sessionStorage.getItem(STORAGE_KEY);
    return raw ? JSON.parse(raw) : {};
  } catch {
    return {};
  }
}

const initialState = { view: "home", step: 0, answers: loadSaved() };

function reducer(state, action) {
  switch (action.type) {
    case "START":
      return { ...state, view: "quiz", step: 0 };
    case "SET_ANSWER":
      return { ...state, answers: { ...state.answers, [action.id]: action.value } };
    case "NEXT": {
      const q = questions[state.step];
      if (!isAnswered(q, state.answers[q.id])) return state;
      if (state.step === questions.length - 1) return { ...state, view: "summary" };
      return { ...state, step: state.step + 1 };
    }
    case "BACK":
      if (state.step === 0) return { ...state, view: "home" };
      return { ...state, step: state.step - 1 };
    case "EDIT":
      return { ...state, view: "quiz", step: 0 };
    case "RESET":
      return { view: "home", step: 0, answers: {} };
    default:
      return state;
  }
}

const Ctx = createContext(null);

export function QuestionnaireProvider({ children }) {
  const [state, dispatch] = useReducer(reducer, initialState);

  // Keep answers if the page is refreshed mid-quiz.
  useEffect(() => {
    try {
      sessionStorage.setItem(STORAGE_KEY, JSON.stringify(state.answers));
    } catch {
      /* storage unavailable, ignore */
    }
  }, [state.answers]);

  const value = useMemo(() => ({ state, dispatch }), [state]);
  return <Ctx.Provider value={value}>{children}</Ctx.Provider>;
}

export function useQuestionnaire() {
  const ctx = useContext(Ctx);
  if (!ctx) throw new Error("useQuestionnaire must be used inside QuestionnaireProvider");
  return ctx;
}
