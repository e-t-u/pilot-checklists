import json
import unittest
from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = REPO_ROOT / "templates"
SCRIPTS_DIR = REPO_ROOT / "scripts"

sys.path.insert(0, str(SCRIPTS_DIR))
import checklist_cli

class TestPilotChecklists(unittest.TestCase):
    def test_templates_exist(self):
        templates = list(TEMPLATES_DIR.glob("*.json"))
        self.assertGreaterEqual(len(templates), 7)

    def test_template_schema_and_integrity(self):
        for p in TEMPLATES_DIR.glob("*.json"):
            with open(p, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.assertIn("title", data)
            self.assertIn("code", data)
            self.assertIn("mode", data)
            self.assertIn("trigger", data)
            self.assertIn("phases", data)
            self.assertIsInstance(data["phases"], list)
            self.assertGreater(len(data["phases"]), 0)
            for phase in data["phases"]:
                self.assertIn("name", phase)
                self.assertIn("items", phase)
                self.assertIsInstance(phase["items"], list)
                self.assertLessEqual(
                    len(phase["items"]), 9,
                    f"Phase {phase['name']} in {p.name} exceeds 9 items (Miller's law limit)"
                )
                for item in phase["items"]:
                    self.assertIn("challenge", item)
                    self.assertIn("response", item)
                    self.assertIn("killer", item)

    def test_markdown_card_exact_line_lengths(self):
        for p in TEMPLATES_DIR.glob("*.json"):
            data = checklist_cli.load_checklist(str(p))
            rendered = checklist_cli.render_markdown_card(data)
            lines = rendered.split("\n")
            self.assertEqual(lines[0], "```text")
            self.assertEqual(lines[-1], "```")
            for idx, line in enumerate(lines[1:-1]):
                self.assertEqual(
                    len(line), 70,
                    f"Line {idx+1} '{line}' in {p.name} has length {len(line)} != 70"
                )

    def test_html_rendering(self):
        for p in TEMPLATES_DIR.glob("*.json"):
            data = checklist_cli.load_checklist(str(p))
            html = checklist_cli.render_html_card(data)
            self.assertIn("<!DOCTYPE html>", html)
            self.assertIn(data["title"].upper(), html)
            self.assertIn(data["code"], html)

    def test_pdf_generation(self):
        sample = TEMPLATES_DIR / "leaving_home.json"
        data = checklist_cli.load_checklist(str(sample))
        out_pdf = REPO_ROOT / "tests" / "test_output.pdf"
        try:
            ok = checklist_cli.generate_pdf(data, str(out_pdf), theme="print")
            self.assertTrue(ok)
            self.assertTrue(out_pdf.is_file())
            self.assertGreater(out_pdf.stat().st_size, 1000)
        finally:
            if out_pdf.is_file():
                out_pdf.unlink()

if __name__ == "__main__":
    unittest.main()
