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
DISCOVER_SCRIPT = MAINTENANCE / "scripts" / "discover_sibling_skill.py"
REFERENCES = UI_UX_ROOT / "references"
INVENTORY_PATH = ROOT / "maintenance" / "filament-ui-ux" / "screenshot-inventory.json"
MAIN_FILAMENT_SKILL_PATH = ROOT / "skills" / "laravel-filament-v5" / "SKILL.md"
MAIN_FILAMENT_QUERY_EVALS_PATH = ROOT / "skills" / "laravel-filament-v5" / "evals" / "eval_queries.json"
UI_UX_QUERY_EVALS_PATH = UI_UX_ROOT / "evals" / "eval_queries.json"
UI_UX_SKILL_PATH = UI_UX_ROOT / "SKILL.md"

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


def load_discover_module():
    return _load("discover_sibling_skill", DISCOVER_SCRIPT)


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

    def test_shipped_library_has_no_uncovered_families(self):
        inventory = json.loads(INVENTORY_PATH.read_text())
        self.assertEqual([], self.validate.uncovered_patterns(inventory, references=REFERENCES))

    def test_shipped_library_has_no_orphan_headings(self):
        inventory = json.loads(INVENTORY_PATH.read_text())
        self.assertEqual([], self.validate.orphan_headings(inventory, references=REFERENCES))

    def test_uncovered_family_is_reported(self):
        directory = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, directory, ignore_errors=True)
        (directory / "table.md").write_text("## Standard compare-and-scan table\n")
        inventory = {
            "screenshots": [
                {"decision_relevance": "decision-changing", "family": "brand-new-surface"},
                {"decision_relevance": "decision-changing", "family": "standard-compare-and-scan-table"},
            ]
        }
        self.assertEqual(
            ["brand-new-surface"],
            self.validate.uncovered_patterns(inventory, references=directory),
        )

    def test_action_feedback_family_matches_its_heading(self):
        self.assertTrue(
            self.validate.heading_covers_family(
                "action-feedback-overlays",
                "Action, feedback, and overlays",
            )
        )

    def test_subset_tokens_are_not_coverage(self):
        self.assertFalse(self.validate.heading_covers_family("sections", "Aside sections"))
        self.assertFalse(self.validate.heading_covers_family("aside-sections", "Sections"))
        self.assertTrue(self.validate.heading_covers_family("sections", "Sections"))
        self.assertTrue(self.validate.heading_covers_family("aside-sections", "Aside sections"))

    def test_orphan_heading_is_reported(self):
        directory = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, directory, ignore_errors=True)
        (directory / "table.md").write_text("## Standard compare-and-scan table\n## Brand new surface\n")
        inventory = {
            "screenshots": [
                {"decision_relevance": "decision-changing", "family": "standard-compare-and-scan-table"},
            ]
        }
        self.assertEqual(
            ["Brand new surface"],
            self.validate.orphan_headings(inventory, references=directory),
        )

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

    def test_inventory_lives_outside_the_install_payload(self):
        self.assertTrue(INVENTORY_PATH.is_file())
        self.assertNotIn(UI_UX_ROOT, INVENTORY_PATH.parents)
        self.assertFalse((REFERENCES / "screenshot-inventory.json").exists())
        self.assertFalse((UI_UX_ROOT / "scripts").exists())
        self.assertTrue((MAINTENANCE / "scripts" / "discover_sibling_skill.py").is_file())
        self.assertFalse((MAINTENANCE / "scripts" / "sync_visual_catalog.py").exists())

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

    def test_standard_compare_and_scan_table_family_is_assigned(self):
        screenshots = {item["name"]: item for item in self.inventory["screenshots"]}
        expected_variants = {
            "tables/overview/columns": "column-scan",
            "tables/overview/filters": "purposeful-filters",
            "tables/actions/group": "direct-row-action",
            "tables/actions/bulk": "bulk-selection",
            "tables/empty-state": "empty-versus-filtered-empty",
            "tables/grouping": "grouped-rows",
            "tables/summaries": "decision-summary",
            "tables/pagination/default": "positional-pagination",
        }

        for screenshot, variant in expected_variants.items():
            self.assertEqual("reviewed", screenshots[screenshot]["status"])
            self.assertEqual("decision-changing", screenshots[screenshot]["decision_relevance"])
            self.assertEqual("standard-compare-and-scan-table", screenshots[screenshot]["family"])
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
    def test_narrative_forward_evaluation_is_retired(self):
        self.assertFalse((MAINTENANCE / "scripts" / "run_forward_evals.py").exists())
        self.assertFalse((UI_UX_ROOT / "evals" / "forward-runs").exists())

    def test_query_engine_and_catalog_are_removed(self):
        for path in (
            MAINTENANCE / "scripts" / "query_visual_catalog.py",
            MAINTENANCE / "scripts" / "build_catalog_index.py",
            REFERENCES / "visual-catalog.json",
            REFERENCES / "visual-catalog-index.md",
        ):
            with self.subTest(path=path.name):
                self.assertFalse(path.exists())

    def test_skill_directory_matches_its_declared_name(self):
        self.assertEqual("laravel-filament-v5-ui-ux", UI_UX_ROOT.name)
        self.assertEqual(
            "laravel-filament-v5-ui-ux",
            load_discover_module().frontmatter_name(UI_UX_SKILL_PATH),
        )
        self.assertEqual(
            "laravel-filament-v5",
            load_discover_module().frontmatter_name(MAIN_FILAMENT_SKILL_PATH),
        )

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


class SiblingDiscoveryTests(unittest.TestCase):
    def setUp(self):
        self.discover = load_discover_module()

    def _write_skill(self, root: Path, name: str, frontmatter_name: str | None = None) -> Path:
        skill = root / name
        skill.mkdir(parents=True)
        declared = name if frontmatter_name is None else frontmatter_name
        (skill / "SKILL.md").write_text(f"---\nname: {declared}\n---\n\n# {declared}\n")
        return skill / "SKILL.md"

    def test_sibling_directory_wins_over_later_roots(self):
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            skills = root / "skills"
            self._write_skill(skills, "laravel-filament-v5-ui-ux")
            expected = self._write_skill(skills, "laravel-filament-v5")
            home = root / "home"
            self._write_skill(home / ".agents" / "skills", "laravel-filament-v5")
            found = self.discover.discover_sibling_skill(
                "laravel-filament-v5",
                skill_dir=skills / "laravel-filament-v5-ui-ux",
                project=root / "project",
                home=home,
            )
            self.assertEqual(expected, found)

    def test_project_agents_directory_is_next(self):
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            project = root / "project"
            expected = self._write_skill(project / ".agents" / "skills", "laravel-filament-v5")
            self._write_skill(project / ".claude" / "skills", "laravel-filament-v5")
            found = self.discover.discover_sibling_skill(
                "laravel-filament-v5",
                skill_dir=root / "skills" / "laravel-filament-v5-ui-ux",
                project=project,
                home=root / "home",
            )
            self.assertEqual(expected, found)

    def test_wrong_frontmatter_name_is_skipped(self):
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            home = root / "home"
            self._write_skill(
                home / ".agents" / "skills",
                "laravel-filament-v5",
                frontmatter_name="other-skill",
            )
            expected = self._write_skill(home / ".claude" / "skills", "laravel-filament-v5")
            found = self.discover.discover_sibling_skill(
                "laravel-filament-v5",
                project=root / "project",
                home=home,
            )
            self.assertEqual(expected, found)

    def test_no_matching_file_returns_none(self):
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            found = self.discover.discover_sibling_skill(
                "laravel-filament-v5",
                skill_dir=root / "skills" / "laravel-filament-v5-ui-ux",
                project=root / "project",
                home=root / "home",
            )
            self.assertIsNone(found)

if __name__ == "__main__":
    unittest.main()
