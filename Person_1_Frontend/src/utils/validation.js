/** Returns true if the question has a valid answer (or is optional). */
export function isAnswered(question, value) {
  if (!question.required) return true;

  switch (question.type) {
    case "single":
      return Boolean(value);
    case "multi":
      return Array.isArray(value) && value.length > 0;
    case "text":
    case "textarea":
      return typeof value === "string" && value.trim().length >= (question.minLength ?? 1);
    default:
      return true; // sliders always have a default
  }
}
