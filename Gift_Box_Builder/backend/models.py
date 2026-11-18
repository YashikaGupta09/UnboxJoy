"""Data models for the Gift Box Builder, Packaging, and Pricing engine."""

from dataclasses import dataclass, field, asdict
from typing import List, Dict, Optional, Any
from datetime import datetime


@dataclass
class Product:
    """Represents a product item from the recommendation catalog."""
    product_id: str
    product_name: str
    brand: str
    category: str  # sight, sound, smell, taste, touch
    price: float
    currency: str = "INR"
    description: str = ""
    image_url: str = ""
    product_url: str = ""
    emotional_tags: List[str] = field(default_factory=list)
    interest_tags: List[str] = field(default_factory=list)
    match_score: Optional[float] = None
    match_rationale: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Product":
        return cls(
            product_id=data.get("product_id", ""),
            product_name=data.get("product_name", ""),
            brand=data.get("brand", ""),
            category=data.get("category", "").lower(),
            price=float(data.get("price", 0)),
            currency=data.get("currency", "INR"),
            description=data.get("description", ""),
            image_url=data.get("image_url", ""),
            product_url=data.get("product_url", ""),
            emotional_tags=list(data.get("emotional_tags", [])),
            interest_tags=list(data.get("interest_tags", [])),
            match_score=data.get("match_score"),
            match_rationale=data.get("match_rationale")
        )


@dataclass
class PackagingOption:
    """Represents a packaging design style inspired by modern gift packaging trends."""
    id: str
    name: str
    price: float
    material: str
    description: str
    tagline: str
    color_theme: str
    accent_color: str
    ribbon_color: str
    preview_icon: str
    sustainability_badge: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class GreetingCard:
    """Custom personalized greeting card placed inside the box."""
    recipient_name: str = ""
    sender_name: str = ""
    message: str = ""
    font_style: str = "calligraphy"  # calligraphy, modern, handwritten
    card_theme: str = "botanical"

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class BoxPricing:
    """Itemized financial breakdown for the gift box."""
    items_subtotal: float
    packaging_fee: float
    tax_gst: float  # 5% GST on gift hampers
    discount: float
    grand_total: float
    target_budget: float
    remaining_budget: float
    budget_exceeded: bool
    budget_percentage: float
    currency: str = "INR"

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class SensoryCoverage:
    """Tracks coverage across the five sensory dimensions."""
    sight: int = 0
    sound: int = 0
    smell: int = 0
    taste: int = 0
    touch: int = 0
    covered_senses: List[str] = field(default_factory=list)
    sensory_harmony_score: float = 0.0  # Percentage 0-100%

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
