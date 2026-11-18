# Person 2 — AI Personalization Engine

## Purpose

This module interprets a gift questionnaire and generates a structured
recipient profile, emotional theme, sensory preferences, matching tags,
recommendation directions and match rationales.

It is the AI and personalization layer of the AI-Guided Sensory Gift
Concierge project.

## Ownership and boundaries

Person 2 owns questionnaire interpretation and personalization.

Person 2 does not select actual products, brands, merchants or prices.
Actual catalogue matching is handled by Person 3.

## Main implementation

- `notebook/Person_2_AI_Personalization.ipynb` — Colab implementation.
- `inputs/` — sample questionnaire input.
- `outputs/` — generated personalization results.
- `test_results/` — evaluation and test-run records.
- `documentation/` — architecture and integration documentation.

## Technology

- Python
- Google Colab
- Google Drive
- Groq API
- Pydantic

The notebook retrieves the Groq API key from Colab Secrets.
Do not place API keys or access tokens in source files.

## Running the notebook

1. Open the notebook in Google Colab.
2. Install the dependencies listed in `requirements.txt`.
3. Mount Google Drive if using the shared Drive workflow.
4. Add `GROQ_API_KEY` to Colab Secrets and enable notebook access.
5. Run the notebook cells in order.
6. Supply a questionnaire matching the input contract.

The notebook copy in this repository has saved cell outputs cleared.
The original working notebook remains in the project owner's Google Drive.

## Validation

The notebook includes synthetic evaluation cases and local validation
tests. The saved test records are included in `test_results/`.

Passing local validation tests establishes structural and input-validation
correctness. It does not independently establish real-world recommendation
quality or complete frontend-to-backend integration.

## Team integration

- Person 1 supplies questionnaire data.
- Person 2 generates a structured personalization result.
- Person 3 uses the personalization output to match catalogue products.
- Person 4 handles the gift box and backend workflow.

See `documentation/integration_contract.md`.
