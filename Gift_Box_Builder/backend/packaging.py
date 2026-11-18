"""Creative Packaging Options & Greeting Card Catalog for Module 4.
Inspired by modern packaging trends: eco-kraft boards, magnetic closures,
and sensory textures (elitecustomboxes.com reference).
"""

from typing import Dict, List, Optional
try:
    from .models import PackagingOption
except (ImportError, ValueError):
    from models import PackagingOption


PACKAGING_CATALOG: Dict[str, PackagingOption] = {
    "eco_kraft": PackagingOption(
        id="eco_kraft",
        name="Eco-Friendly Kraft Keepsake",
        price=99.0,
        material="100% Recycled Kraft Board & Jute Twine",
        description="Earthy and sustainable rustic kraft gift box with herbal crinkle paper fill and hand-tied jute twine.",
        tagline="Sustainable, organic, and heartfelt.",
        color_theme="#D2B48C",
        accent_color="#8B5A2B",
        ribbon_color="#705335",
        preview_icon="📦🌱",
        sustainability_badge="100% Biodegradable & Recyclable"
    ),
    "midnight_luxe": PackagingOption(
        id="midnight_luxe",
        name="Midnight Matte Luxe Box",
        price=199.0,
        material="Rigid Paperboard with Soft-Touch Matte & Gold Foil",
        description="Premium midnight-blue rigid box with magnetic latch closure and embossed metallic gold monogram finish.",
        tagline="Opulent elegance with modern sophistication.",
        color_theme="#1A2A3A",
        accent_color="#D4AF37",
        ribbon_color="#C5A059",
        preview_icon="✨🎁",
        sustainability_badge="FSC-Certified Luxury Rigid Board"
    ),
    "pastel_blossom": PackagingOption(
        id="pastel_blossom",
        name="Pastel Blossom Celebration",
        price=149.0,
        material="Smooth Pastel Finish with Double-Faced Satin Ribbon",
        description="Chic blush-pink celebration box wrapped with a double-faced champagne satin bow and floral embossed liner.",
        tagline="Joyful, warm, and picture-perfect for celebrations.",
        color_theme="#F7D8D5",
        accent_color="#E07A5F",
        ribbon_color="#E6A57E",
        preview_icon="🌸🎀",
        sustainability_badge="FSC Mixed Sourced Board"
    ),
    "velvet_chest": PackagingOption(
        id="velvet_chest",
        name="Minimalist Velvet Chest",
        price=249.0,
        material="Rigid Wooden Core with Deep Velvet Interior",
        description="Heirloom-grade keepsake chest lined with royal navy micro-velvet cushioning and a vintage brass latch.",
        tagline="A timeless keepsake designed to be cherished for years.",
        color_theme="#0F172A",
        accent_color="#93C5FD",
        ribbon_color="#1E3A8A",
        preview_icon="👑💎",
        sustainability_badge="Handcrafted Reusable Keepsake"
    )
}

DEFAULT_PACKAGING_ID = "eco_kraft"


def get_all_packaging_options() -> List[PackagingOption]:
    """Returns all available packaging styles."""
    return list(PACKAGING_CATALOG.values())


def get_packaging_by_id(packaging_id: str) -> PackagingOption:
    """Retrieves packaging option by id, falling back to default."""
    return PACKAGING_CATALOG.get(packaging_id, PACKAGING_CATALOG[DEFAULT_PACKAGING_ID])
