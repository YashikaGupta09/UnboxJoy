# Person 4 — Gift Box Builder, Cart & Backend

## Purpose
This module turns product recommendations into a personalized, multi-sensory gift box with custom packaging, real-time budget validation, automated sensory assembly, and cart checkout order summaries.

It forms **Module 4** of the **UnboxJoy** project.

---

## Deliverables & Features
1. **Interactive Gift Box Creation Interface (`frontend/`)**:
   - Modern, responsive SPA styled with Tailwind CSS.
   - 5 Compartment slots tracking sensory coverage (Sight, Sound, Smell, Taste, Touch).
   - Real-time budget meter progress bar with color-coded safety indicators (Green, Amber, Red).
   - Sensory harmony gauge (measuring multi-sensory balance from 0% to 100%).
   - 4 aesthetic packaging options inspired by 2025 packaging trends (*Eco-Kraft Keepsake*, *Midnight Matte Luxe*, *Pastel Blossom*, *Minimalist Velvet Chest*).
   - Personalized handwritten greeting card drawer with live preview.
   - 3D interactive unboxing preview modal with unfasten ribbon animation and item reveal.
2. **Backend REST APIs (`backend/app.py`)**:
   - Built on Python Flask with CORS support.
   - Comprehensive endpoints for product recommendations, box CRUD, smart auto-assembly, packaging selection, and cart checkout.
3. **Core Business Logic (`backend/`)**:
   - `box_assembler.py`: State manager & bounded knapsack auto-assembly algorithm with strict multi-brand diversity enforcement.
   - `pricing.py`: Subtotal, packaging fee, 5% GST computation, and budget utilization.
   - `packaging.py`: Packaging catalog and greeting card templates.
   - `cart.py`: Order receipt and unboxing sequence generator.
4. **Automated Test Suite & Evaluation (`tests/` & `test_results/`)**:
   - 16 comprehensive unit and integration tests with 100% pass rate.
   - Evaluation reports for TC01 through TC05.

---

## Directory Structure
```
Gift_Box_Builder/
├── backend/
│   ├── __init__.py
│   ├── app.py                 # Flask REST API server
│   ├── box_assembler.py       # Box state & knapsack auto-assembly
│   ├── cart.py                # Cart manager & receipt generator
│   ├── models.py              # Dataclasses & serializations
│   ├── packaging.py           # Packaging styles catalog
│   └── pricing.py             # Pricing, tax, & sensory coverage
├── frontend/
│   ├── index.html             # Responsive UI with Tailwind CSS
│   ├── app.js                 # Interactive state management
│   └── styles.css             # Unboxing & 3D animations
├── inputs/
│   └── sample_recommendations.json # Realistic Person 3 contract input
├── documentation/
│   ├── system_architecture.md # Architecture & mathematical formulation
│   └── integration_contract.md# Upstream & downstream contracts
├── tests/
│   ├── test_pricing.py        # Pricing & sensory coverage tests
│   ├── test_box_assembler.py  # Box CRUD & auto-assembly tests
│   ├── test_cart.py           # Cart & order summary tests
│   ├── test_api.py            # Flask API endpoint tests
│   └── test_e2e_integration.py# Full customer journey E2E test
├── test_results/              # TC01-TC05 evaluation records
├── requirements.txt           # Python dependencies
├── run_tests.py               # Automated test runner & artifact generator
└── README.md
```

---

## Quickstart Guide

### 1. Install Dependencies
```bash
pip install -r Gift_Box_Builder/requirements.txt
```

### 2. Run the Web Application
```bash
python3 Gift_Box_Builder/backend/app.py
```
Open **http://localhost:5000** in your browser to interact with the Gift Box Builder!

### 3. Run Automated Tests & Evaluations
```bash
python3 Gift_Box_Builder/run_tests.py
```
Runs all 16 tests and updates evaluation logs in `test_results/`.

---

## Team Integration Summary
- **Upstream**: Ingests recipient profile from Person 2 and multi-brand product recommendations from Person 3.
- **Internal**: Handles box customization, smart assembly, budget constraints, and aesthetic packaging.
- **Downstream**: Produces confirmed order receipt, financial breakdown, and unboxing sequence for the customer.
