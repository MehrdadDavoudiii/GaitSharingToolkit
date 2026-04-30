
from __future__ import annotations
import os, sys, json
from pathlib import Path

# AppData directory

APP_DIR  = Path(__file__).parent
DATA_DIR = APP_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)
DB_PATH  = APP_DIR / "gait_dataset.db"

_SETTINGS_PATH = APP_DIR / "gait_settings.json"

def load_settings() -> dict:
    try:
        return json.loads(_SETTINGS_PATH.read_text(encoding="utf-8"))
    except Exception:
        return {}

def save_settings(data: dict) -> None:
    current = load_settings()
    current.update(data)
    _SETTINGS_PATH.write_text(
        json.dumps(current, indent=2, ensure_ascii=False), encoding="utf-8"
    )

# User / institution info
USER_INFO = {
    "name":        "Mehrdad Davoudi",
    "title":       "Associate Researcher",
    "institution": "University Children's Hospital Basel (UKBB)",
    "location":    "Basel, Switzerland",
    "email":       "Mehrdaddavoodi15@yahoo.com, Mehrdad.davoudi@ukbb.ch",
    "LinkedIn":    "https://www.linkedin.com/in/mehrdad-davoudi-profile",
}

# User photo
def _find_photo() -> Path | None:
    for ext in [".png", ".ico", ".jpg", ".jpeg"]:
        for candidate in [
            Path(__file__).parent / f"user_photo{ext}",
            APP_DIR / f"user_photo{ext}",
        ]:
            if candidate.exists():
                return candidate
    return None

USER_PHOTO_PATH = _find_photo()

# UI colour palette (UKBB Theme)
PALETTE = {
    "bg":         "#F0F2F5",
    "surface":    "#FFFFFF",
    "primary":    "#2D3436",
    "primary_lt": "#636E72",
    "accent":     "#9CBE20",
    "accent_dk":  "#7A9A10",
    "text":       "#2D3436",
    "text_muted": "#636E72",
    "border":     "#DFE6E9",
    "alt_row":    "#F8FAF0",
    "tag_bg":     "#E6F0C2",
    "tag_fg":     "#333333",
    "log_bg":     "#1E272E",
    "log_fg":     "#D2DAE2",
    "warning":    "#D63031",
    "success":    "#00B894",
    "info":       "#0984E3",
    "sidebar":    "#2D3436",
    "sidebar_hover": "#3D4446",
    "sidebar_active": "#9CBE20",
}
