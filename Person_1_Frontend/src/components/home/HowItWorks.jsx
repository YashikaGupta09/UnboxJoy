const steps = [
  { title: "Tell us the story", text: "Share a memory and what they enjoy." },
  { title: "Set the feeling", text: "Choose the senses and emotions the box should hit." },
  { title: "Get a curated box", text: "We assemble products from multiple brands within your budget." },
];

export default function HowItWorks() {
  return (
    <section className="border-t border-mist bg-white">
      <div className="mx-auto max-w-5xl px-5 py-16">
        <h2 className="text-2xl font-bold sm:text-3xl">How it works</h2>
        {/* This content is a real sequence, so numbering is meaningful here */}
        <ol className="mt-8 grid gap-8 sm:grid-cols-3">
          {steps.map((s, i) => (
            <li key={s.title} className="flex gap-4">
              <span className="flex h-9 w-9 shrink-0 items-center justify-center rounded-full bg-saffron font-display font-bold">
                {i + 1}
              </span>
              <div>
                <h3 className="font-bold">{s.title}</h3>
                <p className="mt-1 text-ink/70">{s.text}</p>
              </div>
            </li>
          ))}
        </ol>
      </div>
    </section>
  );
}
