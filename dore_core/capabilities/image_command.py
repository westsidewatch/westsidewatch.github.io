from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass
from typing import Any

_IMAGE_VERB = re.compile(r"(?:生成|產生|制作|製作|画|畫|绘制|繪製|做一張|做一幅|create|generate|draw|render)", re.I)
_IMAGE_NOUN = re.compile(r"(?:圖|图片|圖片|插圖|插画|插畫|封面|海報|poster|image|illustration|cover)", re.I)


@dataclass(frozen=True)
class ImageCommand:
    message: str
    subject: str
    brief: dict[str, Any]
    seed: int


def is_image_command(message: str) -> bool:
    text = str(message or "").strip()
    return bool(text and _IMAGE_VERB.search(text) and _IMAGE_NOUN.search(text))


def parse_image_command(message: str) -> ImageCommand:
    text = str(message or "").strip()
    if not is_image_command(text):
        raise ValueError("message is not an image-generation command")
    subject = re.sub(r"^(?:多雷[，,:：\s]*)?", "", text, flags=re.I)
    brief: dict[str, Any] = {}
    if re.search(r"金黑|gold\s*(?:and|\+|/)\s*black", text, re.I):
        brief.update({"dominant_ink": "gold", "accent_ink": "black", "ink_mode": "chromatic+black"})
    elif re.search(r"紅黑|red\s*(?:and|\+|/)\s*black", text, re.I):
        brief.update({"dominant_ink": "warm-red", "accent_ink": "black", "ink_mode": "chromatic+black"})
    if re.search(r"大量留白|大面積留白|large negative space|lots of negative space", text, re.I):
        brief["empty_paper_ratio"] = 0.45
    elif re.search(r"留白|negative space", text, re.I):
        brief["empty_paper_ratio"] = 0.35
    digest = hashlib.sha256(text.encode("utf-8")).digest()
    seed = int.from_bytes(digest[:4], "big")
    return ImageCommand(message=text, subject=subject, brief=brief, seed=seed)
