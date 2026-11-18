# UnboxJoy — AI-Guided Sensory Gift Concierge

An intelligent, multi-sensory gift curation and packaging platform designed by a 4-person engineering team.

## Project Architecture & Team Division

```
Person 1: Frontend & Questionnaire
   Collects emotional, sensory, and recipient memories
        │
        ▼
Person 2: AI Personalization Engine (Person_2_AI_Personalization/)
   Interprets responses, extracts personality traits, emotional theme, and sensory profile
        │
        ▼
Person 3: Product Database & Matching (UnboxJoy/product_recommendation/)
   Multi-brand product catalogue across the 5 senses (Sight, Sound, Smell, Taste, Touch)
        │
        ▼
Person 4: Gift Box Builder, Cart & Backend (Gift_Box_Builder/)
   Custom box builder, 2025 packaging aesthetics, budget meter, auto-assembly, and cart checkout
```

## Module 4: Gift Box Builder, Cart & Backend
- **Location**: `Gift_Box_Builder/`
- **Features**: Interactive Tailwind SPA, Flask REST API, 4 modern packaging styles (Eco-Kraft, Midnight Luxe, Pastel Blossom, Velvet Chest), real-time budget meter, sensory harmony tracker, and 3D unboxing preview.
- **Documentation**: [Person 4 Architecture](Gift_Box_Builder/documentation/system_architecture.md) | [Integration Contract](Gift_Box_Builder/documentation/integration_contract.md)
- **Quickstart**:
  ```bash
  python3 Gift_Box_Builder/backend/app.py
  ```
  Visit `http://localhost:5000` to launch the Gift Box Concierge.
