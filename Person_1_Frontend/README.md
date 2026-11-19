# Person 1: Frontend & Questionnaire (UnboxJoy)

React + Vite + Tailwind CSS single-page UI.

## Run
```bash
cd Person_1_Frontend
npm install
npm run dev      # http://localhost:5173
npm run build    # production build in dist/
```

## Where things are
- `src/data/questions.js`: every question (edit here to change content)
- `src/context/QuestionnaireContext.jsx`: state (view, step, answers)
- `src/utils/buildResponse.js`: builds the final structured response object
- `src/services/api.js`: the ONE place that talks to the backend (set `VITE_API_URL`)

## Output contract (handed to the AI/backend team)
```json
{
  "meta": { "version": "1.0", "completedAt": "ISO date" },
  "recipient": { "name": "string", "relationship": "partner|parent|sibling|friend|colleague|other" },
  "occasion": "birthday|anniversary|festival|thank_you|get_well|just_because",
  "favouriteMemory": "string",
  "experiences": ["..."],
  "senses": ["scent|taste|touch|sound|sight"],
  "emotions": ["..."],
  "personality": { "calmToAdventurous": 1-10, "practicalToSentimental": 1-10, "classicToQuirky": 1-10 },
  "budget": { "amount": 2500, "currency": "INR" },
  "avoid": "string"
}
```
