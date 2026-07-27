import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
QUERY_SCRIPT = ROOT / "skills" / "laravel-filament-5-ui-ux" / "scripts" / "query_visual_catalog.py"


def load_query_module():
    spec = importlib.util.spec_from_file_location("query_visual_catalog", QUERY_SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class VisualCatalogQueryTests(unittest.TestCase):
    def test_wide_parallel_settings_groups_prioritize_vertical_tabs(self):
        query = load_query_module()

        result = query.query_catalog(
            surface="form",
            goal="organize-stable-groups",
            workflow="parallel",
            available_width="wide",
        )

        self.assertEqual("vertical-tabs", result["selected_pattern"]["id"])
        self.assertEqual(
            ["vertical-tabs", "horizontal-tabs", "sections"],
            [candidate["id"] for candidate in result["candidates"]],
        )
        self.assertEqual(
            "schemas/layout/tabs/vertical",
            result["selected_pattern"]["visual_evidence"][0]["screenshot"],
        )
        self.assertIn(
            "several stable groups",
            result["selected_pattern"]["selection_signals"],
        )


if __name__ == "__main__":
    unittest.main()
