import ChoiceInput from "./inputs/ChoiceInput.jsx";
import TextInput from "./inputs/TextInput.jsx";
import SliderInput from "./inputs/SliderInput.jsx";
import SpectrumInput from "./inputs/SpectrumInput.jsx";

const inputs = {
  single: ChoiceInput,
  multi: ChoiceInput,
  text: TextInput,
  textarea: TextInput,
  slider: SliderInput,
  spectrum: SpectrumInput,
};

export default function QuestionCard({ question, value, onChange }) {
  const Input = inputs[question.type];
  return (
    <div key={question.id} className="animate-swap">
      <h2 className="text-2xl font-bold leading-tight sm:text-3xl">{question.title}</h2>
      {question.subtitle && <p className="mb-6 mt-2 text-ink/65">{question.subtitle}</p>}
      <div className={question.subtitle ? "" : "mt-6"}>
        <Input question={question} value={value} onChange={onChange} />
      </div>
    </div>
  );
}
