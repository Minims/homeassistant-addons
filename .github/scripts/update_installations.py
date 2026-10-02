import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path


REPOSITORY_URL = "https://github.com/minims/homeassistant-addons"
PREFIXES = tuple(
    hashlib.sha1(url.encode()).hexdigest()[:8] + "_"
    for url in (REPOSITORY_URL, REPOSITORY_URL + "/")
)


def installation_rows(analytics, configs):
    if not isinstance(analytics, dict) or not any(
        slug.startswith(PREFIXES) for slug in analytics
    ):
        raise ValueError("Analytics contains no entries for this repository")
    rows = []
    for config in configs:
        # ponytail: plain top-level scalars; use a YAML parser for quoted/multiline fields.
        settings = config.read_text(encoding="utf-8")
        name = re.search(r"^name: (.+)$", settings, re.MULTILINE).group(1)
        slug = re.search(r"^slug: (\S+)$", settings, re.MULTILINE).group(1)
        totals = [
            analytics.get(prefix + slug, {"total": 0})["total"] for prefix in PREFIXES
        ]
        if any(type(total) is not int or total < 0 for total in totals):
            raise ValueError(f"Invalid installation count for {slug}")
        rows.append(f"| [{name}](./{config.parent.name}) | {sum(totals)} |")
    return rows


def readme_with_installations(readme, analytics, configs):
    rows = installation_rows(analytics, configs)
    refreshed = datetime.now(timezone.utc).date().isoformat()
    section = "\n".join(
        [
            "<!-- installations:start -->", "",
            "| Add-on | Reported installations |",
            "| --- | ---: |",
            *rows, "", f"Last refreshed: {refreshed} (UTC).", "",
            "<!-- installations:end -->",
        ]
    )
    updated, replacements = re.subn(
        r"<!-- installations:start -->.*?<!-- installations:end -->",
        lambda match: section, readme, flags=re.DOTALL,
    )
    if replacements != 1:
        raise ValueError("README must contain exactly one installation section")
    return updated


if __name__ == "__main__":
    root = Path(__file__).resolve().parents[2]
    analytics = json.load(sys.stdin)
    readme = root / "README.md"
    updated = readme_with_installations(
        readme.read_text(encoding="utf-8"), analytics, sorted(root.glob("*/config.yaml")),
    )
    readme.write_text(updated, encoding="utf-8")
