"""Skills engine — skills.sh-compatible install + local cryo-omega registry."""
import json
import re
import shutil
import subprocess
import tempfile
from pathlib import Path

from . import config

SKILL_MD = "SKILL.md"
FRONT_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.S)


def frontmatter(path):
    m = FRONT_RE.match(Path(path).read_text(errors="replace"))
    if not m:
        return {}
    meta = {}
    for line in m.group(1).splitlines():
        if ":" in line:
            k, _, v = line.partition(":")
            meta[k.strip()] = v.strip()
    return meta


def local_skills():
    out = []
    for d in sorted(config.SKILLS_DIR.glob("*")):
        sm = d / SKILL_MD
        if d.is_dir() and sm.exists():
            meta = frontmatter(sm)
            out.append({
                "name": d.name,
                "path": str(d),
                "description": meta.get("description", "")[:120],
                "location": meta.get("location", str(sm)),
            })
    return out


def search(term):
    term = term.lower()
    return [s for s in local_skills()
            if term in s["name"].lower() or term in s["description"].lower()]


def add(repo, target=None):
    """Install skills from a GitHub repo (skills.sh protocol).

    Accepts `owner/repo`. Clones shallow, finds every SKILL.md, and installs
    each parent directory into ~/.agents/skills/<dir-name>.
    """
    repo = repo.strip().removeprefix("https://github.com/").removesuffix(".git")
    if "/" not in repo:
        raise ValueError("expected owner/repo")
    target = target or config.SKILLS_DIR
    target.mkdir(parents=True, exist_ok=True)
    tmp = Path(tempfile.mkdtemp(prefix="omega-skill-"))
    try:
        url = f"https://github.com/{repo}.git"
        r = subprocess.run(
            ["git", "clone", "--depth", "1", url, str(tmp / "repo")],
            capture_output=True, text=True, timeout=120,
        )
        if r.returncode != 0:
            raise RuntimeError(f"clone failed: {r.stderr.strip()[:200]}")
        installed = []
        for sm in sorted((tmp / "repo").rglob(SKILL_MD)):
            src = sm.parent
            dest = target / src.name
            if dest.exists():
                shutil.rmtree(dest)
            shutil.copytree(src, dest, ignore=shutil.ignore_patterns(".git"))
            installed.append(dest.name)
        return installed
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def info(name):
    for s in local_skills():
        if s["name"] == name:
            p = Path(s["path"]) / SKILL_MD
            body = FRONT_RE.sub("", p.read_text(errors="replace")).strip()
            return s, body[:600]
    raise KeyError(name)
