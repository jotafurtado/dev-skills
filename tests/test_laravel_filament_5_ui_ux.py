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
INVENTORY_PATH = ROOT / "skills" / "laravel-filament-5-ui-ux" / "references" / "screenshot-inventory.json"
MAIN_FILAMENT_SKILL_PATH = ROOT / "skills" / "laravel-filament-v5" / "SKILL.md"
MAIN_FILAMENT_QUERY_EVALS_PATH = ROOT / "skills" / "laravel-filament-v5" / "evals" / "eval_queries.json"
UI_UX_QUERY_EVALS_PATH = ROOT / "skills" / "laravel-filament-5-ui-ux" / "evals" / "eval_queries.json"
UI_UX_SKILL_PATH = ROOT / "skills" / "laravel-filament-5-ui-ux" / "SKILL.md"
UI_UX_RELEASE_PATH = ROOT / "skills" / "laravel-filament-5-ui-ux" / "RELEASE.md"


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

    def test_query_excludes_parallel_patterns_for_a_sequential_workflow(self):
        query = load_query_module()

        result = query.query_catalog(
            surface="form",
            goal="organize-stable-groups",
            workflow="sequential",
            available_width="standard",
            information_shape="dependent-steps",
            relationship="ordered-steps",
            responsive_context="mobile-first",
        )

        self.assertEqual("wizard", result["selected_pattern"]["id"])

    def test_ordinary_field_composition_query_selects_field_geometry_and_guidance(self):
        query = load_query_module()

        result = query.query_catalog(
            surface="form",
            goal="compose-ordinary-fields",
            workflow="parallel",
            available_width="wide",
            information_shape="mixed-field-lengths",
            relationship="field-and-context",
            responsive_context="desktop-with-mobile-fallback",
        )

        self.assertEqual("ordinary-field-composition", result["selected_pattern"]["id"])
        self.assertTrue(
            any(
                consideration.startswith("labels identify fields")
                for consideration in result["selected_pattern"]["accessibility_considerations"]
            )
        )
        variants = {item["id"]: item for item in result["selected_pattern"]["variant_decisions"]}
        self.assertIn("inline-label", variants)
        self.assertIn("adjoined-affix", variants)
        self.assertIn("placeholder-example", variants)
        self.assertIn("auxiliary-content", variants)

    def test_collection_input_query_selects_repeatable_item_hierarchy(self):
        query = load_query_module()

        result = query.query_catalog(
            surface="form",
            goal="compose-repeatable-items",
            workflow="parallel",
            available_width="wide",
            information_shape="repeatable-structured-items",
            relationship="collection-of-structured-items",
            responsive_context="desktop-with-mobile-fallback",
        )

        self.assertEqual("collection-items", result["selected_pattern"]["id"])
        self.assertIn(
            "forms/fields/repeater/simple",
            [evidence["screenshot"] for evidence in result["selected_pattern"]["visual_evidence"]],
        )
        variants = {item["id"]: item for item in result["selected_pattern"]["variant_decisions"]}
        self.assertIn("add-action-placement", variants)
        self.assertIn("table-layout", variants)
        self.assertIn("reorder-buttons", variants)

    def test_rich_content_query_selects_a_full_width_editor(self):
        query = load_query_module()

        result = query.query_catalog(
            surface="form",
            goal="edit-long-form-content",
            workflow="linear",
            available_width="wide",
            information_shape="long-form-content",
            relationship="single-high-density-control",
            responsive_context="desktop-with-mobile-fallback",
        )

        self.assertEqual("rich-content-editor", result["selected_pattern"]["id"])
        self.assertIn("full-width", " ".join(result["selected_pattern"]["selection_signals"]))

    def test_compare_and_scan_query_selects_standard_table_operations(self):
        query = load_query_module()

        result = query.query_catalog(
            surface="table",
            goal="compare-and-scan-records",
            workflow="parallel",
            available_width="wide",
            information_shape="repeated-records-with-comparable-facts",
            relationship="peer-records",
            responsive_context="desktop-with-mobile-fallback",
        )

        self.assertEqual("standard-compare-and-scan-table", result["selected_pattern"]["id"])
        self.assertIn(
            "tables/overview/columns",
            [evidence["screenshot"] for evidence in result["selected_pattern"]["visual_evidence"]],
        )
        variants = {item["id"]: item for item in result["selected_pattern"]["variant_decisions"]}
        self.assertIn("status-and-boolean-meaning", variants)
        self.assertIn("color alone", " ".join(variants["status-and-boolean-meaning"]["avoid_when"]))

    def test_identity_centred_record_query_selects_responsive_table_layout(self):
        query = load_query_module()

        result = query.query_catalog(
            surface="table",
            goal="present-identity-centred-records",
            workflow="parallel",
            available_width="standard",
            information_shape="identity-with-grouped-details",
            relationship="record-with-supporting-details",
            responsive_context="desktop-with-mobile-fallback",
        )

        self.assertEqual("responsive-identity-centred-table", result["selected_pattern"]["id"])
        variants = {item["id"]: item for item in result["selected_pattern"]["variant_decisions"]}
        self.assertIn("split-identity-and-details", variants)
        self.assertIn("mobile", variants["split-identity-and-details"]["visual_evidence"])
        self.assertIn("keyboard", " ".join(result["selected_pattern"]["accessibility_considerations"]))

    def test_operational_dashboard_query_selects_decision_ordered_widgets(self):
        query = load_query_module()

        result = query.query_catalog(
            surface="dashboard",
            goal="support-operational-decisions",
            workflow="monitoring",
            available_width="wide",
            information_shape="operational-metrics-with-trends-and-activity",
            relationship="summary-to-detail",
            responsive_context="desktop-with-mobile-fallback",
        )

        self.assertEqual("operational-dashboard", result["selected_pattern"]["id"])
        self.assertEqual(
            ["operational-dashboard"],
            [candidate["id"] for candidate in result["candidates"]],
        )
        evidence = [item["screenshot"] for item in result["selected_pattern"]["visual_evidence"]]
        self.assertIn("panels/dashboard", evidence)
        self.assertIn("widgets/stats-overview/chart", evidence)
        variants = {item["id"]: item for item in result["selected_pattern"]["variant_decisions"]}
        self.assertIn("decision-relevant-stats", variants)
        self.assertEqual("panels/dashboard", variants["table-widget-queue"]["visual_evidence"])
        self.assertIn("semantic trend", " ".join(result["selected_pattern"]["accessibility_considerations"]))

    def test_record_detail_query_selects_identity_first_infolist_composition(self):
        query = load_query_module()

        result = query.query_catalog(
            surface="record-detail",
            goal="present-scannable-record-details",
            workflow="parallel",
            available_width="wide",
            information_shape="identity-status-primary-facts-with-secondary-metadata",
            relationship="identity-to-facts-and-secondary-history",
            responsive_context="desktop-with-mobile-fallback",
        )

        self.assertEqual("record-detail-infolist", result["selected_pattern"]["id"])
        self.assertEqual(
            ["record-detail-infolist"],
            [candidate["id"] for candidate in result["candidates"]],
        )
        variants = {item["id"]: item for item in result["selected_pattern"]["variant_decisions"]}
        self.assertIn("inline-label-facts", variants)
        self.assertIn("tabbed-secondary-detail", variants)
        self.assertEqual(
            "schemas/layout/tabs/simple",
            variants["tabbed-secondary-detail"]["visual_evidence"],
        )
        self.assertIn(
            "infolists/entries/inline-label/section",
            [evidence["screenshot"] for evidence in result["selected_pattern"]["visual_evidence"]],
        )
        self.assertIn(
            "panels/resources/viewing",
            [evidence["screenshot"] for evidence in result["selected_pattern"]["visual_evidence"]],
        )

    def test_panel_shell_queries_select_top_navigation_for_small_panels_and_grouped_sidebar_for_back_offices(self):
        query = load_query_module()

        small_panel = query.query_catalog(
            surface="panel-shell",
            goal="navigate-a-small-panel",
            workflow="parallel",
            available_width="wide",
            information_shape="few-peer-destinations",
            relationship="peer-destinations",
            responsive_context="desktop-with-mobile-fallback",
        )
        back_office = query.query_catalog(
            surface="panel-shell",
            goal="navigate-a-substantial-back-office",
            workflow="parallel",
            available_width="wide",
            information_shape="many-domain-destinations-with-actionable-queues",
            relationship="domain-groups-within-one-audience",
            responsive_context="desktop-with-mobile-fallback",
        )

        self.assertEqual("small-panel-top-navigation", small_panel["selected_pattern"]["id"])
        self.assertEqual("back-office-sidebar-navigation", back_office["selected_pattern"]["id"])
        self.assertIn(
            "panels/navigation/top-navigation",
            [evidence["screenshot"] for evidence in small_panel["selected_pattern"]["visual_evidence"]],
        )
        variants = {item["id"]: item for item in back_office["selected_pattern"]["variant_decisions"]}
        self.assertIn("actionable-navigation-badge", variants)
        self.assertEqual("panels/navigation/badge", variants["actionable-navigation-badge"]["visual_evidence"])

    def test_action_feedback_query_selects_risk_aware_overlay_composition(self):
        query = load_query_module()

        result = query.query_catalog(
            surface="action-feedback",
            goal="complete-contextual-action-safely",
            workflow="contextual",
            available_width="standard",
            information_shape="risk-confirmation-or-short-form-with-feedback",
            relationship="action-to-affected-record-and-result",
            responsive_context="desktop-with-mobile-fallback",
        )

        self.assertEqual("action-feedback-overlays", result["selected_pattern"]["id"])
        variants = {item["id"]: item for item in result["selected_pattern"]["variant_decisions"]}
        self.assertIn("compact-confirmation", variants)
        self.assertIn("focused-modal-form", variants)
        self.assertIn("reference-heavy-slide-over", variants)
        self.assertIn("full-page-workflow", variants)
        self.assertIn(
            "actions/modal/confirmation",
            [evidence["screenshot"] for evidence in result["selected_pattern"]["visual_evidence"]],
        )

    def test_action_feedback_evidence_is_reviewed_and_assigned_to_variants(self):
        inventory = json.loads(INVENTORY_PATH.read_text())
        screenshots = {item["name"]: item for item in inventory["screenshots"]}

        expected_variants = {
            "actions/group/simple": "direct-and-grouped-actions",
            "actions/modal/confirmation": "compact-confirmation",
            "actions/modal/form": "focused-modal-form",
            "actions/modal/slide-over": "reference-heavy-slide-over",
            "panels/resources/editing": "full-page-workflow",
            "components/callout/simple": "contextual-callout",
            "notifications/actions": "action-feedback-notification",
            "components/empty-state/actions": "actionable-empty-state",
        }

        for name, variant in expected_variants.items():
            self.assertEqual("reviewed", screenshots[name]["status"])
            self.assertEqual("decision-changing", screenshots[name]["decision_relevance"])
            self.assertEqual("action-feedback-overlays", screenshots[name]["family"])
            self.assertEqual(variant, screenshots[name]["variant"])


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
        self.assertEqual(["forms/fields/text-input/affix"], inventory["crawl"]["manifest"][second_page])
        self.assertEqual([first_page, second_page], inventory["screenshots"][0]["documentation_pages"])


class VisualCatalogValidationTests(unittest.TestCase):
    def test_release_metadata_and_notes_state_scope_authority_and_fallbacks(self):
        skill = UI_UX_SKILL_PATH.read_text()
        release = UI_UX_RELEASE_PATH.read_text()

        self.assertIn('version: "1.0.0"', skill)
        self.assertIn("filament_version: \"5.x\"", skill)
        self.assertIn("Filament 5.x only", release)
        self.assertIn("laravel-filament-v5", release)
        self.assertIn("offline", release.lower())
        self.assertIn("image inspection", release.lower())

    def test_cross_skill_contract_routes_visual_selection_to_ui_ux_skill(self):
        main_skill = MAIN_FILAMENT_SKILL_PATH.read_text()
        ui_ux_skill = (ROOT / "skills" / "laravel-filament-5-ui-ux" / "SKILL.md").read_text()

        self.assertIn(
            "For every material Filament 5 visual selection and composition decision, delegate to `laravel-filament-5-ui-ux` when it is installed.",
            main_skill,
        )
        self.assertIn(
            "Let `laravel-filament-v5` own installed-version APIs, security, implementation, and tests.",
            ui_ux_skill,
        )
        self.assertNotIn("retains its current guidance for every other visual surface", main_skill)

    def test_cross_skill_trigger_evals_keep_visual_work_out_of_main_skill(self):
        main_queries = json.loads(MAIN_FILAMENT_QUERY_EVALS_PATH.read_text())
        ui_ux_queries = json.loads(UI_UX_QUERY_EVALS_PATH.read_text())

        main_visual_query = next(
            query for query in main_queries
            if query["query"] == "Polish this Filament settings page while retaining our panel theme."
        )
        ui_ux_visual_query = next(
            query for query in ui_ux_queries
            if query["query"] == "Design a Filament 5 settings form with several stable categories and poor use of desktop width."
        )

        self.assertFalse(main_visual_query["should_trigger"])
        self.assertTrue(ui_ux_visual_query["should_trigger"])

    def test_record_detail_evidence_is_assigned_to_reviewed_variants(self):
        inventory = json.loads(INVENTORY_PATH.read_text())
        screenshots = {item["name"]: item for item in inventory["screenshots"]}

        expected_variants = {
            "panels/resources/viewing": "two-zone-identity-and-facts",
            "infolists/overview": "simple-detail-page",
            "infolists/entries/simple": "two-zone-identity-and-facts",
            "infolists/entries/inline-label/section": "inline-label-facts",
            "infolists/entries/text/badge": "status-badge-and-icon",
            "infolists/entries/icon/boolean": "status-badge-and-icon",
            "infolists/entries/text/copyable": "media-and-copyable-identity",
            "infolists/entries/placeholder": "placeholder-for-absent-fact",
            "infolists/entries/repeatable/table": "repeatable-secondary-detail",
            "infolists/entries/text/expandable-limited-list": "collapsed-long-tail-detail",
        }

        for screenshot, variant in expected_variants.items():
            self.assertEqual("reviewed", screenshots[screenshot]["status"])
            self.assertEqual("decision-changing", screenshots[screenshot]["decision_relevance"])
            self.assertEqual("record-detail-infolist", screenshots[screenshot]["family"])
            self.assertEqual(variant, screenshots[screenshot]["variant"])

    def test_responsive_record_pairs_are_decision_changing_inventory_variants(self):
        inventory = json.loads(INVENTORY_PATH.read_text())
        screenshots = {item["name"]: item for item in inventory["screenshots"]}

        expected_variants = {
            "tables/layout/split-desktop": "split-identity-and-details",
            "tables/layout/split-desktop/mobile": "split-identity-and-details",
            "tables/layout/stack": "stack-related-details",
            "tables/layout/stack/mobile": "stack-related-details",
            "tables/layout/grid": "grid-grouped-details",
            "tables/layout/grid/mobile": "grid-grouped-details",
            "tables/layout/column-grid": "content-grid-records",
            "tables/layout/grow-disabled": "fixed-width-identity",
            "tables/layout/collapsible": "collapsible-secondary-details",
            "tables/layout/collapsible/mobile": "collapsible-secondary-details",
            "tables/layout/stack-hidden-on-mobile": "mobile-visibility",
            "tables/layout/stack-hidden-on-mobile/mobile": "mobile-visibility",
        }

        for screenshot, variant in expected_variants.items():
            self.assertEqual("reviewed", screenshots[screenshot]["status"])
            self.assertEqual("decision-changing", screenshots[screenshot]["decision_relevance"])
            self.assertEqual("responsive-identity-centred-table", screenshots[screenshot]["family"])
            self.assertEqual(variant, screenshots[screenshot]["variant"])

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
