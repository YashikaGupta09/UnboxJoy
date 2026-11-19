import { useEffect } from "react";
import { useQuestionnaire } from "./context/QuestionnaireContext.jsx";
import Navbar from "./components/layout/Navbar.jsx";
import Footer from "./components/layout/Footer.jsx";
import Hero from "./components/home/Hero.jsx";
import HowItWorks from "./components/home/HowItWorks.jsx";
import Questionnaire from "./components/questionnaire/Questionnaire.jsx";
import Summary from "./components/results/Summary.jsx";

export default function App() {
  const { state } = useQuestionnaire();

  // Single-page "views": home -> quiz -> summary. No router needed.
  useEffect(() => {
    window.scrollTo({ top: 0 });
  }, [state.view]);

  return (
    <div className="flex min-h-screen flex-col">
      <Navbar />
      <main className="flex-1">
        {state.view === "home" && (
          <>
            <Hero />
            <HowItWorks />
          </>
        )}
        {state.view === "quiz" && <Questionnaire />}
        {state.view === "summary" && <Summary />}
      </main>
      <Footer />
    </div>
  );
}
