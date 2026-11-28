import hashlib
import json
import re
import sys
from datetime import date, datetime, timedelta, timezone
from html import escape
from pathlib import Path


REPOSITORY_URL = "https://github.com/minims/homeassistant-addons"
PREFIXES = tuple(
    hashlib.sha1(url.encode()).hexdigest()[:8] + "_"
    for url in (REPOSITORY_URL, REPOSITORY_URL + "/")
)
HISTORY_DAYS = 365
GRAPH_WIDTH = 1100
GRAPH_HEIGHT = 360


def addon_metadata(configs):
    metadata = []
    for config in configs:
        settings = config.read_text(encoding="utf-8")
        metadata.append(
            {
                "name": re.search(r"^name: (.+)$", settings, re.MULTILINE).group(1),
                "slug": re.search(r"^slug: (\S+)$", settings, re.MULTILINE).group(1),
                "directory": config.parent.name,
            }
        )
    return metadata


def installation_counts(analytics, configs):
    if not isinstance(analytics, dict) or not any(
        slug.startswith(PREFIXES) for slug in analytics
    ):
        raise ValueError("Analytics contains no entries for this repository")
    counts = {}
    for addon in addon_metadata(configs):
        totals = [
            analytics.get(prefix + addon["slug"], {"total": 0})["total"]
            for prefix in PREFIXES
        ]
        if any(type(total) is not int or total < 0 for total in totals):
            raise ValueError(f"Invalid installation count for {addon['slug']}")
        counts[addon["directory"]] = sum(totals)
    return counts


def installation_rows(analytics, configs):
    counts = installation_counts(analytics, configs)
    return [
        f"| [{addon['name']}](./{addon['directory']}) | {counts[addon['directory']]} |"
        for addon in addon_metadata(configs)
    ]


def update_history(history, refreshed, counts):
    history = {**history, refreshed: counts}
    cutoff = date.fromisoformat(refreshed) - timedelta(days=HISTORY_DAYS - 1)
    return {
        day: history[day]
        for day in sorted(history)
        if date.fromisoformat(day) >= cutoff
    }


def render_svg(history, configs):
    days = sorted(history)
    totals = {day: sum(history[day].values()) for day in days}
    maximum = max(totals.values(), default=0)
    cell, gap = 13, 3
    left, top, legend_left = 32, 24, 780
    colors = ["#ebedf0", "#9be9a8", "#40c463", "#30a14e", "#216e39"]
    lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {GRAPH_WIDTH} 190" role="img">',
        '<title>Home Assistant add-on installations over the last year</title>',
        '<rect width="100%" height="100%" fill="white"/>',
        '<text x="32" y="14" fill="#24292f" font-size="12">Installations</text>',
    ]
    if days:
        first = date.fromisoformat(days[0])
        start = first - timedelta(days=(first.weekday() + 1) % 7)
        for offset in range(((date.fromisoformat(days[-1]) - start).days // 7 + 1) * 7):
            day = start + timedelta(days=offset)
            if day.day == 1 or offset == 0:
                column = offset // 7
                lines.append(f'<text x="{left + column * (cell + gap)}" y="22" font-size="10">{day:%b}</text>')
            if offset % 7 == 1:
                lines.append(f'<text x="2" y="{top + (offset % 7) * (cell + gap) + 10}" font-size="9">Mon</text>')
            if day.isoformat() not in totals:
                continue
            total = totals[day.isoformat()]
            level = 0 if maximum == 0 else min(4, (total * 4) // maximum + (total > 0))
            column, row = offset // 7, offset % 7
            x, y = left + column * (cell + gap), top + row * (cell + gap)
            lines.append(
                f'<rect x="{x}" y="{y}" width="{cell}" height="{cell}" rx="2" fill="{colors[level]}"><title>{day.isoformat()}: {total} installations</title></rect>'
            )
    legend_y = 58
    lines.append(f'<text x="{legend_left}" y="{legend_y - 14}" fill="#24292f" font-size="11">installations</text>')
    for index, color in enumerate(colors):
        x = legend_left + index * 24
        lines.append(f'<rect x="{x}" y="{legend_y}" width="16" height="16" rx="2" fill="{color}"/>')
    lines.append(f'<text x="{legend_left}" y="{legend_y + 32}" font-size="10">0</text>')
    lines.append(f'<text x="{legend_left + 96}" y="{legend_y + 32}" font-size="10">{maximum} installations</text>')
    if days:
        lines.append(f'<text x="{left}" y="170" font-size="10">{days[0]}</text>')
        lines.append(f'<text x="{left + 690}" y="170" font-size="10">{days[-1]}</text>')
    lines.append("</svg>")
    return "\n".join(lines) + "\n"


def readme_with_installations(readme, analytics, configs, refreshed=None):
    refreshed = refreshed or datetime.now(timezone.utc).date().isoformat()
    rows = installation_rows(analytics, configs)
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


def update_files(root, analytics, refreshed=None):
    configs = sorted(root.glob("*/config.yaml"))
    refreshed = refreshed or datetime.now(timezone.utc).date().isoformat()
    counts = installation_counts(analytics, configs)
    history_path = root / ".github/data/installations.json"
    history = json.loads(history_path.read_text(encoding="utf-8")) if history_path.exists() else {}
    history_path.parent.mkdir(parents=True, exist_ok=True)
    history = update_history(history, refreshed, counts)
    history_path.write_text(json.dumps(history, indent=2) + "\n", encoding="utf-8")
    (root / ".github/data/installations.svg").write_text(render_svg(history, configs), encoding="utf-8")
    readme = root / "README.md"
    content = readme_with_installations(readme.read_text(encoding="utf-8"), analytics, configs, refreshed)
    marker = "<!-- installations-graph -->"
    graph = f'{marker}\n\n![Installation evolution over the last year](.github/data/installations.svg)\n'
    content = re.sub(r"<!-- installations-graph -->.*?(?=\n### )", graph, content, flags=re.DOTALL)
    if marker not in content:
        content = content.replace("<!-- installations:end -->", "<!-- installations:end -->\n\n" + graph)
    readme.write_text(content, encoding="utf-8")


if __name__ == "__main__":
    root = Path(__file__).resolve().parents[2]
    update_files(root, json.load(sys.stdin))
