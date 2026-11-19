import { questions } from "../data/questions.js";

/**
 * Turns raw answers ({ [questionId]: value }) into the structured object
 * that gets handed to the AI / backend team.
 */
export function buildResponse(answers) {
  const get = (id) => {
    const q = questions.find((x) => x.id === id);
    return answers[id] ?? q?.defaultValue ?? null;
  };

  return {
    meta: {
      version: "1.0",
      completedAt: new Date().toISOString(),
    },
    recipient: {
      name: (get("name") || "").trim(),
      relationship: get("relationship"),
    },
    occasion: get("occasion"),
    favouriteMemory: (get("memory") || "").trim(),
    experiences: get("experiences") || [],
    senses: get("senses") || [],
    emotions: get("emotions") || [],
    personality: get("personality"),
    budget: { amount: Number(get("budget")), currency: "INR" },
    avoid: (get("avoid") || "").trim(),
  };
}
