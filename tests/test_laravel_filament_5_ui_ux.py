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

    def test_sequential_workflow_prioritizes_a_wizard(self):
        query = load_query_module()

        result = query.query_catalog(
            surface="form",
            goal="complete-required-sequence",
            workflow="sequential",
            available_width="standard",
            information_shape="dependent-steps",
            relationship="ordered-steps",
            responsive_context="mobile-first",
        )

        self.assertEqual("wizard", result["selected_pattern"]["id"])
        self.assertIn("horizontal-tabs", result["selected_pattern"]["alternatives"])

    def test_query_exposes_variant_level_composition_decisions(self):
        query = load_query_module()

        result = query.query_catalog(
            surface="form",
            goal="increase-information-density",
            workflow="parallel",
            available_width="wide",
            information_shape="repetitive-low-risk-fields",
            relationship="closely-related-fields",
            responsive_context="desktop-with-mobile-fallback",
        )

        self.assertEqual("dense-layout", result["selected_pattern"]["id"])
        variants = {item["id"]: item for item in result["selected_pattern"]["variant_decisions"]}
        self.assertIn("no-gap", variants)
        self.assertIn("would blur labels", " ".join(variants["no-gap"]["avoid_when"]))


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

    def test_sync_deduplicates_reused_screenshots(self):
        sync = load_sync_module()
        first_page = "https://filamentphp.com/docs/5.x/forms/overview.md"
        second_page = "https://filamentphp.com/docs/5.x/forms/text-input.md"

        inventory = sync.build_inventory(
            [second_page, first_page],
            fetch=lambda _url: """
                <AutoScreenshot name=\"forms/fields/text-input/affix\" alt=\"Affix\" />
            """,
        )

        self.assertEqual(1, len(inventory["screenshots"]))
        self.assertEqual(["forms/fields/text-input/affix"], inventory["crawl"]["manifest"][first_page])
        self.assertEqual([], inventory["crawl"]["manifest"][second_page])


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

    def test_validation_accepts_explicit_non_decision_changing_evidence(self):
        validate = load_validate_module()
        page = "https://filamentphp.com/docs/5.x/forms/overview.md"
        catalog = {"patterns": []}
        inventory = {
            "crawl": {
                "status": "complete",
                "pages": [page],
                "manifest": {page: ["forms/fields/above-label"]},
            },
            "screenshots": [{
                "name": "forms/fields/above-label",
                "documentation": page,
                "light_image": "https://filamentphp.com/docs/images/5.x/light/forms/fields/above-label.jpg",
                "dark_image": "https://filamentphp.com/docs/images/5.x/dark/forms/fields/above-label.jpg",
                "status": "reviewed",
                "decision_relevance": "non-decision-changing",
            }],
        }

        self.assertEqual([], validate.validate(catalog, inventory))


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
