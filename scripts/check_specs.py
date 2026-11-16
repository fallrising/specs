#!/usr/bin/env python3
"""Validate the specs repo structure described in docs/conventions.md.

Usage:
    python3 scripts/check_specs.py [--root DIR] [--fix]

--fix only rewrites the generated scope index in each milestones.md.
Exit status 0 when clean, 1 when any error is found.
"""
from __future__ import annotations

import argparse
import re
import sys
from collections import OrderedDict
from dataclasses import dataclass, field
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    sys.exit("PyYAML is required: pip install pyyaml")

STATUSES = {"draft", "approved", "superseded"}
MILESTONE_STATUSES = {"draft", "approved"}
PRIORITIES = {"必要", "應有", "可選"}
VERIFY = {"自動", "手動", "人工確認"}
WITHDRAWN = "[撤回]"

ID_HEADING = re.compile(r"^(#{1,6})\s+((?:REQ|AC)-\S*)(.*)$")
REQ_HEADING = re.compile(r"^### REQ-([A-Z]{2,4})-(\d{2,})(\s+.*)?$")
AC_HEADING = re.compile(r"^#### AC-([A-Z]{2,4})-(\d{2,})(\s+.*)?$")
MILESTONE_HEADING = re.compile(r"^## (M\d+)\s+(\S.*)$")
ID_REF = re.compile(r"\b((?:REQ|AC)-[A-Z]{2,4}-\d{2,})\b")
LINK = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")
AREA = re.compile(r"^[A-Z]{2,4}$")
GEN_BEGIN = "<!-- BEGIN GENERATED: scope -->"
GEN_END = "<!-- END GENERATED: scope -->"


@dataclass
class Ac:
    id: str
    title: str
    withdrawn: bool
    path: Path
    line: int
    fields: dict = field(default_factory=dict)


@dataclass
class Req:
    id: str
    title: str
    withdrawn: bool
    path: Path
    line: int
    milestone: str | None = None
    priority: str | None = None
    acs: list = field(default_factory=list)


class Report:
    def __init__(self, root: Path):
        self.root = root
        self.errors: list[str] = []

    def err(self, path: Path, line: int | None, msg: str) -> None:
        try:
            rel = path.relative_to(self.root)
        except ValueError:
            rel = path
        loc = f"{rel}:{line}" if line else f"{rel}"
        self.errors.append(f"{loc}: {msg}")


def split_frontmatter(text: str):
    """Return (frontmatter dict | None, body offset in lines)."""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None, 0
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            data = yaml.safe_load("\n".join(lines[1:i])) or {}
            return data, i + 1
    return None, 0


def parse_requirements(path: Path, text: str, area: str, rep: Report):
    reqs: list[Req] = []
    cur_req: Req | None = None
    cur_ac: Ac | None = None
    for n, raw in enumerate(text.splitlines(), 1):
        line = raw.rstrip()
        m_any = ID_HEADING.match(line)
        if m_any:
            m_req = REQ_HEADING.match(line)
            m_ac = AC_HEADING.match(line)
            if m_req:
                rid = f"REQ-{m_req.group(1)}-{m_req.group(2)}"
                if m_req.group(1) != area:
                    rep.err(path, n, f"{rid} 的 area 與檔案 area '{area}' 不符")
                rest = (m_req.group(3) or "").strip()
                withdrawn = rest.startswith(WITHDRAWN)
                cur_req = Req(rid, rest.removeprefix(WITHDRAWN).strip(), withdrawn, path, n)
                cur_ac = None
                reqs.append(cur_req)
            elif m_ac:
                aid = f"AC-{m_ac.group(1)}-{m_ac.group(2)}"
                if m_ac.group(1) != area:
                    rep.err(path, n, f"{aid} 的 area 與檔案 area '{area}' 不符")
                if cur_req is None:
                    rep.err(path, n, f"{aid} 出現在任何 REQ 之前")
                    cur_ac = None
                    continue
                rest = (m_ac.group(3) or "").strip()
                withdrawn = rest.startswith(WITHDRAWN)
                cur_ac = Ac(aid, rest.removeprefix(WITHDRAWN).strip(), withdrawn, path, n)
                cur_req.acs.append(cur_ac)
            else:
                rep.err(path, n, f"編號標題格式錯誤（REQ 用 ###、AC 用 ####，編號 <AREA>-<NN>）：{line}")
            continue
        if line.startswith("#"):
            # Any other heading closes the current blocks.
            if line.startswith("## ") or line.startswith("# "):
                cur_req, cur_ac = None, None
            continue
        if cur_ac is not None:
            for key in ("Given", "When", "Then"):
                if line.startswith(f"- {key} ") or line == f"- {key}":
                    cur_ac.fields[key] = line[len(key) + 2:].strip()
            if line.startswith("- 驗證："):
                cur_ac.fields["驗證"] = line.split("：", 1)[1].strip()
        elif cur_req is not None:
            if line.startswith("- 里程碑："):
                cur_req.milestone = line.split("：", 1)[1].strip()
            elif line.startswith("- 優先："):
                cur_req.priority = line.split("：", 1)[1].strip()
    return reqs


def parse_milestones(path: Path, text: str):
    """Return {id: (title, line, status)}; status is the section's `- 狀態：` value or None."""
    out: "OrderedDict[str, tuple[str, int, str | None]]" = OrderedDict()
    in_gen = False
    cur = None
    for n, line in enumerate(text.splitlines(), 1):
        if line.strip() == GEN_BEGIN:
            in_gen = True
            cur = None
        elif line.strip() == GEN_END:
            in_gen = False
        elif not in_gen:
            m = MILESTONE_HEADING.match(line)
            if m:
                cur = m.group(1)
                out[cur] = (m.group(2).strip(), n, None)
            elif line.startswith("#"):
                cur = None
            elif cur and line.startswith("- 狀態："):
                title, ln, _ = out[cur]
                out[cur] = (title, ln, line.split("：", 1)[1].strip())
    return out


def render_scope(milestones, reqs: list[Req]) -> str:
    lines = [GEN_BEGIN, "", "## 範圍索引（自動產生，勿手改）", ""]
    for mid, (title, _, status) in milestones.items():
        lines.append(f"**{mid} {title}（approved）**" if status == "approved" else f"**{mid} {title}**")
        lines.append("")
        scoped = [r for r in reqs if r.milestone == mid and not r.withdrawn]
        if not scoped:
            lines.append("- （尚無需求）")
        for r in scoped:
            acs = "、".join(a.id for a in r.acs if not a.withdrawn)
            lines.append(f"- {r.id} {r.title}：{acs}")
        lines.append("")
    lines.append(GEN_END)
    return "\n".join(lines)


def check_card_pool(path: Path, data: dict, milestones, rep: Report) -> None:
    cards = data.get("cards") or []
    lords = {l.get("id"): l for l in data.get("lords") or []}
    factions = {f.get("id"): f for f in data.get("factions") or []}
    rules = data.get("deck_rules") or {}
    by_id: dict = {}
    for c in cards:
        cid = c.get("id")
        if cid in by_id:
            rep.err(path, None, f"卡片編號重複：{cid}")
        by_id[cid] = c
        if c.get("faction") not in factions:
            rep.err(path, None, f"{cid} 的陣營不存在：{c.get('faction')}")
        if c.get("type") not in {"unit", "general", "stratagem"}:
            rep.err(path, None, f"{cid} 的 type 不合法：{c.get('type')}")
        if c.get("type") in {"unit", "general"}:
            for k in ("troop", "attack", "hp"):
                if k not in c:
                    rep.err(path, None, f"{cid} 缺少 {k}")
            if c.get("troop") not in {"步", "騎", "弓", "謀"}:
                rep.err(path, None, f"{cid} 的 troop 不合法：{c.get('troop')}")
    for f in factions.values():
        if f.get("lord") and f["lord"] not in lords:
            rep.err(path, None, f"陣營 {f.get('id')} 的主公不存在：{f['lord']}")
        if milestones and f.get("milestone") not in milestones:
            rep.err(path, None, f"陣營 {f.get('id')} 的里程碑不存在：{f.get('milestone')}")
    for lid, l in lords.items():
        if l.get("faction") not in factions:
            rep.err(path, None, f"主公 {lid} 的陣營不存在：{l.get('faction')}")
    size = rules.get("size")
    max_copies = rules.get("max_copies")
    max_general = rules.get("max_copies_general")
    for d in data.get("decks") or []:
        did = d.get("id")
        dcards = d.get("cards") or {}
        total = sum(dcards.values())
        if size is not None and total != size:
            rep.err(path, None, f"牌組 {did} 有 {total} 張，規則要求 {size} 張")
        if d.get("lord") not in lords:
            rep.err(path, None, f"牌組 {did} 的主公不存在：{d.get('lord')}")
        elif lords[d["lord"]].get("faction") != d.get("faction"):
            rep.err(path, None, f"牌組 {did} 的主公不屬於陣營 {d.get('faction')}")
        if milestones and d.get("milestone") not in milestones:
            rep.err(path, None, f"牌組 {did} 的里程碑不存在：{d.get('milestone')}")
        for cid, count in dcards.items():
            c = by_id.get(cid)
            if c is None:
                rep.err(path, None, f"牌組 {did} 引用不存在的卡：{cid}")
                continue
            if c.get("collectible") is False:
                rep.err(path, None, f"牌組 {did} 含不可收集的卡：{cid}")
            if c.get("faction") not in {d.get("faction"), "neutral"}:
                rep.err(path, None, f"牌組 {did} 含他陣營的卡：{cid}")
            limit = max_general if c.get("type") == "general" else max_copies
            if limit is not None and count > limit:
                rep.err(path, None, f"牌組 {did} 的 {cid} 有 {count} 張，上限 {limit}")


def check_product(pdir: Path, rep: Report, fix: bool = False, expected_slug: str | None = None) -> None:
    slug = expected_slug or pdir.name
    md_files = sorted(pdir.rglob("*.md"))
    readme = pdir / "README.md"
    if not readme.exists():
        rep.err(pdir, None, "缺少 README.md")
    for required in ("prd.md", "milestones.md", "changelog.md"):
        if not (pdir / required).exists():
            rep.err(pdir, None, f"缺少 {required}")

    texts: dict[Path, str] = {}
    metas: dict[Path, dict] = {}
    for p in md_files:
        text = p.read_text(encoding="utf-8")
        texts[p] = text
        meta, _ = split_frontmatter(text)
        if meta is None:
            rep.err(p, 1, "缺少 frontmatter")
            continue
        metas[p] = meta
        st = meta.get("status")
        if st not in STATUSES:
            rep.err(p, 1, f"status 必須是 {sorted(STATUSES)} 之一，目前是 {st!r}")
        if st == "superseded" and not meta.get("superseded_by"):
            rep.err(p, 1, "status 為 superseded 時必須有 superseded_by")

    meta = metas.get(readme)
    if meta is not None:
        if meta.get("product") != slug:
            rep.err(readme, 1, f"product 應為 {slug!r}，目前是 {meta.get('product')!r}")
        if not meta.get("title"):
            rep.err(readme, 1, "缺少 title")
        for k in ("impl_repos", "desk_cards"):
            if not isinstance(meta.get(k), list):
                rep.err(readme, 1, f"{k} 必須是清單")

    mpath = pdir / "milestones.md"
    milestones = parse_milestones(mpath, texts[mpath]) if mpath in texts else OrderedDict()
    if mpath in texts and not milestones:
        rep.err(mpath, None, "沒有任何 `## M<n> 名稱` 里程碑")
    for mid, (_, mline, mstatus) in milestones.items():
        # A milestone without a 狀態 line is draft.
        if mstatus is not None and mstatus not in MILESTONE_STATUSES:
            rep.err(mpath, mline, f"{mid} 的狀態必須是 draft 或 approved，目前是 {mstatus!r}")
    approved = {mid for mid, v in milestones.items() if v[2] == "approved"}
    if approved and metas.get(mpath, {}).get("status") != "approved":
        rep.err(mpath, 1, "有里程碑為 approved 時，milestones.md 的 status 必須是 approved")

    reqs: list[Req] = []
    areas: dict[str, Path] = {}
    for p in sorted((pdir / "requirements").glob("*.md")):
        m = metas.get(p)
        if m is None:
            continue
        area = m.get("area")
        if not isinstance(area, str) or not AREA.match(area):
            rep.err(p, 1, f"area 必須是 2–4 個大寫英文字母，目前是 {area!r}")
            continue
        if area in areas:
            rep.err(p, 1, f"area {area} 已被 {areas[area].name} 使用")
        areas[area] = p
        reqs.extend(parse_requirements(p, texts[p], area, rep))

    seen: dict[str, tuple[Path, int]] = {}
    for r in reqs:
        for item in [r, *r.acs]:
            if item.id in seen:
                sp, sl = seen[item.id]
                rep.err(item.path, item.line, f"{item.id} 重複（先出現在 {sp.name}:{sl}）")
            else:
                seen[item.id] = (item.path, item.line)
        if r.withdrawn:
            continue
        if not r.title:
            rep.err(r.path, r.line, f"{r.id} 缺少標題")
        if r.milestone is None:
            rep.err(r.path, r.line, f"{r.id} 缺少「- 里程碑：M<n>」")
        elif r.milestone not in milestones:
            rep.err(r.path, r.line, f"{r.id} 的里程碑 {r.milestone} 不在 milestones.md")
        if r.milestone in approved and metas.get(r.path, {}).get("status") != "approved":
            rep.err(r.path, r.line, f"{r.id} 屬於已批准的 {r.milestone}，所在檔案的 status 必須是 approved")
        if r.priority is not None and r.priority not in PRIORITIES:
            rep.err(r.path, r.line, f"{r.id} 的優先必須是 {'／'.join(sorted(PRIORITIES))}")
        live = [a for a in r.acs if not a.withdrawn]
        if not live:
            rep.err(r.path, r.line, f"{r.id} 沒有任何 AC")
        for a in live:
            for key in ("Given", "When", "Then"):
                if not a.fields.get(key):
                    rep.err(a.path, a.line, f"{a.id} 缺少「- {key} …」")
            v = a.fields.get("驗證")
            if v not in VERIFY:
                rep.err(a.path, a.line, f"{a.id} 的驗證必須是 {'／'.join(sorted(VERIFY))}，目前是 {v!r}")

    # Every REQ/AC id mentioned anywhere in the product must exist.
    for p, text in texts.items():
        for n, line in enumerate(text.splitlines(), 1):
            for ref in ID_REF.findall(line):
                if ref not in seen and not p.name.startswith("changelog"):
                    rep.err(p, n, f"引用不存在的編號 {ref}")

    # Generated scope index.
    if mpath in texts:
        text = texts[mpath]
        expected = render_scope(milestones, reqs)
        if GEN_BEGIN not in text or GEN_END not in text:
            rep.err(mpath, None, f"缺少自動產生區塊 {GEN_BEGIN} … {GEN_END}")
        else:
            start = text.index(GEN_BEGIN)
            end = text.index(GEN_END) + len(GEN_END)
            if text[start:end] != expected:
                if fix:
                    mpath.write_text(text[:start] + expected + text[end:], encoding="utf-8")
                else:
                    rep.err(mpath, None, "範圍索引過期，請執行 scripts/check_specs.py --fix")

    for p in sorted(pdir.glob("data/*.y*ml")):
        try:
            data = yaml.safe_load(p.read_text(encoding="utf-8"))
        except yaml.YAMLError as e:
            rep.err(p, None, f"YAML 解析失敗：{e}")
            continue
        if isinstance(data, dict) and data.get("schema") == "card-pool/v1":
            check_card_pool(p, data, milestones, rep)


def check_links(root: Path, rep: Report) -> None:
    for p in sorted(root.rglob("*.md")):
        if ".git" in p.parts:
            continue
        in_code = False
        for n, line in enumerate(p.read_text(encoding="utf-8").splitlines(), 1):
            if line.lstrip().startswith("```"):
                in_code = not in_code
                continue
            if in_code:
                continue
            for target in LINK.findall(line):
                if re.match(r"^[a-z]+:", target) or target.startswith("#"):
                    continue
                path_part = target.split("#", 1)[0]
                if not path_part:
                    continue
                if not (p.parent / path_part).resolve().exists():
                    rep.err(p, n, f"連結目標不存在：{target}")


def run(root: Path, fix: bool = False) -> list[str]:
    rep = Report(root)
    products = root / "products"
    if products.is_dir():
        for pdir in sorted(d for d in products.iterdir() if d.is_dir()):
            check_product(pdir, rep, fix=fix)
    template = root / "templates" / "product"
    if template.is_dir():
        check_product(template, rep, fix=fix, expected_slug="example")
    check_links(root, rep)
    return rep.errors


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", type=Path, default=Path(__file__).resolve().parent.parent)
    ap.add_argument("--fix", action="store_true", help="重建 milestones.md 的範圍索引")
    args = ap.parse_args(argv)
    errors = run(args.root.resolve(), fix=args.fix)
    if args.fix:
        errors = run(args.root.resolve(), fix=False)
    for e in errors:
        print(e)
    if errors:
        print(f"\n{len(errors)} 個錯誤", file=sys.stderr)
        return 1
    print("check_specs: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
