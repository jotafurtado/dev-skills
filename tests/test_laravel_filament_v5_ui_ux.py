import importlib.util
import json
import shutil
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
UI_UX_ROOT = ROOT / "skills" / "laravel-filament-v5-ui-ux"
MAINTENANCE = ROOT / "maintenance" / "filament-ui-ux"
SYNC_SCRIPT = MAINTENANCE / "scripts" / "sync_screenshot_inventory.py"
VALIDATE_SCRIPT = MAINTENANCE / "scripts" / "validate_compositions.py"
VERIFY_APIS_SCRIPT = MAINTENANCE / "scripts" / "verify_filament_apis.py"
REFERENCES = UI_UX_ROOT / "references"
INVENTORY_PATH = ROOT / "maintenance" / "filament-ui-ux" / "screenshot-inventory.json"
MAIN_FILAMENT_SKILL_PATH = ROOT / "skills" / "laravel-filament-v5" / "SKILL.md"
MAIN_FILAMENT_QUERY_EVALS_PATH = ROOT / "skills" / "laravel-filament-v5" / "evals" / "eval_queries.json"
UI_UX_QUERY_EVALS_PATH = UI_UX_ROOT / "evals" / "eval_queries.json"
UI_UX_SKILL_PATH = UI_UX_ROOT / "SKILL.md"
UI_UX_RELEASE_PATH = UI_UX_ROOT / "RELEASE.md"
UI_UX_RELEASE_VERIFICATION_PATH = MAINTENANCE / "release-verification.md"
UI_UX_INSTALL_SMOKE_SCRIPT = MAINTENANCE / "scripts" / "release_install_smoke.py"

PHP = shutil.which("php")


def _load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def load_sync_module():
    return _load("sync_screenshot_inventory", SYNC_SCRIPT)


def load_validate_module():
    return _load("validate_compositions", VALIDATE_SCRIPT)


def load_verify_apis_module():
    return _load("verify_filament_apis", VERIFY_APIS_SCRIPT)


COMPOSITION = """# Example

| Pattern | Use it for |
|---|---|
| [Thing](#thing) | Something |

---

## Thing

**When**: the record needs one scan line.

**Not when**: the facts must be compared across rows.

**Source**: [tables/layout](https://filamentphp.com/docs/5.x/tables/layout.md)

```php
use Filament\\Tables\\Columns\\TextColumn;

TextColumn::make('name')
    ->searchable(),
```
"""


class FragmentWrappingTests(unittest.TestCase):
    """Compositions are fragments; the validator must make each one parseable."""

    def setUp(self):
        if PHP is None:
            self.skipTest("php is not installed")
        self.validate = load_validate_module()

    def test_each_fragment_shape_parses(self):
        shapes = {
            "complete file": "use Filament\\Widgets\\ChartWidget;\n\nclass OrdersChart extends ChartWidget\n{\n    protected ?string $heading = 'Orders';\n}",
            "method body": "use Filament\\Tables\\Table;\n\npublic static function table(Table $table): Table\n{\n    return $table;\n}",
            "return statement": "return $table->columns([]);",
            "chained call": "->filters([\n    SelectFilter::make('status'),\n])",
            "statement": "use Filament\\Notifications\\Notification;\n\nNotification::make()\n    ->title('Saved')\n    ->send();",
            "array element": "TextColumn::make('name')\n    ->searchable(),",
        }
        for label, code in shapes.items():
            with self.subTest(shape=label):
                self.assertIsNone(self.validate.lint_php(code, php=PHP))

    def test_unparseable_fragment_is_reported(self):
        self.assertIsNotNone(self.validate.lint_php("TextColumn::make('name'", php=PHP))

    def test_use_statements_are_hoisted_out_of_the_wrapper(self):
        wrapped = self.validate.wrap_fragment("use Filament\\Tables\\Table;\n\nTextColumn::make('name'),")
        self.assertLess(wrapped.index("use Filament"), wrapped.index("$__p = ["))


class CompositionValidationTests(unittest.TestCase):
    def setUp(self):
        self.validate = load_validate_module()

    def test_shipped_library_is_valid(self):
        errors = self.validate.validate_compositions(references=REFERENCES, php=PHP)
        self.assertEqual([], errors)

    def test_coverage_matches_the_shipped_files(self):
        patterns, variants = self.validate.coverage(references=REFERENCES)
        expected_patterns = sum(
            (REFERENCES / name).read_text().count("\n## ")
            for name in self.validate.COMPOSITION_FILES
        )
        self.assertEqual(expected_patterns, patterns)
        self.assertGreater(variants, patterns)

    def test_pattern_without_when_is_rejected(self):
        broken = COMPOSITION.replace("**When**: the record needs one scan line.\n\n", "")
        errors = self.validate.validate_composition("example.md", broken, php=None)
        self.assertIn("example.md: pattern 'Thing' is missing **When**", errors)

    def test_pattern_without_official_source_is_rejected(self):
        broken = COMPOSITION.replace(
            "[tables/layout](https://filamentphp.com/docs/5.x/tables/layout.md)",
            "internal notes",
        )
        errors = self.validate.validate_composition("example.md", broken, php=None)
        self.assertIn("example.md: pattern 'Thing' has no official Source URL", errors)

    def test_placeholder_identifier_is_rejected(self):
        broken = COMPOSITION.replace("TextColumn::make('name')", "TextColumn::make('your_column')")
        errors = self.validate.validate_composition("example.md", broken, php=None)
        self.assertIn("example.md: uses placeholder identifier 'your_column'", errors)

    def test_namespace_removed_in_v5_is_rejected(self):
        broken = COMPOSITION.replace(
            "use Filament\\Tables\\Columns\\TextColumn;",
            "use Filament\\Tables\\Actions\\DeleteAction;",
        )
        errors = self.validate.validate_composition("example.md", broken, php=None)
        self.assertIn(
            "example.md: uses Filament\\Tables\\Actions\\, removed in Filament 5",
            errors,
        )

    def test_file_without_php_is_rejected(self):
        prose = COMPOSITION.split("```php")[0]
        errors = self.validate.validate_composition("example.md", prose, php=None)
        self.assertIn("example.md ships no php composition", errors)

    def test_valid_composition_produces_no_errors(self):
        self.assertEqual([], self.validate.validate_composition("example.md", COMPOSITION, php=PHP))


class ScreenshotInventoryTests(unittest.TestCase):
    """The inventory is the discovery asset for uncovered official patterns."""

    def setUp(self):
        self.validate = load_validate_module()
        self.inventory = json.loads(INVENTORY_PATH.read_text())

    def _one(self, **overrides):
        screenshot = {
            "name": "tables/layout/split",
            "documentation": "https://filamentphp.com/docs/5.x/tables/layout.md",
            "documentation_pages": ["https://filamentphp.com/docs/5.x/tables/layout.md"],
            "light_image": "https://filamentphp.com/docs/images/5.x/light/tables/layout/split.jpg",
            "dark_image": "https://filamentphp.com/docs/images/5.x/dark/tables/layout/split.jpg",
            "status": "reviewed",
            "decision_relevance": "non-decision-changing",
        }
        screenshot.update(overrides)
        return {
            "crawl": {
                "status": "complete",
                "pages": ["https://filamentphp.com/docs/5.x/tables/layout.md"],
                "manifest": {"https://filamentphp.com/docs/5.x/tables/layout.md": [screenshot["name"]]},
            },
            "screenshots": [screenshot],
        }

    def test_shipped_inventory_is_valid(self):
        self.assertEqual([], self.validate.validate_inventory(self.inventory))

    def test_unreviewed_screenshot_is_rejected(self):
        errors = self.validate.validate_inventory(self._one(status="unreviewed"))
        self.assertIn("tables/layout/split is unreviewed", errors)

    def test_non_official_image_source_is_rejected(self):
        errors = self.validate.validate_inventory(self._one(light_image="https://example.com/a.jpg"))
        self.assertIn("tables/layout/split has an invalid light_image source", errors)

    def test_decision_changing_screenshot_needs_family_and_variant(self):
        errors = self.validate.validate_inventory(self._one(decision_relevance="decision-changing"))
        self.assertIn(
            "tables/layout/split needs a family for a decision-changing screenshot",
            errors,
        )
        self.assertIn(
            "tables/layout/split needs a variant for a decision-changing screenshot",
            errors,
        )

    def test_incomplete_crawl_is_rejected(self):
        inventory = self._one()
        inventory["crawl"]["status"] = "partial"
        self.assertIn(
            "inventory is missing a complete crawl contract",
            self.validate.validate_inventory(inventory),
        )

    def test_record_detail_evidence_is_assigned_to_reviewed_variants(self):
        screenshots = {item["name"]: item for item in self.inventory["screenshots"]}
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
        screenshots = {item["name"]: item for item in self.inventory["screenshots"]}
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

    def test_action_feedback_evidence_is_reviewed_and_assigned_to_variants(self):
        screenshots = {item["name"]: item for item in self.inventory["screenshots"]}
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


class FilamentApiSymbolTests(unittest.TestCase):
    """Symbol collection for the Composer fixture gate — no network required."""

    def setUp(self):
        self.verify = load_verify_apis_module()

    def _references(self, body: str) -> Path:
        directory = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, directory, ignore_errors=True)
        (directory / "table.md").write_text(body)
        return directory

    def test_imported_classes_and_enum_cases_are_collected(self):
        references = self._references(
            "## Thing\n\n```php\n"
            "use Filament\\Tables\\Columns\\TextColumn;\n"
            "use Filament\\Support\\Icons\\Heroicon;\n\n"
            "TextColumn::make('name')->icon(Heroicon::Envelope),\n"
            "```\n"
        )
        classes, enum_cases = self.verify.collect_symbols(references)

        self.assertIn("Filament\\Tables\\Columns\\TextColumn", classes)
        self.assertIn("Filament\\Support\\Icons\\Heroicon", classes)
        self.assertIn("Filament\\Support\\Icons\\Heroicon::Envelope", enum_cases)

    def test_make_and_class_are_not_treated_as_enum_cases(self):
        references = self._references(
            "## Thing\n\n```php\n"
            "use Filament\\Tables\\Columns\\TextColumn;\n\n"
            "TextColumn::make('name')->options(TextColumn::class),\n"
            "```\n"
        )
        _, enum_cases = self.verify.collect_symbols(references)

        self.assertEqual({}, enum_cases)

    def test_symbols_without_a_filament_import_are_ignored(self):
        references = self._references(
            "## Thing\n\n```php\n"
            "use Illuminate\\Database\\Eloquent\\Builder;\n\n"
            "OrderStatus::Pending,\n"
            "```\n"
        )
        classes, enum_cases = self.verify.collect_symbols(references)

        self.assertEqual({}, classes)
        self.assertEqual({}, enum_cases)

    def test_every_file_using_a_symbol_is_reported(self):
        directory = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, directory, ignore_errors=True)
        block = (
            "## Thing\n\n```php\n"
            "use Filament\\Tables\\Table;\n\n"
            "Table::make(),\n"
            "```\n"
        )
        (directory / "table.md").write_text(block)
        (directory / "dashboard.md").write_text(block)

        classes, _ = self.verify.collect_symbols(directory)

        self.assertEqual({"table.md", "dashboard.md"}, classes["Filament\\Tables\\Table"])


class ScreenshotSynchronizationTests(unittest.TestCase):
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


class CrossSkillContractTests(unittest.TestCase):
    def test_release_metadata_and_notes_state_scope_authority_and_gates(self):
        skill = UI_UX_SKILL_PATH.read_text()
        release = UI_UX_RELEASE_PATH.read_text()
        verification = UI_UX_RELEASE_VERIFICATION_PATH.read_text()
        smoke_script = UI_UX_INSTALL_SMOKE_SCRIPT.read_text()

        self.assertIn('version: "2.1.0"', skill)
        self.assertIn('filament_version: "5.x"', skill)
        self.assertIn("Filament 5.x only", release)
        self.assertIn("laravel-filament-v5", release)
        self.assertIn("offline", release.lower())
        self.assertIn("release_install_smoke.py", release)
        self.assertIn("validate_compositions.py", release)
        self.assertIn("verify_filament_apis.py", release)
        self.assertIn("Authority: `laravel-filament-v5`", verification)
        self.assertIn("Evidence: local reviewed catalog", verification)
        self.assertIn("verify_filament_apis.py", verification)
        self.assertIn("cursor", smoke_script)
        self.assertIn("--copy", smoke_script)
        self.assertIn("Jota Furtado Dev Skills", smoke_script)
        self.assertIn("README.md", smoke_script)

    def test_narrative_forward_evaluation_is_retired(self):
        release = UI_UX_RELEASE_PATH.read_text()
        verification = UI_UX_RELEASE_VERIFICATION_PATH.read_text()

        self.assertFalse((MAINTENANCE / "scripts" / "run_forward_evals.py").exists())
        self.assertFalse((UI_UX_ROOT / "evals" / "forward-runs").exists())
        self.assertIn("discontinued", verification.lower())
        self.assertIn("narrative forward evaluations", release.lower())

    def test_query_engine_and_catalog_are_removed(self):
        for path in (
            MAINTENANCE / "scripts" / "query_visual_catalog.py",
            MAINTENANCE / "scripts" / "build_catalog_index.py",
            REFERENCES / "visual-catalog.json",
            REFERENCES / "visual-catalog-index.md",
        ):
            with self.subTest(path=path.name):
                self.assertFalse(path.exists())

    def test_skill_routes_every_surface_to_a_composition_file(self):
        validate = load_validate_module()
        skill = UI_UX_SKILL_PATH.read_text()

        for name in validate.COMPOSITION_FILES:
            with self.subTest(reference=name):
                self.assertIn(f"`references/{name}`", skill)

    def test_skill_imposes_no_mandatory_workflow(self):
        skill = UI_UX_SKILL_PATH.read_text()

        self.assertIn("no required workflow", skill.lower())
        self.assertNotIn("Mandatory visual decision flow", skill)
        self.assertNotIn("visual decision trace", skill.lower())

    def test_skill_directory_matches_its_declared_name(self):
        skill = UI_UX_SKILL_PATH.read_text()

        self.assertIn("name: laravel-filament-v5-ui-ux", skill)
        self.assertEqual("laravel-filament-v5-ui-ux", UI_UX_ROOT.name)

    def test_skill_states_the_sibling_pairing(self):
        skill = UI_UX_SKILL_PATH.read_text()

        self.assertIn(
            "--skill laravel-filament-v5-ui-ux --skill laravel-filament-v5",
            skill,
        )
        self.assertIn("If it is not installed, say so", skill)

    def test_cross_skill_contract_routes_visual_selection_to_ui_ux_skill(self):
        main_skill = MAIN_FILAMENT_SKILL_PATH.read_text()
        ui_ux_skill = UI_UX_SKILL_PATH.read_text()

        self.assertIn(
            "How a Filament 5 surface is arranged belongs to `laravel-filament-v5-ui-ux`",
            main_skill,
        )
        self.assertIn(
            "Let `laravel-filament-v5` own installed-version APIs, security, implementation, and tests.",
            ui_ux_skill,
        )

    def test_main_skill_names_composition_decisions_without_resolving_them(self):
        main_skill = MAIN_FILAMENT_SKILL_PATH.read_text()

        self.assertIn("may name a composition decision", main_skill)
        self.assertIn("must leave it unresolved", main_skill)

    def test_main_skill_does_not_branch_on_sibling_installation(self):
        """The skill format has no dependency or runtime-detection mechanism, so a
        branch on whether the sibling is installed cannot be evaluated. The seam is
        stated unconditionally instead."""
        main_skill = MAIN_FILAMENT_SKILL_PATH.read_text()
        screenshots = (
            ROOT / "skills" / "laravel-filament-v5" / "references" / "screenshots.md"
        ).read_text()

        for source, label in (
            (main_skill, "SKILL.md"),
            (screenshots, "references/screenshots.md"),
        ):
            for branch in ("when it is installed", "when installed", "is unavailable", "were unavailable", "was unavailable"):
                self.assertNotIn(branch, source, f"{label} branches on sibling availability: {branch!r}")

    def test_sibling_skill_defers_arrangement_to_the_composition_library(self):
        tables = (ROOT / "skills" / "laravel-filament-v5" / "references" / "tables.md").read_text()
        layout = (ROOT / "skills" / "laravel-filament-v5" / "references" / "layout.md").read_text()

        self.assertIn("references/table.md", tables)
        self.assertIn("references/form-layout.md", layout)
        self.assertIn("API inventory", tables)
        self.assertIn("API inventory", layout)

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


if __name__ == "__main__":
    unittest.main()
