import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
QUERY_SCRIPT = ROOT / "skills" / "laravel-filament-5-ui-ux" / "scripts" / "query_visual_catalog.py"
SYNC_SCRIPT = ROOT / "skills" / "laravel-filament-5-ui-ux" / "scripts" / "sync_visual_catalog.py"
VALIDATE_SCRIPT = ROOT / "skills" / "laravel-filament-5-ui-ux" / "scripts" / "validate_visual_catalog.py"
REVIEW_SCRIPT = ROOT / "skills" / "laravel-filament-5-ui-ux" / "scripts" / "build_review_sheets.py"


def load_query_module():
    spec = importlib.util.spec_from_file_location("query_visual_catalog", QUERY_SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def load_sync_module():
    spec = importlib.util.spec_from_file_location("sync_visual_catalog", SYNC_SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def load_validate_module():
    spec = importlib.util.spec_from_file_location("validate_visual_catalog", VALIDATE_SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def load_review_module():
    spec = importlib.util.spec_from_file_location("build_review_sheets", REVIEW_SCRIPT)
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

    def test_query_filters_by_information_shape_relationship_and_responsive_context(self):
        query = load_query_module()

        result = query.query_catalog(
            surface="form",
            goal="organize-stable-groups",
            workflow="parallel",
            available_width="wide",
            information_shape="several-stable-groups",
            relationship="peer-groups",
            responsive_context="desktop-with-mobile-fallback",
        )

        self.assertEqual("vertical-tabs", result["selected_pattern"]["id"])
        self.assertEqual("several-stable-groups", result["query"]["information_shape"])


class VisualCatalogSynchronizationTests(unittest.TestCase):
    def test_discovery_does_not_duplicate_markdown_extension(self):
        sync = load_sync_module()

        pages = sync.discover_markdown_pages(
            "https://filamentphp.com/docs/5.x",
            fetch=lambda _url: '<a href="/docs/5.x/introduction/overview.md">Overview</a>',
        )

        self.assertEqual(
            ["https://filamentphp.com/docs/5.x/introduction/overview.md"],
            pages,
        )

    def test_sync_discovers_screenshots_and_preserves_existing_review(self):
        sync = load_sync_module()
        pages = {
            "https://filamentphp.com/docs/5.x/forms/overview.md": """
                # Forms
                <AutoScreenshot name=\"forms/overview\" alt=\"A settings form\" />
                <AutoScreenshot name=\"forms/new\" alt=\"A new field\" />
            """,
        }

        def fetch(url: str) -> str:
            return pages[url]

        existing = {
            "schema_version": 1,
            "screenshots": [
                {
                    "name": "forms/overview",
                    "alt": "A settings form",
                    "documentation": "https://filamentphp.com/docs/5.x/forms/overview.md",
                    "light_image": "https://filamentphp.com/docs/images/5.x/light/forms/overview.jpg",
                    "dark_image": "https://filamentphp.com/docs/images/5.x/dark/forms/overview.jpg",
                    "status": "reviewed",
                    "family": "responsive-columns",
                }
            ],
        }

        inventory = sync.build_inventory(
            ["https://filamentphp.com/docs/5.x/forms/overview.md"],
            fetch=fetch,
            existing=existing,
        )

        self.assertEqual(["forms/new", "forms/overview"], [item["name"] for item in inventory["screenshots"]])
        self.assertEqual("unreviewed", inventory["screenshots"][0]["status"])
        self.assertEqual("reviewed", inventory["screenshots"][1]["status"])
        self.assertEqual("responsive-columns", inventory["screenshots"][1]["family"])
        self.assertEqual(
            "https://filamentphp.com/docs/images/5.x/light/forms/new.jpg",
            inventory["screenshots"][0]["light_image"],
        )

    def test_sync_marks_materially_changed_evidence_unreviewed(self):
        sync = load_sync_module()
        page = "https://filamentphp.com/docs/5.x/forms/overview.md"
        existing = {
            "screenshots": [{
                "name": "forms/overview",
                "alt": "Old description",
                "documentation": page,
                "light_image": "https://filamentphp.com/docs/images/5.x/light/forms/overview.jpg",
                "dark_image": "https://filamentphp.com/docs/images/5.x/dark/forms/overview.jpg",
                "status": "reviewed",
                "family": "responsive-columns",
            }],
        }

        inventory = sync.build_inventory(
            [page],
            fetch=lambda _url: '<AutoScreenshot name="forms/overview" alt="New description" />',
            existing=existing,
        )

        self.assertEqual("unreviewed", inventory["screenshots"][0]["status"])
        self.assertNotIn("family", inventory["screenshots"][0])

    def test_inventory_output_is_stable_json(self):
        sync = load_sync_module()
        inventory = {
            "schema_version": 1,
            "screenshots": [{"name": "forms/overview", "status": "unreviewed"}],
        }

        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "inventory.json"
            sync.write_inventory(output, inventory)
            first = output.read_text()
            sync.write_inventory(output, inventory)

            self.assertEqual(first, output.read_text())
            self.assertEqual(inventory, json.loads(first))


class VisualCatalogValidationTests(unittest.TestCase):
    def test_validation_rejects_unreviewed_evidence_and_unknown_family(self):
        validate = load_validate_module()
        catalog = {
            "patterns": [{"id": "sections", "status": "reviewed", "visual_evidence": []}],
        }
        inventory = {
            "screenshots": [
                {
                    "name": "forms/new",
                    "documentation": "https://filamentphp.com/docs/5.x/forms/overview.md",
                    "light_image": "https://filamentphp.com/docs/images/5.x/light/forms/new.jpg",
                    "dark_image": "https://filamentphp.com/docs/images/5.x/dark/forms/new.jpg",
                    "status": "unreviewed",
                    "family": "unknown",
                    "decision_relevance": "decision-changing",
                }
            ]
        }

        errors = validate.validate(catalog, inventory)

        self.assertIn("forms/new is unreviewed", errors)
        self.assertIn("forms/new references unknown family unknown", errors)
        self.assertIn("forms/new needs a variant for a decision-changing screenshot", errors)

    def test_validation_rejects_missing_classification_and_crawl_contract(self):
        validate = load_validate_module()
        catalog = {"patterns": [{"id": "sections"}]}
        inventory = {
            "screenshots": [{
                "name": "forms/new",
                "documentation": "https://filamentphp.com/docs/5.x/forms/overview.md",
                "light_image": "https://filamentphp.com/docs/images/5.x/light/forms/new.jpg",
                "dark_image": "https://filamentphp.com/docs/images/5.x/dark/forms/new.jpg",
                "status": "reviewed",
                "family": "sections",
            }],
        }

        errors = validate.validate(catalog, inventory)

        self.assertIn("inventory is missing a complete crawl contract", errors)
        self.assertIn("forms/new is missing decision_relevance", errors)

    def test_validation_rejects_inventory_missing_a_manifest_screenshot(self):
        validate = load_validate_module()
        catalog = {"patterns": [{"id": "sections"}]}
        inventory = {
            "crawl": {
                "status": "complete",
                "pages": ["https://filamentphp.com/docs/5.x/forms/overview.md"],
                "manifest": {
                    "https://filamentphp.com/docs/5.x/forms/overview.md": ["forms/new", "forms/overview"],
                },
            },
            "screenshots": [{
                "name": "forms/overview",
                "documentation": "https://filamentphp.com/docs/5.x/forms/overview.md",
                "light_image": "https://filamentphp.com/docs/images/5.x/light/forms/overview.jpg",
                "dark_image": "https://filamentphp.com/docs/images/5.x/dark/forms/overview.jpg",
                "status": "reviewed",
                "family": "sections",
                "decision_relevance": "non-decision-changing",
            }],
        }

        errors = validate.validate(catalog, inventory)

        self.assertIn("inventory does not match its crawl manifest", errors)


class VisualCatalogReviewSheetTests(unittest.TestCase):
    def test_review_sheet_groups_downloaded_images_in_temporary_output(self):
        review = load_review_module()
        screenshots = [
            {
                "name": "schemas/layout/tabs/vertical",
                "family": "vertical-tabs",
                "alt": "Vertical tabs",
                "light_image": "https://example.test/vertical.jpg",
                "status": "reviewed",
            }
        ]

        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory)
            sheet = review.build_review_sheet(
                screenshots,
                output,
                download=lambda _url: b"image-bytes",
            )

            self.assertEqual(output / "index.html", sheet)
            self.assertIn("vertical-tabs", sheet.read_text())
            self.assertEqual(b"image-bytes", (output / "images" / "schemas-layout-tabs-vertical.jpg").read_bytes())


if __name__ == "__main__":
    unittest.main()
