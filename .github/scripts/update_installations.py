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
GRAPH_WIDTH = 900
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
    addons = addon_metadata(configs)
    days = sorted(history)
    values = [count for day in days for count in history[day].values()]
    maximum = max(values, default=1)
    left, top, plot_width, plot_height = 70, 30, GRAPH_WIDTH - 100, GRAPH_HEIGHT - 90
    colors = ["#03a9f4", "#ff9800", "#4caf50", "#e91e63", "#9c27b0"]
    lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {GRAPH_WIDTH} {GRAPH_HEIGHT}" role="img">',
        '<title>Home Assistant add-on installations over the last year</title>',
        '<rect width="100%" height="100%" fill="white"/>',
        f'<line x1="{left}" y1="{top + plot_height}" x2="{left + plot_width}" y2="{top + plot_height}" stroke="#666"/>',
        f'<line x1="{left}" y1="{top}" x2="{left}" y2="{top + plot_height}" stroke="#666"/>',
    ]
    if days:
        for index, addon in enumerate(addons):
            points = []
            for position, day in enumerate(days):
                x = left + (position * plot_width / max(len(days) - 1, 1))
                y = top + plot_height - history[day].get(addon["directory"], 0) * plot_height / maximum
                points.append(f"{x:.1f},{y:.1f}")
            color = colors[index % len(colors)]
            lines.append(
                f'<polyline points="{" ".join(points)}" fill="none" stroke="{color}" stroke-width="2"/>'
            )
            legend_x = left + index * 170
            lines.append(
                f'<text x="{legend_x}" y="{GRAPH_HEIGHT - 25}" fill="{color}" font-size="12">{escape(addon["name"])}</text>'
            )
        lines.append(f'<text x="{left}" y="{GRAPH_HEIGHT - 8}" font-size="11">{days[0]}</text>')
        lines.append(f'<text x="{left + plot_width - 70}" y="{GRAPH_HEIGHT - 8}" font-size="11">{days[-1]}</text>')
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
