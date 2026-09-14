#!/usr/bin/env python3
"""Publish docs/wiki/index.md to the GitHub Wiki Home page (Repo → Wiki only).

Usage:
  python3 tools/publish_wiki_home.py [--dry-run] [--wiki-dir PATH]

Requires git write access to https://github.com/OWNER/REPO.wiki.git
Does not invent Wiki pages beyond Home. Never syncs Wiki → repo.
"""
from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
INDEX = REPO / "docs" / "wiki" / "index.md"
DEFAULT_REMOTE = None  # resolved from origin


def _run(cmd: list[str], cwd: Path | None = None, check: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, cwd=cwd, check=check, text=True, capture_output=True)


def origin_https() -> str:
    out = _run(["git", "-C", str(REPO), "remote", "get-url", "origin"]).stdout.strip()
    # git@github.com:owner/repo.git or https://github.com/owner/repo.git
    m = re.search(r"github\.com[:/](?P<owner>[^/]+)/(?P<repo>[^/.]+)", out)
    if not m:
        raise SystemExit(f"cannot parse GitHub origin from: {out}")
    return f"https://github.com/{m.group('owner')}/{m.group('repo')}.wiki.git"


def rewrite_links(md: str, blob_base: str) -> tuple[str, list[str]]:
    """Rewrite relative links that leave docs/wiki/ to blob URLs on main."""
    notes: list[str] = []

    def repl(match: re.Match[str]) -> str:
        label, path = match.group(1), match.group(2)
        if path.startswith(("http://", "https://", "#", "mailto:")):
            return match.group(0)
        # paths under docs/wiki stay as-is for future multi-page mirror
        if not path.startswith("../"):
            return match.group(0)
        # ../x from docs/wiki → docs/x ; ../../x → repo root
        parts = Path("docs/wiki").joinpath(path).resolve()
        try:
            rel = parts.relative_to(REPO.resolve())
        except ValueError:
            notes.append(f"unresolved link kept: {path}")
            return match.group(0)
        url = f"{blob_base}/{rel.as_posix()}"
        notes.append(f"{path} → {url}")
        return f"[{label}]({url})"

    out = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", repl, md)
    return out, notes


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--dry-run", action="store_true", help="print Home.md; do not push")
    ap.add_argument("--wiki-dir", type=Path, default=None, help="existing wiki working copy")
    args = ap.parse_args()

    if not INDEX.is_file():
        print(f"missing SoT: {INDEX}", file=sys.stderr)
        return 2

    owner_repo = origin_https().removesuffix(".wiki.git").removeprefix("https://github.com/")
    blob_base = f"https://github.com/{owner_repo}/blob/main"
    raw = INDEX.read_text(encoding="utf-8")
    home, notes = rewrite_links(raw, blob_base)
    header = (
        "<!-- Published from docs/wiki/index.md — Do not edit on GitHub Wiki. "
        "Source of truth: repository docs/wiki/ (Repo → Wiki only). -->\n\n"
    )
    body = header + home

    print("Sync policy: repository → GitHub Wiki only")
    print(f"SoT: {INDEX.relative_to(REPO)}")
    print("Target: Wiki Home.md")
    for n in notes:
        print(f"  rewrite: {n}")

    if args.dry_run:
        print("--- Home.md (dry-run) ---")
        print(body)
        return 0

    wiki_url = origin_https()
    tmp_owned = False
    if args.wiki_dir:
        wiki = args.wiki_dir
        if not (wiki / ".git").exists():
            print(f"wiki-dir is not a git repo: {wiki}", file=sys.stderr)
            return 2
    else:
        wiki = Path(tempfile.mkdtemp(prefix="omega-wiki-"))
        tmp_owned = True
        try:
            _run(["git", "clone", "--depth", "1", wiki_url, str(wiki)])
        except subprocess.CalledProcessError as e:
            print(e.stderr or e.stdout, file=sys.stderr)
            print(
                "Clone failed. Ensure the GitHub Wiki is initialized "
                "(create Home once in the UI) and credentials can push .wiki.git.",
                file=sys.stderr,
            )
            if tmp_owned:
                shutil.rmtree(wiki, ignore_errors=True)
            return 2

    try:
        (wiki / "Home.md").write_text(body, encoding="utf-8")
        _run(["git", "add", "Home.md"], cwd=wiki)
        st = _run(["git", "status", "--porcelain"], cwd=wiki, check=False)
        if not st.stdout.strip():
            print("No changes to publish.")
            return 0
        _run(
            [
                "git",
                "-c",
                "user.name=CryoOmega Docs",
                "-c",
                "user.email=docs@users.noreply.github.com",
                "commit",
                "-m",
                "docs(wiki): mirror Home from docs/wiki/index.md",
            ],
            cwd=wiki,
        )
        _run(["git", "push", "origin", "HEAD"], cwd=wiki)
        print("Published Wiki Home from docs/wiki/index.md")
        return 0
    finally:
        if tmp_owned:
            shutil.rmtree(wiki, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
