# Person 2 — System Architecture

## 1. Position in the overall project

Person 2 is the AI and personalization layer between the questionnaire
frontend (Person 1) and product matching (Person 3).

## 2. Processing workflow

1. Receive questionnaire JSON from Person 1.
2. Validate required fields and input types.
3. Construct the prompt using the questionnaire information.
4. Send the request to the Groq language model.
5. Request a structured JSON response using the defined schema.
6. Validate the response using Pydantic.
7. Produce the recipient profile and recommendation directions.
8. Save the personalization result.
9. Pass the structured result to Person 3.

## 3. Input information

The questionnaire contract includes:

- Relationship
- Personality
- Memories
- Interests
- Sensory preferences
- Desired emotion
- Occasion
- Budget in INR

## 4. Output information

The structured output includes:

- Recipient profile
- Personality descriptors
- Interests
- Emotional theme
- Sensory preferences
- Gift style
- Matching tags
- Budget
- Profile summary
- Recommendation directions
- Match rationales
- Missing information
- Safety note

## 5. Matching tag categories

The revised schema groups matching tags into:

- interest_tags
- emotion_tags
- sensory_tags
- personality_tags
- style_tags
- occasion_tags

## 6. Technology and dependencies

- Python and Google Colab for execution
- Groq API for language-model inference
- Pydantic for structured data validation
- Google Drive for shared files and outputs

## 7. Responsibility boundary

Person 2 generates personalization signals and broad recommendation
directions. Person 3 owns actual product catalogue matching, including
specific products, brands, merchants and prices.

## 8. Validation boundary

Local validation tests check structural and input-validation behaviour.
Synthetic evaluations provide test evidence but do not replace
end-to-end integration testing or human evaluation of recommendation quality.
