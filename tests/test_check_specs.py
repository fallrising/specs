import shutil
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import check_specs  # noqa: E402

TEMPLATE = ROOT / "templates" / "product"

CARD_POOL = """schema: card-pool/v1
deck_rules: {size: 4, max_copies: 2, max_copies_general: 1}
factions:
  - {id: a, name: A, lord: L-A, milestone: M1}
  - {id: neutral, name: N, lord: null, milestone: M1}
lords:
  - {id: L-A, name: LA, faction: a, hp: 30}
cards:
  - {id: A1, name: x, faction: a, type: general, troop: 步, cost: 1, attack: 1, hp: 1}
  - {id: N1, name: y, faction: neutral, type: unit, troop: 弓, cost: 1, attack: 1, hp: 1}
  - {id: T1, name: z, faction: neutral, type: stratagem, cost: 0, collectible: false}
decks:
  - {id: d, faction: a, lord: L-A, milestone: M1, cards: {%CARDS%}}
"""


class CheckSpecsTest(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.pdir = self.tmp / "products" / "demo"
        shutil.copytree(TEMPLATE, self.pdir)
        readme = self.pdir / "README.md"
        readme.write_text(readme.read_text(encoding="utf-8").replace("product: example", "product: demo"), encoding="utf-8")
        self.assertEqual(check_specs.run(self.tmp, fix=True), [])
        self.assertEqual(self.errors(), [])

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def errors(self):
        return check_specs.run(self.tmp)

    def edit(self, rel, old, new):
        p = self.pdir / rel
        text = p.read_text(encoding="utf-8")
        self.assertIn(old, text)
        p.write_text(text.replace(old, new), encoding="utf-8")

    def append(self, rel, text):
        p = self.pdir / rel
        p.write_text(p.read_text(encoding="utf-8") + text, encoding="utf-8")

    def assertError(self, fragment):
        errs = self.errors()
        self.assertTrue(any(fragment in e for e in errs), f"expected {fragment!r} in {errs}")

    def test_repository_is_clean(self):
        self.assertEqual(check_specs.run(ROOT), [])

    def test_bad_status(self):
        self.edit("prd.md", "status: draft", "status: done")
        self.assertError("status 必須是")

    def test_superseded_needs_target(self):
        self.edit("prd.md", "status: draft", "status: superseded")
        self.assertError("superseded_by")

    def test_readme_product_must_match_dir(self):
        self.edit("README.md", "product: demo", "product: other")
        self.assertError("product 應為 'demo'")

    def test_duplicate_id(self):
        self.append("requirements/example.md", "\n### REQ-EX-01 again\n- 里程碑：M1\n\n#### AC-EX-02 x\n- Given a\n- When b\n- Then c\n- 驗證：自動\n")
        self.assertError("REQ-EX-01 重複")

    def test_ac_missing_then(self):
        self.edit("requirements/example.md", "- Then 可觀察的結果\n", "")
        self.assertError("AC-EX-01 缺少「- Then")

    def test_bad_verify_value(self):
        self.edit("requirements/example.md", "- 驗證：自動", "- 驗證：之後再說")
        self.assertError("AC-EX-01 的驗證必須是")

    def test_unknown_milestone(self):
        self.edit("requirements/example.md", "- 里程碑：M1", "- 里程碑：M9")
        self.assertError("里程碑 M9 不在 milestones.md")

    def test_req_without_ac(self):
        self.append("requirements/example.md", "\n### REQ-EX-02 no ac\n- 里程碑：M1\n")
        self.check_fix_then("REQ-EX-02 沒有任何 AC")

    def check_fix_then(self, fragment):
        check_specs.run(self.tmp, fix=True)
        self.assertError(fragment)

    def test_withdrawn_req_is_exempt(self):
        self.append("requirements/example.md", "\n### REQ-EX-02 [撤回] 不做了\n2026-11-16 撤回：範圍調整。\n")
        check_specs.run(self.tmp, fix=True)
        self.assertEqual(self.errors(), [])

    def test_area_mismatch(self):
        self.append("requirements/example.md", "\n### REQ-ZZ-01 wrong\n- 里程碑：M1\n\n#### AC-ZZ-01 x\n- Given a\n- When b\n- Then c\n- 驗證：自動\n")
        self.assertError("area 與檔案 area 'EX' 不符")

    def test_malformed_heading(self):
        self.append("requirements/example.md", "\n### REQ-EX-3 bad number\n")
        self.assertError("編號標題格式錯誤")

    def test_unknown_reference(self):
        self.append("prd.md", "\n見 REQ-EX-42。\n")
        self.assertError("引用不存在的編號 REQ-EX-42")

    def test_stale_scope_index(self):
        self.edit("requirements/example.md", "### REQ-EX-01 需求標題", "### REQ-EX-01 改過的標題")
        self.assertError("範圍索引過期")
        check_specs.run(self.tmp, fix=True)
        self.assertEqual(self.errors(), [])
        self.assertIn("REQ-EX-01 改過的標題：AC-EX-01", (self.pdir / "milestones.md").read_text(encoding="utf-8"))

    def test_milestone_status_value(self):
        self.edit("milestones.md", "- 狀態：draft", "- 狀態：done")
        self.assertError("M1 的狀態必須是 draft 或 approved")

    def test_milestone_without_status_is_draft(self):
        self.edit("milestones.md", "- 狀態：draft\n", "")
        self.assertEqual(self.errors(), [])

    def test_approved_milestone_requires_approved_files(self):
        self.edit("milestones.md", "- 狀態：draft", "- 狀態：approved")
        check_specs.run(self.tmp, fix=True)
        errs = self.errors()
        self.assertTrue(any("milestones.md 的 status 必須是 approved" in e for e in errs), errs)
        self.assertTrue(any("REQ-EX-01 屬於已批准的 M1" in e for e in errs), errs)
        self.edit("milestones.md", "status: draft", "status: approved")
        self.edit("requirements/example.md", "status: draft", "status: approved")
        self.assertEqual(self.errors(), [])
        self.assertIn("**M1 名稱（approved）**", (self.pdir / "milestones.md").read_text(encoding="utf-8"))

    def test_broken_link(self):
        self.append("prd.md", "\n[x](nope.md)\n")
        self.assertError("連結目標不存在：nope.md")

    def write_pool(self, cards):
        (self.pdir / "data").mkdir(exist_ok=True)
        (self.pdir / "data" / "cards.yaml").write_text(CARD_POOL.replace("%CARDS%", cards), encoding="utf-8")

    def test_card_pool_valid(self):
        self.write_pool("A1: 1, N1: 2, N2: 1")
        self.edit("data/cards.yaml", "  - {id: T1", "  - {id: N2, name: w, faction: neutral, type: unit, troop: 騎, cost: 1, attack: 1, hp: 1}\n  - {id: T1")
        self.assertEqual(self.errors(), [])

    def test_card_pool_deck_size(self):
        self.write_pool("A1: 1, N1: 1")
        self.assertError("有 2 張，規則要求 4 張")

    def test_card_pool_general_limit(self):
        self.write_pool("A1: 2, N1: 2")
        self.assertError("A1 有 2 張，上限 1")

    def test_card_pool_non_collectible(self):
        self.write_pool("A1: 1, N1: 2, T1: 1")
        self.assertError("不可收集的卡：T1")

    def test_card_pool_unknown_card(self):
        self.write_pool("A1: 1, N1: 2, Q9: 1")
        self.assertError("不存在的卡：Q9")


if __name__ == "__main__":
    unittest.main()
