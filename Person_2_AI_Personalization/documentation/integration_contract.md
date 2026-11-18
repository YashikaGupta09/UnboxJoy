# Person 2 Integration Contract

## 1. Upstream input: Person 1 to Person 2

Person 1 supplies a JSON questionnaire.

Example:

```json
{
  "relationship": "best friend",
  "personality": ["creative", "emotional"],
  "memories": "We travelled together and took photographs.",
  "interests": ["photography", "travel"],
  "sensory_preferences": ["sight", "touch"],
  "desired_emotion": "nostalgia",
  "occasion": "birthday",
  "budget_inr": 1500
}
```

The example is illustrative. The frontend and AI modules must agree
on exact field names, types and allowed values during integration.

## 2. Person 2 processing

Person 2 validates the questionnaire, interprets the recipient's
preferences and desired emotion, and generates a structured
personalization result.

The current implementation uses Pydantic models and a Groq model
request constrained by a JSON schema.

## 3. Structured output contract

The top-level result contains:

- `recipient_profile`
- `recommendation_directions`
- `match_rationales`
- `missing_information`
- `safety_note`

The recipient profile contains:

- `relationship`
- `personality_descriptors`
- `interests`
- `emotional_theme`
- `sensory_preferences`
- `gift_style`
- `matching_tags`
- `budget_inr`
- `profile_summary`

The `matching_tags` object contains:

- `interest_tags`
- `emotion_tags`
- `sensory_tags`
- `personality_tags`
- `style_tags`
- `occasion_tags`

## 4. Downstream handoff: Person 2 to Person 3

Person 3 should use the recipient profile, matching tags,
recommendation directions and match rationales as inputs to catalogue
matching.

Person 2 does not return actual catalogue products, product brands,
merchants or product prices.

The budget is contextual input for downstream matching. Person 3
remains responsible for checking actual catalogue prices.

## 5. Integration checks

Before declaring end-to-end integration complete, verify:

1. Person 1 field names and data types match the Person 2 input validator.
2. All sensory preference values are represented consistently.
3. The desired emotion and occasion reach Person 2 correctly.
4. Person 2 returns valid JSON matching the current schema.
5. Person 3 can consume the structured output without renaming fields.
6. Budget information is passed correctly.
7. Missing or invalid questionnaire fields produce controlled validation errors.

## 6. Current limitation

The sample contract is available, but final frontend integration depends
on the actual JSON payload supplied by Person 1. Confirm the live
payload before declaring the complete system integrated.
