#!/usr/bin/env python3
"""Convenience launcher for Module 4: Gift Box Builder & Cart."""

import sys
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT))

from Gift_Box_Builder.backend.app import create_app

if __name__ == "__main__":
    app = create_app()
    print("\n=======================================================")
    print("  🎁 UNBOXJOY: GIFT BOX BUILDER & CART (MODULE 4)")
    print("=======================================================")
    print("  Server running at:  http://localhost:5000")
    print("  Open this link in your web browser to use the app.")
    print("  Press Ctrl+C to stop the server.")
    print("=======================================================\n")
    app.run(host="0.0.0.0", port=5000, debug=True)
