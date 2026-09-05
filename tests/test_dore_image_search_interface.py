from __future__ import annotations

import unittest
from pathlib import Path

from dore_core.capabilities.image_command import is_image_command, parse_image_command

ROOT = Path(__file__).resolve().parents[1]


class DoreImageSearchInterfaceTests(unittest.TestCase):
    def test_chinese_generation_command_routes_to_image(self):
        q = "多雷，生成一張耶路撒冷黎明的封面圖，金黑雙色，大量留白"
        self.assertTrue(is_image_command(q))
        cmd = parse_image_command(q)
        self.assertEqual(cmd.brief["dominant_ink"], "gold")
        self.assertEqual(cmd.brief["accent_ink"], "black")
        self.assertEqual(cmd.brief["empty_paper_ratio"], 0.45)
        self.assertGreaterEqual(cmd.seed, 0)

    def test_normal_question_does_not_trigger_generation(self):
        self.assertFalse(is_image_command("馬太福音第六章為什麼說一天的憂慮一天當就夠了？"))
        self.assertFalse(is_image_command("找一張現有的耶路撒冷圖片"))

    def test_search_ai_router_preempts_conversation_handler(self):
        js = (ROOT / "static/dore/dore-image-command.js").read_text(encoding="utf-8")
        self.assertIn("http://127.0.0.1:8790/generate", js)
        self.assertIn("window.addEventListener('submit',intercept,true)", js)
        self.assertIn("X-Dore-Origin':'dore-search", js)

    def test_existing_search_load_chain_loads_image_router(self):
        js = (ROOT / "static/dore/dore-video-subtitle-router.js").read_text(encoding="utf-8")
        self.assertIn("/dore/dore-image-command.js", js)

    def test_local_api_is_loopback_and_origin_gated(self):
        py = (ROOT / "scripts/dore_image_local_api.py").read_text(encoding="utf-8")
        self.assertIn('HOST = "127.0.0.1"', py)
        self.assertIn('PORT = 8790', py)
        self.assertIn('X-Dore-Origin', py)
        self.assertIn('image.generate', py)


if __name__ == "__main__":
    unittest.main()
